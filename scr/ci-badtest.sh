#!/bin/sh
set +e

if [ -z "${PACKAGE_NAME}" ];           then echo "PACKAGE_NAME is blank"; exit 1; fi
if [ -z "${PYTHON_RUNNER}" ];           then echo "PYTHON_RUNNER is blank"; exit 1; fi
if [ -z "${CI_REPOSITORY_URL}" ];       then echo "CI_REPOSITORY_URL is blank"; exit 1; fi
if [ -z "${CI_COMMIT_REF_NAME}" ];      then echo "CI_COMMIT_REF_NAME is blank"; exit 1; fi
if [ -z "${PIP_SERVER_INTRANET_URL}" ]; then echo "PIP_SERVER_INTRANET_URL is blank"; exit 1; fi
if [ -z "${PIP_SERVER_INTRANET_HOST}" ];then echo "PIP_SERVER_INTRANET_HOST is blank"; exit 1; fi

for SUITE_REL_PATH in test/bad/*/ ; do
    if [ -f ${SUITE_REL_PATH}/args ]; then
        ARGS=$(cat ${SUITE_REL_PATH}/args)
    else
        ARGS=
    fi

    echo '-----------------------------------------------------------------'
    echo " Suite:      ${SUITE_REL_PATH}"
    echo " Search for: $(cat ${SUITE_REL_PATH}/search)"
    echo " Arguments:  ${ARGS}"
    echo '-----------------------------------------------------------------'

    docker run -t --rm ${PYTHON_RUNNER} sh -c "
        git clone ${CI_REPOSITORY_URL} --branch ${CI_COMMIT_REF_NAME} --single-branch /tmp/project;
        pip3 install -q --extra-index-url ${PIP_SERVER_INTRANET_URL} --trusted-host ${PIP_SERVER_INTRANET_HOST} /tmp/project;
        cd /tmp/project/${SUITE_REL_PATH};
        python3 -m ${PACKAGE_NAME} ${ARGS}" > /tmp/volcano.log

    cat /tmp/volcano.log | grep -qFf ${SUITE_REL_PATH}/search

    if [ $? -ne 0 ] ; then
        echo " !!! Test failed !!!"
        cat /tmp/volcano.log
        exit 1
    else
        echo 'OK'
    fi
done
