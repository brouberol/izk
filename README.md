# IZK: interactive zookeeper

[![Build Status](https://travis-ci.org/brouberol/izk.svg?branch=master)](https://travis-ci.org/brouberol/izk) [![Coverage Status](https://coveralls.io/repos/github/brouberol/izk/badge.svg?branch=master)](https://coveralls.io/github/brouberol/izk?branch=master)

`izk` is a modern and simple zookeeper shell, with autocompletion, history search, vi bindings, syntax highlighting and pretty-printing.

[![asciicast](https://asciinema.org/a/Cw1yNF3lu9Qkgqtg4n9jzvj54.png)](https://asciinema.org/a/Cw1yNF3lu9Qkgqtg4n9jzvj54?t=02)


## Installation

To install `izk`, simply run

```shell
$ pip install izk
```

`izk` is Python 3 only. I do not plan to support Python 2, but it that's important to you, feel free to contribute!

## Docker

`izk` is also available as a docker image. To run it, execute

```shell
$ docker run -it brouberol/izk
```

Note that to ease usage woith docker, all command-line arguments can be passed as environment variables, prefixed with `IZK_`.

Example: here is how to run `izk --write` in docker

```shell
$ docker run -it -e IZK_WRITE=1 brouberol/izk
```

## Usage

```
$ izk --help
usage: izk [-h] [--write WRITE]
           [--style {default,emacs, ...}]
           [--version]
           [zk_url]

CLI for zookeeper with syntax-highlighting and auto-completion.

positional arguments:
  zk_url                URL of the zookeeper node. Default: localhost:2181.
                        Override via the IZK_ZK_URL environment variable.

optional arguments:
  -h, --help            show this help message and exit
  --write WRITE         Authorize write operations (update/insert/remove).
                        Override via the IZK_WRITE environment variable.
  --style {default,emacs, ...}
                        The color style to adopt. Default: monokai. Override
                        via the IZK_STYLE environment variable.
  --input-mode {vi,emacs}
                        The input mode to adopt. Default: vi. Override via the
                        IZK_INPUT_MODE environment variable.
  --version             Display izk version number and exit

Version: 0.4.0
```
