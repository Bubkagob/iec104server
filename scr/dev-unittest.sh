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
PROJECT_NAME=$(basename $PWD)           # volcano-abc
PACKAGES=$(realpath $PWD/../packages)   # docker обязывает все пути указывать как абсолютные при монтировании volume

echo ''
echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
echo " Task:     UNIT-TEST"
echo " Project:  ${PROJECT_NAME}"
echo " Packages: ${PACKAGES}"
echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
echo ''


echo 'Activate env...'
rm -fr env
python3 -m venv env
. env/bin/activate

echo 'Install...'
pip3 install -q --find-links=${PACKAGES} .
pip3 install -q -r requirements_unittest.txt

echo 'Run tests...'
coverage run --source volcano -m unittest discover test/unit 'test_*.py'
coverage report
