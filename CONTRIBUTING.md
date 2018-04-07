# Contributing to IZK

First, thanks for even wanting to contribute to `izk`!

## Setup your environ,ent
To work on `izk` itself, fork the repository and clone your fork to your local system.

If you have `pipenv` installed, you can let it install the dependencies:

```shell
$ cd path/to/izk
$ pipenv install --dev --three
```

If you don't use `pipenv`, you can simply use `pip` (bear in mind that you need python3 for local development)

```shell
$ cd path/to/izk
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```


## Run the tests
To run the test suite locally when using `pipenv`

```shell
$ pipenv run py.test
```

Otherwise, just run
```shell
$ py.test
```


## Send the patch

Create a local branch on which you can commit your changes, push it to your fork, and open a pull-request on the main repo. If Travis reports broken tests, please fix them, otherwise the pull request will not be merged.
