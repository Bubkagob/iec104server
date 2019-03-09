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
SUITE=$1
PROJECT_NAME=$(basename $PWD)           # volcano-abc
PROJECT_PACKAGE=${PROJECT_NAME//-/.}    # volcano.abc
export PYTHON_RUNNER=${PROJECT_NAME}-ci-py-lux
export PACKAGES=$(realpath $PWD/../packages)   # docker обязывает все пути указывать как абсолютные при монтировании volume

echo ''
echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
echo " Task:     SYS-TEST"
echo " Project:  ${PROJECT_NAME}"
echo " Package:  ${PROJECT_PACKAGE}  (autodetected)"
echo " Packages: ${PACKAGES}"
echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
echo ''

echo 'Renew dockers'
docker build -t ${PYTHON_RUNNER} dockers/${PYTHON_RUNNER}

for SUITE_REL_PATH in test/sys/*/ ; do
    SUITE_NAME=$(basename ${SUITE_REL_PATH})

    if [ -z "$SUITE" ] || [ "$SUITE" = "$SUITE_NAME" ] ; then
        echo '-----------------------------------------------------------------'
        echo " SUITE: ${SUITE_NAME}"
        echo '-----------------------------------------------------------------'

        cd ${SUITE_REL_PATH}
        
        if [[ -f docker-compose.yml ]] ; then
            docker-compose -f ../docker-compose-local.yml -f docker-compose.yml up --exit-code-from test --abort-on-container-exit --force-recreate  --remove-orphans
        else
            docker-compose -f ../docker-compose-local.yml up --exit-code-from test --abort-on-container-exit --force-recreate  --remove-orphans
        fi

        cd ../../..
    else
        echo "Skip -- $SUITE_NAME"
    fi
done

echo ''
echo ''
echo 'SUCCESS'
echo ''
echo ''
