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
