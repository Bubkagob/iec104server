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

PROJECT=$(basename $PWD)
# перебор по маске не подходит, потому что порядок тестов не должен быть алфавитным
TESTS='dev-unittest.sh dev-badtest.sh dev-systest.sh'

cd scr

for TEST in ${TESTS} ; do
    if [[ -f ${TEST} ]] ; then
        echo ''
        echo ''
        echo ">>>>>>>>>>>>>  ${PROJECT} / ${TEST}"
        echo ''
        echo ''

        /bin/bash ${TEST}
    fi
done
