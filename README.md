
# KT Map Base Table

This repo is for development of the [KT Map Base Table][ktmbt_item] steam workshop mod

## Usage with Steam Workshop item

1. Subscribe to the [workshop item][ktmbt_item]
1. Open Tabletop simulator
1. Create a multiplayer game and select "KT Map Base Table"
1. Invite a friend and play

## Usage from development branches

1. Select desired branch from [current dev branches](https://github.com/feuerfritas/kt-map-base-table/branches)
1. Download [`2574389665.json`](./2574389665.json) and [`2574389665.png`](./2574389665.png)
1. Save files to `%HOMEPATH%\Documents\My Games\Tabletop Simulator\Saves`
1. Open TTS and load save game called "KT Map Base Table"

## Development

### Windows Setup

1. Install [git](https://git-scm.com/download/win) if not already installed
1. Open a Command Prompt
    ```
    %HOMEDRIVE%
    cd %HOMEPATH%\Documents\My Games\Tabletop Simulator\Saves
    ```
1. Clone this repository:
    ```
    git clone git@github.com:feuerfritas/kt-map-base-table.git
    ```
1. Open Tabletop Simulator
1. Create a new game
1. Load save game in kt-map-base-table folder
1. Install atom and tabletop simulator plugin. See this [guide](https://api.tabletopsimulator.com/atom/#installing-the-official-plugin)
1. Once installed tabletop-simulator-plugin lookup path
    ```
    File->Settings
    ->filter by writing tabletop-simulator-lua on the package search bar
    ->Settings
    ->Base path for files you wish to bundle or #include
    write C:\Users\Feuer\Documents\My Games\Tabletop Simulator\Saves\KT Map Base Table replacing "Feuer" with your username
    ```
1. We are almost there! now add the repo to atom by doing:
    ```
    File->Add project folder
    %HOMEPATH%\Documents\My Games\Tabletop Simulator\Saves\kt-map-base-table
    ```
1. Last Step!
    ```
    Packages->Tabletop Simulator->Get Lua Scripts
    ```
1. Happy Coding!

## TODO

- Ideally we don't want to have the big savefile blob here.
  - We need somewhere else to store it
  - It seemed easier to go this way instead of adding more repos and making dev setup harder.
  - We might have to do it if savefile becomes larger than github's limit (100Mb?)
- Maybe switch dev environment to vscode
  - Github is sunsetting Atom Editor
  - There seems to be a tabletop simulator plugin for vscode [here](https://marketplace.visualstudio.com/items?itemName=rolandostar.tabletopsimulator-lua)
    - Not official yet




## Development notes for game resources

- Image generation uses json data from killteamjson project
- Requires gimp development version to support markup in text: https://www.gimp.org/downloads/devel/


## Other useful TTS commands

Commands doc here: https://github.com/Berserk-Games/Tabletop-Simulator-Console-Commands/blob/main/Commands.md

### Copy chat text

```
exec chat_tab_game; chat_copy
```

### Change rewind interval to improve performance

`rewind_interval` defines how often `onSave` will be called for each object. Given that `JSON.encode` is pretty slow for large objects, the default setting of `10` might make the game lag quite a lot. I recommend setting it to something closer to the autosave interval.

```
rewind_interval 150
```

### Enable a second screen

Move camera around and save current view with with `CTRL+1`

```
spectator_screen 1
spectator_camera_load 1
```

### Second screen ui (not functional, just rendered)

```
spectator_show_ui 1
```

### Highlight object

```
highlight guid [duration] [color]
```

### Extract player rolls from save game (requires [jq](https://stedolan.github.io/jq/) tool)

```
cat TS_Save_13231.json | jq -r '.ObjectStates[] | select (.GUID == "bafa93") | .LuaScriptState ' 2>&1 | grep -Ev '^$' | jq 'select(.type == "roll") | select(.player=="Feuerfritas") | .rolls[]'
```

### End game score:

```
cat TS_Save_13250.json | jq -r '.ObjectStates[] | select(.GUID == "bafa93") | .LuaScriptState' | jq -r '. | select(.type == "scoring") | .score' | jq -cs '.[]' | tail -n 1 | jq .
```

## Other resources:

- Structured kill team data (ploys, tac ops, etc) [killteamjson](https://github.com/vjosset/killteamjson)

```
 cat compendium.json | jq '.[].killteams[] | select(.killteamname == "Pathfinders") | .ploys[][] | {name: .ployname, description: .description}' | jq -s .
```

[ktmbt_item]: https://steamcommunity.com/sharedfiles/filedetails/?id=2574389665




"Full screen" (https://skfb.ly/6TO9E) by ChesterGames is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
