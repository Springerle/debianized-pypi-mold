# debianized-pypi-mold

A [cookiecutter](http://cookiecutter.readthedocs.io/) template to
make a Debian package from an application's existing Python package
as released to PyPI or a private repository.
It creates a project to build a self-contained Python virtualenv wrapped into a Debian package
(an "omnibus" package, all passengers on board).
The packaged virtualenv is kept in sync with the host's interpreter automatically.

See [spotify/dh-virtualenv](https://github.com/spotify/dh-virtualenv) for more details,
and [1and1/debianized-sentry](https://github.com/1and1/debianized-sentry) for an example project.

 [![Groups](https://img.shields.io/badge/Google_groups-springerle--users-orange.svg)](https://groups.google.com/forum/#!forum/springerle-users)
 ![MIT licensed](http://img.shields.io/badge/license-MIT-red.svg)

The similar [dh-virtualenv-mold](https://github.com/Springerle/dh-virtualenv-mold)
adds packaging metadata to an existing Python project under your control.
That one should also be used when you want to contribute Debian packaging to an upstream project.


## Preparations

In case you don't have the `cookiecutter` command line tool yet, here's
[how to install](https://github.com/Springerle/springerle.github.io#installing-the-cookiecutter-cli) it.


## Using the template

Creating the packaging project goes like this (make sure you're in a suitable directory like ``~/src``):

```sh
cookiecutter https://github.com/Springerle/debianized-pypi-mold.git
cd ‹projectname›
dch -r "" # add a proper distro and date to the changelog
```

It makes sense to `git init` the created directory directly afterwards, and ``git add`` all files.
Do that before any additional files are generated, that you don't want to have in your repository.

Next check *all* the files for necessary changes regarding the software your're packaging.
The template makes some assumptions that often fit, but there's always some differences in details.
Delete anything you do not need, e.g. from the list of build dependencies.

The license used for the packaging project is “BSD 3-clause”, change the ``LICENSE``
file and “BSD” references in ``README.md`` and ``setup.py`` as needed.

See the template's README for more information on how to actually build the DEB package.
