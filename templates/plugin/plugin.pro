{# Copyright (c) Pelagicore AB 2016 #}
{% import "qface/qtcpp.j2" as cpp %}
{{ cpp.preserved(prefix="##")}}

TEMPLATE = lib
QT += qml quick
CONFIG += qt plugin c++11
TARGET = $$qtLibraryTarget({{module|identifier}})

uri = {{module}}


{% for interface in module.interfaces %}
HEADERS += {{interface|lower}}.h
SOURCES += {{interface|lower}}.cpp

{% endfor %}

HEADERS += plugin.h
SOURCES += plugin.cpp


include( generated/generated.pri )
include( docs/docs.pri )

DISTFILES = qmldir

!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    copy_qmldir.target = $$OUT_PWD/qmldir
    copy_qmldir.depends = $$_PRO_FILE_PWD_/qmldir
    copy_qmldir.commands = $(COPY_FILE) \"$$replace(copy_qmldir.depends, /, $$QMAKE_DIR_SEP)\" \"$$replace(copy_qmldir.target, /, $$QMAKE_DIR_SEP)\"
    QMAKE_EXTRA_TARGETS += copy_qmldir
    PRE_TARGETDEPS += $$copy_qmldir.target
}

qmldir.files = qmldir
unix {
    installPath = $$[QT_INSTALL_QML]/$$replace(uri, \\., /)
    qmldir.path = $$installPath
    target.path = $$installPath
    INSTALLS += target qmldir
}
