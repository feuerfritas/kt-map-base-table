
# KT Map Base Table

## Setup

### Windows

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


## Other useful TTS commands

### Copy chat text

```
exec chat_tab_game; chat_copy
```

