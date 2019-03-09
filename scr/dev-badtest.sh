#!/bin/bash
set +e  # смысл теста в проверке вылета программы, у нашей программы всегда будет ExitCode != 0

cd ..   # все операции - от корня проекта

#
# CONFIG
#
SUITE=$1
PACKAGES=$PWD/../packages       # docker обязывает все пути указывать как абсолютные при монтировании volume
PROJECT_NAME=$(basename $PWD)           # volcano-abc
PROJECT_PACKAGE=${PROJECT_NAME//-/.}    # volcano.abc
PYTHON_RUNNER=${PROJECT_NAME}-ci-py-lux
LOG_FILE=$(mktemp)

echo ''
echo '----------------------------------------------------------------'
echo ' Task:         BAD TESTS'
echo " Package name: ${PROJECT_PACKAGE}  (autodetect)"
echo " Log file:     ${LOG_FILE}"
echo " Packages:     ${PACKAGES}"
echo '----------------------------------------------------------------'
echo ''


echo 'Renew dockers...'
docker build -t ${PYTHON_RUNNER} dockers/${PYTHON_RUNNER}

for SUITE_PATH in test/bad/*/ ; do
    SUITE_NAME=$(basename ${SUITE_PATH})

    if [ -z "${SUITE}" ] || [ "${SUITE}" = "${SUITE_NAME}" ] ; then
        ARGS=
        if [ -f ${SUITE_PATH}/args ]; then
            ARGS=$(cat ${SUITE_PATH}/args)
        fi

        echo '-----------------------------------------------------------------'
        echo " Suite:      ${SUITE_NAME}"
        echo " Search for: $(cat ${SUITE_PATH}/search)"
        echo " Arguments:  ${ARGS}"
        echo '-----------------------------------------------------------------'

        docker run -it --rm -v $PWD:/project:ro -v ${PACKAGES}:/packages:ro -w /project/${SUITE_PATH} ${PYTHON_RUNNER} sh -c "
            pip3 install -q --find-links=/packages /project;
            python3 -m ${PROJECT_PACKAGE} ${ARGS}" > ${LOG_FILE}

        cat ${LOG_FILE} | grep -qFf ${SUITE_PATH}/search

        if [ $? -ne 0 ] ; then
            echo ''
            echo " !!! Test failed !!!"
            echo ''
            cat ${LOG_FILE}
            exit 1
        else
            echo 'OK'
        fi
    else
        echo "Skip -- ${SUITE_NAME}"
    fi
done

echo ''
echo 'SUCCESS'
echo ''
