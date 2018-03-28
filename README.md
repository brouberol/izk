# IZK: interactive zookeeper

[![Build Status](https://travis-ci.org/brouberol/izk.svg?branch=master)](https://travis-ci.org/brouberol/izk)

`izk` is a modern and simple zookeeper shell, with autoccompletion, history search, vi bindings, syntax highlighting and pretty-printing.

[![asciicast](https://asciinema.org/a/Cw1yNF3lu9Qkgqtg4n9jzvj54.png)](https://asciinema.org/a/Cw1yNF3lu9Qkgqtg4n9jzvj54?t=02)


## Installation

To install `izk`, simply run

```shell
$ pip install izk
```

`izk` is Python 3 only. I do not plan to support Python 2, but it that's important to you, feel free to contribute!

## Usage

```shell
$ izk --help
usage: izk [-h] [--write]
           [--style {default,emacs,...}]
           [zk_url]

CLI for zookeeper with syntax-highlighting and auto-completion

positional arguments:
  zk_url                URL of the zookeeper node. Default: localhost:2181

optional arguments:
  -h, --help            show this help message and exit
  --write               Authorize write operations (update/insert/remove)
  --style {default,emacs,...}
                        The color style to adopt. Default: monokai
```
