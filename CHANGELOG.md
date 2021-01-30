## 0.4.4

- `raw` commands are now autocompleted to the Zookeeper 4 letter words
- New commands: `tree` and `ftree` (thanks [`@mackong`](https://github.com/mackong)!)
- Fix colorization of commands composed of 4 letters that are not zookeeper 4 letter words
- Switch from Pipenv to Poetry to lock dependencies

## 0.3.1
Improvements:
- Enable vi mode by default
- Don't display a traceback when mashing Ctrl-D on exit confirmation message

Fixes:
- `raw` commands are now usable (reported by @hzluyang)

## 0.3.0
New command:
 - `edit`: opens an editor to edit the content of a znode

Improvements:
- If only a path is given to `set`, an editor will be opened to type-in the ZNode data
- Command validation refactoring
