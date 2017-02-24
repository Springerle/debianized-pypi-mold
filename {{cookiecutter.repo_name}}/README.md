# "{{ cookiecutter.pypi_package }}" Debian Packaging

![BSD 3-clause licensed](http://img.shields.io/badge/license-BSD_3--clause-red.svg)
[![{{ cookiecutter.repo_name }}](http://img.shields.io/pypi/v/{{ cookiecutter.repo_name }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.repo_name }}/)
[![{{ cookiecutter.pypi_package }}](http://img.shields.io/pypi/v/{{ cookiecutter.pypi_package }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.pypi_package }}/)

**Contents**

 * [What is this?](#what-is-this)
 * [How to build and install the package](#how-to-build-and-install-the-package)
 * [How to set up a simple service instance](#how-to-set-up-a-simple-service-instance)
 * [Trouble-Shooting](#trouble-shooting)
   * ['pkg-resources not found' or similar during virtualenv creation](#pkg-resources-not-found-or-similar-during-virtualenv-creation)
 * [Configuration Files](#configuration-files)
 * [Data Directories](#data-directories)
 * [References](#references)
   * [Related Projects](#related-projects)


## What is this?

This project helps to install typical Python services like Django web applications on Debian-like target hosts,
by providing DEB packaging for the server component.
This makes life-cycle management on production hosts a lot easier, and
[avoids common drawbacks](https://nylas.com/blog/packaging-deploying-python/) of ‘from source’ installs,
like needing build tools and direct internet access in production environments.

The Debian packaging metadata in
[debian]({{ cookiecutter.url }}/tree/master/debian)
puts the `{{ cookiecutter.pypi_package }}` Python package and its dependencies as released on PyPI into a DEB package,
using [dh-virtualenv](https://github.com/spotify/dh-virtualenv).
The resulting *omnibus package* is thus easily installed to and removed from a machine,
but is not a ‘normal’ Debian `python-*` package. If you want that, look elsewhere.

To add any plugins or other optional dependencies, add them to ``install_requires`` in ``setup.py`` as usual
– only use versioned dependencies so package builds are reproducible.


## How to build and install the package

You need a build machine with all build dependencies installed, specifically
[dh-virtualenv](https://github.com/spotify/dh-virtualenv) in addition to the normal Debian packaging tools.
You can get it from [this PPA](https://launchpad.net/~spotify-jyrki/+archive/ubuntu/dh-virtualenv),
the [official Ubuntu repositories](http://packages.ubuntu.com/search?keywords=dh-virtualenv),
or [Debian packages](https://packages.debian.org/source/sid/dh-virtualenv).

This code requires and is tested with ``dh-virtualenv`` v1.0
– depending on your platform you might get an older version via the standard packages.
On *Jessie*, install it from ``jessie-backports``.
On *Xenial* you get *v0.11* by default, so you have to build *v1.0* from source.
See the [dh-virtualenv documentation](https://dh-virtualenv.readthedocs.io/en/latest/tutorial.html#step-1-install-dh-virtualenv) for that.

With tooling installed,
the following commands will install a *release* version of `{{ cookiecutter.pypi_package }}` into `/opt/venvs/{{ cookiecutter.pypi_package }}/`,
and place a symlink for the `{{ cookiecutter.pypi_package }}` command into the machine's PATH.

```sh
git clone {{ cookiecutter.url }}.git
cd {{ cookiecutter.repo_name }}/
# or "pip download --no-deps --no-binary :all: {{ cookiecutter.repo_name }}" and unpack the archive

sudo apt-get install build-essential debhelper devscripts equivs

# Extra steps on Jessie
echo "deb http://ftp.debian.org/debian jessie-backports main" \
    | sudo tee /etc/apt/sources.list.d/jessie-backports.list >/dev/null
sudo apt-get update -qq
sudo apt-get install -t jessie-backports cmake dh-virtualenv
# END jessie

sudo mk-build-deps --install debian/control
dpkg-buildpackage -uc -us -b
dpkg-deb -I ../{{ cookiecutter.pypi_package }}_*.deb
```

The resulting package, if all went well, can be found in the parent of your project directory.
You can upload it to a Debian package repository via e.g. `dput`, see
[here](https://github.com/jhermann/artifactory-debian#package-uploading)
for a hassle-free solution that works with *Artifactory* and *Bintray*.

You can also install it directly on the build machine:

```sh
sudo dpkg -i ../{{ cookiecutter.pypi_package }}_*.deb
/usr/bin/{{ cookiecutter.pypi_package }} --version  # ensure it basically works
```

To list the installed version of `{{ cookiecutter.pypi_package }}` and all its dependencies, call this:

```sh
/opt/venvs/{{ cookiecutter.pypi_package }}/bin/pip freeze | less
```


## How to set up a simple service instance

**TODO** Link to packaged project's documentation, and adapt the text below as needed!

After installing the package, …

The package contains a ``systemd`` unit for the service, and starting it is done via ``systemctl``:

```sh
# {{ cookiecutter.pypi_package }}-web requires {{ cookiecutter.pypi_package }}-worker and {{ cookiecutter.pypi_package }}-cron,
# so there is no need to start / enable them separately
sudo systemctl enable {{ cookiecutter.pypi_package }}
sudo systemctl start {{ cookiecutter.pypi_package }}

# This should show the service in state "active (running)"
systemctl status '{{ cookiecutter.pypi_package }}' | grep -B2 Active:
```

The service runs as ``{{ cookiecutter.pypi_package }}.daemon``.
Note that the ``{{ cookiecutter.pypi_package }}`` user is not removed when purging the package,
but the ``/var/{log,opt}/{{ cookiecutter.pypi_package }}`` directories and the configuration are.

After an upgrade, the services restart automatically by default,


## Trouble-Shooting

### 'pkg-resources not found' or similar during virtualenv creation

If you get errors regarding ``pkg-resources`` during the virtualenv creation,
update your build machine's ``pip`` and ``virtualenv``.
The versions on many distros are just too old to handle current infrastructure (especially PyPI).

This is the one exception to “never sudo pip”, so go ahead and do this:

```sh
sudo pip install -U pip virtualenv
```

Then try building the package again.


## Configuration Files

 * ``/etc/default/{{ cookiecutter.pypi_package }}`` – Operational parameters like global log levels.
 * ``/etc/{{ cookiecutter.pypi_package }}/config.yml`` – The service's YAML configuration.
 * ``/etc/cron.d/{{ cookiecutter.pypi_package }}`` – The house-keeping cron job running each day.

 :information_source: Please note that the files in ``/etc/{{ cookiecutter.pypi_package }}``
 are *not* world-readable, since they might contain passwords.


## Data Directories

 * ``/var/log/{{ cookiecutter.pypi_package }}`` – Extra log files (by the cron job).
 * ``/var/opt/{{ cookiecutter.pypi_package }}`` – Data files created during runtime.

You should stick to these locations, because the maintainer scripts have special handling for them.
If you need to relocate, consider using symbolic links to point to the physical location.


## References

### Related Projects

 * [Springerle/debianized-pypi-mold](https://github.com/Springerle/debianized-pypi-mold) – Cookiecutter that was used to create this project.
