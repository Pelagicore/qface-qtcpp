{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(struct) %}
{% import "qface/qtcpp.j2" as cpp %}
{{ cpp.autogenerated() }}

#pragma once

#include <QtCore>


class {{class}}Data;

class {{class}}
{
    Q_GADGET
{% for field in struct.fields %}
    Q_PROPERTY({{field|returnType}} {{field}} READ {{field}} WRITE set{{field|upperfirst}})
{% endfor %}

public:
    {{class}}();
    {{class}}(const {{class}} &other);
    ~{{class}}();

    static void registerQmlTypes(const QString& uri, int majorVersion=1, int minorVersion=0);

    Q_INVOKABLE {{class}} clone();

    bool operator==(const {{class}} &other) const;
    {{class}} &operator=(const {{class}} &other);

{% for field in struct.fields %}
    void set{{field|upperfirst}}({{field|parameterType}});
    {{field|returnType}} {{field}}() const;

{% endfor %}


private:
    QExplicitlySharedDataPointer <{{class}}Data> d;
};


