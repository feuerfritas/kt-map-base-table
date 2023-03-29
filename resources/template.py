#!/usr/bin/python

import os, glob, sys, time
import traceback
import json
import re
from gi.repository import Gimp
from gi.repository import Gio


def log(str):
    Gimp.message(str)


def get_factions():
    with open('compendium.json') as data:
        factions = json.loads(data.read())
    return factions


def set_layer_text(image, layer_name, text, set_markup=False):
    layer = Gimp.Image.get_layer_by_name(image, layer_name)
    log('setting text to layer {} : {}'.format(layer_name, text))
    Gimp.TextLayer.set_text(layer, text)
    if set_markup:
        Gimp.TextLayer.set_markup(layer, text)


def generate_ploy(image, out_dir, ploy_type, faction, ploy, cp, description):
    set_layer_text(image,
        'faction-type',
        '{} - {} Ploy'.format(
            faction,
            'Strategic' if ploy_type == 'strat' else 'Tactical'
        )
    )
    set_layer_text(image, 'title', ploy)
    set_layer_text(image, 'cost', '{} CP'.format(cp))
    set_layer_text(image, 'description', description, True)
    filename = os.path.join(out_dir, "{}-{}.xcf".format(ploy_type, ploy))
    new_image = Gimp.Image.duplicate(image)
    Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, new_image, new_image.list_layers(), Gio.File.new_for_path(filename))
    filename = os.path.join(out_dir, "{}-{}.png".format(ploy_type, ploy))
    layer = Gimp.Image.merge_visible_layers(new_image, Gimp.MergeType.CLIP_TO_IMAGE)
    Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, new_image, [layer], Gio.File.new_for_path(filename))
    Gimp.Image.delete(new_image)


def replace_markup(text):
    text = text.replace('[PENT]', '<span foreground="red">⬟</span>')
    text = text.replace('[SQUARE]', '<span foreground="blue">■</span>')
    text = text.replace('[CIRCLE]', '<span foreground="black">◯</span>')
    text = text.replace('[TRI]', '<span foreground="black">▲</span>')
    #text = text.replace('[PENT]', '⬟')
    #text = text.replace('[SQUARE]', '■')
    #text = text.replace('[CIRCLE]', '⬤')
    #text = text.replace('[TRI]', '▲')
    text = text.replace('<ul>', '')
    text = text.replace('</ul>', '')
    text = text.replace('</li>', '')
    text = text.replace('<br/>', '\n')
    text = text.replace('&nbsp;', '')
    text = re.sub('\s*<td[^>]*>', '', text)
    text = re.sub('\s*<th[^>]*>', '', text)
    text = re.sub('\s*<tr[^>]*>', '', text)
    text = re.sub('\s*<table[^>]*>', '\n', text)
    text = re.sub('</td>', '|', text)
    text = re.sub('</th>', '|', text)
    text = re.sub('\s*</tr>\s*', '\n', text)
    text = text.replace('</table>', '\n')
    return re.sub('\s*<li>', '\n • ', text)

def generate_ploys_for(image, killteam):
    out_path = killteam['killteamname']
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    for type in ['strat', 'tac']:
        for ploy in killteam['ploys'][type]:
            generate_ploy(
                image,
                out_path,
                type,
                killteam['killteamname'],
                ploy['ployname'].upper(),
                ploy['CP'],
                replace_markup(ploy['description'])
            )

def _run():
    start=time.time()
    template_path = 'ploys-template.xcf'
    image = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, Gio.File.new_for_path(template_path)) #
    for faction in get_factions():
        for killteam in faction['killteams']:
            log(killteam['killteamname'])
            generate_ploys_for(image, killteam)
        end=time.time()
        log("Finished, total processing time: %.2f seconds" % (end-start))

def run():
    try:
        _run()
    except Exception as e:
        log(traceback.format_exc())

if __name__ == "__main__":
    print("Running as __main__ with args: %s" % sys.argv)
