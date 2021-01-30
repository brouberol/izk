# Contributing to IZK

First, thanks for even wanting to contribute to `izk`!

## Setup your environ,ent
To work on `izk` itself, fork the repository and clone your fork to your local system.

If you have `poetry` installed, you can let it install the dependencies:

```shell
$ cd path/to/izk
$ poery install
```

If you don't use `poetry`, you can simply use `pip` (bear in mind that you need python3 for local development)

```shell
$ cd path/to/izk
$ pip install .
```


## Run the tests
To run the test suite locally when using `poetry`

```shell
$ poetry run pytest
```


## Send the patch

Create a local branch on which you can commit your changes, push it to your fork, and open a pull-request on the main repo. If Travis reports broken tests, please fix them, otherwise the pull request will not be merged.
