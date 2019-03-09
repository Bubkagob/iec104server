# PyVolcano 60870-5-104 Server

[![N|Solid](https://avatars2.githubusercontent.com/u/25686380?s=200&v=4)](https://nodesource.com/products/nsolid)

[![pipeline status](https://gitlab.com/schneiderelectricru/pyvolcano/volcano-iec104srv/badges/dev/pipeline.svg)](gitlab.com/schneiderelectricru/pyvolcano/volcano-iec104srv/commits/dev)
[![coverage](https://gitlab.com/schneiderelectricru/pyvolcano/volcano-iec104srv/badges/dev/coverage.svg?style=flat-square)](gitlab.com/schneiderelectricru/pyvolcano/volcano-iec104srv/commits/dev)
# Порядок установки

  - Обновить зависимость peavey-client
  - проверить/собрать необходимую c-библиотеку
  - установить python-зависимости

Проверить конфигурацию 'config.xml'.

### Requirements

сервер использует след. пакеты:

* [lib60870] - C-реализация библиотеки 60870 от mz-Automation
* [Twisted] - an event-driven networking engine.
* [LXML] - the most feature-rich and easy-to-use library for processing XML.

Пакеты и их версии доступны в файле requirements.txt.

### Installation

py60870 server требует наличие iec60870 в системе.
Установка библиотеки описывается в проекте lib60870.


Обновление зависимостей
```sh
$ git clone "project" && cd "project"
$ git submodule update --init --recursive
```

Необходимые модули Python
```sh
$ pip install -r requirements.txt
```

Запуск приложения:
```sh
$ python -m volcano.srv104 --config $YOURCONFIG
```


### Конфигурация сервера

Файл конфигурации для демонстрации "config.xml".


### Todos

 - Дописать README
 - Добавить новые возможности

License
----

MIT


[//]: # ( )
   [lib60870]: <https://github.com/mz-automation/lib60870>
   [Twisted]: <https://twistedmatrix.com/trac/>
   [LXML]: <https://lxml.de/>
