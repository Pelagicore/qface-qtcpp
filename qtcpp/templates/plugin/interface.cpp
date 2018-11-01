{# Copyright (c) Pelagicore AB 2016 #}
{% import "qface/qtcpp.j2" as cpp %}
{{ cpp.preserved() }}
{% set class = '{0}'.format(interface) %}

#include "{{class|lower}}.h"

#include <QtQml>

/*!
   \qmltype {{interface}}
   \inqmlmodule {{module}}
{% with doc = interface.comment|parse_doc %}
   \brief {{doc.brief|join(" ")}}

   {{doc.description|join("\n   ")}}
{% endwith %}
*/

{{interface.comment}}
{% if 'item' in interface.tags %}
    {{class}}::{{class}}(QQuickItem *parent)
{% else %}
    {{class}}::{{class}}(QObject *parent)
{% endif %}
    : {{interface}}Base(parent)
{
}

{{class}}::~{{class}}()
{
}

{% for property in interface.properties %}
{{ cpp.property_setter_impl(class, property) }}

{{ cpp.property_getter_impl(class, property) }}
{% endfor %}

{%- for operation in interface.operations %}
{{ cpp.operation_impl(class, operation) }}
{% endfor %}

