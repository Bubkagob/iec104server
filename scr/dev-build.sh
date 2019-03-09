#!/bin/bash
set -e

# CWD
if [[ "$(basename $PWD)" == "scr" ]] ; then
    cd ..
fi

if [[ ! -f ".gitlab-ci.yml" ]] ; then
    echo "Incorrect cwd. Use project root or ./scr subfolder" >&2
    exit 1
fi

#
# CONFIG
#
PACKAGES=../packages

echo 'Activate env...'
rm -fr env
python3 -m venv env
. env/bin/activate

pip3 install -q --upgrade wheel setuptools twine

python3 setup.py sdist bdist_wheel

if [ -d "${PACKAGES}" ]; then
    echo "Copy distribution package to ${PACKAGES}"
    cp dist/* ${PACKAGES}
else
    echo "Package folder ${PACKAGES} not found => skip copy"
fi
