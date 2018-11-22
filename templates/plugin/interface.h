{# Copyright (c) Pelagicore AB 2016 #}
{% import "qface/qtcpp.j2" as cpp %}
{{ cpp.preserved() }}
{% set class = '{0}'.format(interface) %}

#pragma once

#include <QtCore>
{% if 'item' in interface.tags %}
#include <QtQuick>
{% endif %}
#include "generated/{{module|identifier}}_gen.h"

class {{class}} : public {{interface}}Base
{
    Q_OBJECT
public:
{% if 'item' in interface.tags %}
    explicit {{class}}(QQuickItem *parent = nullptr);
{% else %}
    explicit {{class}}(QObject *parent = nullptr);
{% endif %}
    virtual ~{{class}}();
public Q_SLOTS:
{% for operation in interface.operations %}
    {{ cpp.operation_decl(operation) }}
{% endfor %}
public:
{% for property in interface.properties %}
    {{ cpp.property_setter_decl(property) }}
{% endfor %}
public:
{% for property in interface.properties %}
    {{cpp.property_getter_decl(property) }}
{% endfor %}
private:
{% for property in interface.properties %}
    {{ cpp.property_member_decl(property) }}
{% endfor %}
};
