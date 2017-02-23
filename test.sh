#! /bin/bash
#
# Run integration test suite.
#
set -e


fail() { # fail with error message on stderr and exit code 1
    echo >&2 "ERROR:" "$@"
    exit 1
}

ensure_tool() {
    local tool="${1:?You must provide a tool name}"
    command which "$tool" >/dev/null 2>&1 || fail "'$tool' not found, please install it"
}

deactivate 2>/dev/null || :
rootdir=$(cd $(dirname "$0") && pwd)

# Fail fast for some obvious errors
ensure_tool "dh_virtualenv"
ensure_tool "cookiecutter"
python -c "assert (1, 0) <= tuple(int(i) for i in '$(dh_virtualenv --version | cut -f2 -d' ')'.split('.')), 'You need dh_virtualenv 1.0+'"
test -f "$rootdir/README.md" || fail 'Use a full git clone!'

# Create sample project (unattended)
prjname="debianized-realms-wiki"
test ! -d "$prjname" || rm -rf "$prjname"
#git clone "https://github.com/borntyping/cookiecutter-pypackage-minimal.git"
#sed -r -i -e "s/cookiecutter.pypackage.minimal/$prjname/" "$workdir/cookiecutter-pypackage-minimal/cookiecutter.json"
cookiecutter --no-input "$PWD"
echo

cd "$prjname"
dch -r ""

# Build the package
dpkg-buildpackage -uc -us -b
cd ..

# Check the package
deb=$(ls -1 ${prjname#debianized-}*.deb)
while read i; do
    dpkg-deb -c $deb | egrep "$i" >/dev/null || fail "DPKG content misses '$i'"
done <<EOF
/opt/venvs/${prjname#debianized-}/bin/python
EOF

while read i; do
    dpkg-deb -I $deb | egrep "$i" >/dev/null || fail "DPKG metadata misses '$i'"
done <<EOF
Package: ${prjname#debianized-}
Homepage: https://github.com/[^/]+/${prjname}
Description: ${prjname#debianized-} packaged into a virtualenv.
EOF


# Yay!
echo
echo "*** ALL OK ***"
# end of integration test
