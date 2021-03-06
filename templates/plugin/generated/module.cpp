{% import "qface/qtcpp.j2" as cpp %}
{{ cpp.autogenerated() }}
#include "{{module|identifier}}_gen.h"


{# ***************************************************************** #}
{# *** ENUMERATIONS                                              *** #}
{# ***************************************************************** #}
{% for enum in module.enums %}
{% set class = '{0}'.format(enum) %}
// ********************************************************************
// Enumeration {{class}}
// ********************************************************************

{{class}}::{{class}}Enum {{class}}::toEnum(quint8 v, bool *ok)
{
    if (ok) {
        *ok = true;
    }
    switch (v) {
{% for member in enum.members %}
        case {{member.value}}: return {{class}}::{{member.name}};
{% endfor %}
        default:
            if (ok) {
                *ok = false;
            }
            return {{enum|qt.defaultValue}};
    }
}
{% endfor %}

{# ***************************************************************** #}
{# *** STRUCTS                                                   *** #}
{# ***************************************************************** #}

{% for struct in module.structs %}
{% set class = '{0}'.format(struct) %}
//
// Struct {{class}}
//

{{class}}::{{class}}()
{% for field in struct.fields %}
{% if loop.first %}    :{% else %}    ,{% endif %} m_{{field}}({{field|qt.defaultValue}})
{% endfor %}
{
}

{% for field in struct.fields %}
{{cpp.property_setter_impl(class, field, notifiable=False)}}

{{cpp.property_getter_impl(class, field)}}
{% endfor %}

bool {{class}}::operator==(const {{class}} &other) const
{
    return (
{% for field in struct.fields %}
        {{field}}() == other.{{field}}(){% if not loop.last %} &&
{% endif %}
{% endfor %}

    );
}

bool {{class}}::operator!=(const {{class}} &other) const
{
    return !(*this == other);
}

QDataStream &operator<<(QDataStream &stream, const {{class}} &obj)
{
    {% for field in struct.fields %}
    stream << obj.{{field}}();
    {% endfor %}

    return stream;
}

QDataStream &operator>>(QDataStream &stream, {{class}} &obj)
{
    {% for field in struct.fields %}
    {{field|qt.returnType}} {{field}}Value;
    stream >> {{field}}Value;
    obj.set{{field|upperfirst}}({{field}}Value);

    {% endfor %}
    return stream;
}

//
// {{class}} Factory
//

{{class}} {{class}}Factory::create()
{
    return {{class}}();
}

{% endfor %}


{# ***************************************************************** #}
{# *** INTERFACES                                                *** #}
{# ***************************************************************** #}
{% for interface in module.interfaces %}
{% set class = '{0}Base'.format(interface) %}

//
// Interface {{class}}
//


{% if 'item' in interface.tags %}
{{class}}::{{class}}(QQuickItem *parent)
    : QQuickItem(parent)
{% else %}
{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{% endif %}
{
}

{{class}}::~{{class}}()
{
}

{% if 'factory' in interface.tags %}
{% set class = '{0}Factory'.format(interface) %}
{% set base = '{0}Base'.format(interface) %}

//
// Factory for {{interface}}
//

class {{class}}Loader
{
public:
    {{class}} {{class|lowerfirst}};
};

Q_GLOBAL_STATIC({{class}}Loader, {{class|lowerfirst}}Loader)


{{class}}::{{class}}()
{
}

{{class}} *{{class}}::instance()
{
    return &{{class|lowerfirst}}Loader->{{class|lowerfirst}};
}

{{base}} *{{class}}::create(const QString &id, QObject *parent)
{
    auto creatorFunc = m_creatorFuncs.value(id);
    if (!creatorFunc) {
        return nullptr;
    }
    return (*creatorFunc)(parent);
}

template<typename T>
void {{class}}::registerType(const QString &id)
{
    qInfo() << "register connection type: " << id;
    m_creatorFuncs[id] = [](QObject *parent) -> {{base}} * {
        return new T(parent);
    };
}
{% endif %}

{% endfor %}