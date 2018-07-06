#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=
# mkvenv: no-deps
""" Debian packaging for the {{ cookiecutter.pypi_package }} package.

    | Copyright ©  {{ cookiecutter.year }}, {{ cookiecutter.full_name }}
    | See LICENSE for details.

    This puts the ``{{ cookiecutter.pypi_package }}`` Python package and its dependencies as released
    on PyPI into a DEB package, using ``dh-virtualenv``.
    The resulting *omnibus package* is thus easily installed to and removed
    from a machine, but is not a ‘normal’ Debian ``python-*`` package.
    Services are controlled by ``systemd`` units.

    See the `GitHub README`_ for more.

    .. _`GitHub README`: {{ cookiecutter.url }}
"""
import os
import re
import sys
import json
import rfc822
import textwrap
import subprocess

try:
    from setuptools import setup
except ImportError as exc:
    raise RuntimeError("setuptools is missing ({1})".format(exc))


# get external project data (and map Debian version semantics to PEP440)
pkg_version = subprocess.check_output("parsechangelog | grep ^Version:", shell=True)
upstream_version, maintainer_version = pkg_version.split()[1].split('~', 1)[0].split('-', 1)
maintainer_version = maintainer_version.replace('~~rc', 'rc').replace('~~dev', '.dev')
pypi_version = upstream_version + '.' + maintainer_version

with open('debian/control') as control_file:
    deb_source = rfc822.Message(control_file)
    deb_binary = rfc822.Message(control_file)

maintainer, email = re.match(r'(.+) <([^>]+)>', deb_source['Maintainer']).groups()
desc, long_desc = deb_binary['Description'].split('.', 1)
desc, pypi_desc = __doc__.split('\n', 1)
long_desc = textwrap.dedent(pypi_desc) + textwrap.dedent(long_desc).replace('\n.\n', '\n\n')
dev_status = 'Development Status :: 5 - Production/Stable'

# Check for pre-release versions like "1.2-3~~rc1~distro"
if '~~rc' in pkg_version or '~~dev' in pkg_version:
    rc_tag = pkg_version.split('~')[-1].split('~')[0].split('-')[0]
    upstream_version += rc_tag
    pypi_version += rc_tag
    dev_status = 'Development Status :: 4 - Beta'

# build setuptools metadata
project = dict(
    name='debianized-' + deb_source['Source'],
    version=pypi_version,
    author=maintainer,
    author_email=email,
    license='BSD 3-clause',
    description=desc.strip(),
    long_description=textwrap.dedent(long_desc).strip(),
    url=deb_source['Homepage'],
    classifiers=[
        # Details at http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 3 - Alpha',
        #dev_status,
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='{{ cookiecutter.pypi_package }} deployment debian-packages dh-virtualenv devops omnibus-packages'.split(),
    install_requires=[
        # core
        '{{ cookiecutter.pypi_package }}==' + upstream_version,

        # extensions
        #'…==1.2.3',
    ],
    packages=[],
)


# 'main'
__all__ = ['project']
if __name__ == '__main__':
    if '--metadata' in sys.argv[:2]:
        json.dump(project, sys.stdout, default=repr, indent=4, sort_keys=True)
        sys.stdout.write('\n')
    elif '--tag' in sys.argv[:2]:
        subprocess.call("git tag -a 'v{version}' -m 'Release v{version}'"
                        .format(version=pypi_version), shell=True)
    else:
        setup(**project)
