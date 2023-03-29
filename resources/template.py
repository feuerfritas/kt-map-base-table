#!/usr/bin/python

import os, glob, sys, time
from gimpfu import *
import traceback
import json


def log(str):
    pdb.gimp_message(str)


def get_factions():
    with open('compendium.json') as data:
        factions = json.loads(data.read())
    return factions


def set_layer_text(image, layer_name, text):
    layer = pdb.gimp_image_get_layer_by_name(image, layer_name)
    log('setting text to layer {} : {}'.format(layer_name, text))
    pdb.gimp_text_layer_set_text(layer, text)


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
    set_layer_text(image, 'description', description)
    new_image = pdb.gimp_image_duplicate(image)
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    filename = os.path.join(out_dir, "{}-{}.png".format(ploy_type, ploy))
    new_image = pdb.gimp_image_duplicate(image)
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(new_image, layer, filename, '?')
    pdb.gimp_image_delete(new_image)


def generate_ploys_for(image, killteam):
    out_path = killteam['killteamname']
    os.mkdir(killteam['killteamname'])
    for type in ['strat', 'tac']:
        log(type)
        for ploy in killteam['ploys'][type]:
            generate_ploy(
                image,
                out_path,
                type,
                killteam['killteamname'],
                ploy['ployname'],
                ploy['CP'],
                ploy['description']
            )

def _run(directory):
    start=time.time()
    template_path = 'ploys-template.xcf'
    image = pdb.gimp_file_load(template_path, template_path, run_mode=RUN_NONINTERACTIVE)
    for faction in get_factions():
        for killteam in faction['killteams']:
            log(killteam['killteamname'])
            generate_ploys_for(image, killteam)
        end=time.time()
        log("Finished, total processing time: %.2f seconds" % (end-start))

def run(dir):
    try:
        pdb.gimp_message(os.getcwd())
        _run(dir)
    except Exception as e:
        pdb.gimp_message(traceback.format_exc())

if __name__ == "__main__":
    print "Running as __main__ with args: %s" % sys.argv
