#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from path import Path

from qface.generator import FileSystem, Generator
from qface.helper.qtcpp import Filters
from qface.helper.doc import parse_doc
from qface.watch import monitor


here = Path(__file__).dirname()

logging.basicConfig()
with open('log.yaml', 'r') as fp:
    logging.config.dictConfig(yaml.load(fp))
log = logging.getLogger(__name__)


def run(src, dst):
    log.debug('run {0} {1}'.format(src, dst))
    project = Path(dst).name
    system = FileSystem.parse(src)
    generator = Generator(search_path=here / 'templates')
    generator.register_filter('returnType', Filters.returnType)
    generator.register_filter('parameterType', Filters.parameterType)
    generator.register_filter('defaultValue', Filters.defaultValue)
    generator.register_filter('parameters', Filters.parameters)
    generator.register_filter('parse_doc', parse_doc)
    generator.register_filter('upper_first', Filters.upper_first)
    generator.register_filter('identifier', Filters.identifier)
    generator.register_filter('path', Filters.path)
    ctx = {
        'dst': dst,
        'system': system,
        'project': project
    }

    dst = generator.apply('{{dst}}', ctx)
    generator.destination = dst
    generator.write('{{project}}.pro', 'project.pro', ctx)
    generator.write('.qmake.conf', 'qmake.conf', ctx)
    generator.write('CMakeLists.txt', 'CMakeLists.txt', ctx)
    for module in system.modules:
        log.debug('generate code for module %s', module)
        ctx.update({'module': module})
        dst = generator.apply('{{dst}}/{{module|identifier}}', ctx)
        generator.destination = dst
        generator.write('{{module|identifier}}.pro', 'plugin/plugin.pro', ctx, preserve=True)
        generator.write('CMakeLists.txt', 'plugin/CMakeLists.txt', ctx)
        generator.write('plugin.cpp', 'plugin/plugin.cpp', ctx, preserve=True)
        generator.write('plugin.h', 'plugin/plugin.h', ctx, preserve=True)
        generator.write('qmldir', 'plugin/qmldir', ctx, preserve=True)
        generator.write('generated/generated.pri', 'plugin/generated/generated.pri', ctx)
        generator.write('generated/{{module.module_name|lower}}module.h', 'plugin/generated/module.h', ctx)
        generator.write('generated/{{module.module_name|lower}}module.cpp', 'plugin/generated/module.cpp', ctx)
        generator.write('generated/variantmodel.h', 'plugin/generated/variantmodel.h', ctx)
        generator.write('generated/variantmodel.cpp', 'plugin/generated/variantmodel.cpp', ctx)
        generator.write('docs/plugin.qdocconf', 'plugin/docs/plugin.qdocconf', ctx)
        generator.write('docs/plugin-project.qdocconf', 'plugin/docs/plugin-project.qdocconf', ctx)
        generator.write('docs/docs.pri', 'plugin/docs/docs.pri', ctx)
        for interface in module.interfaces:
            log.debug('generate code for interface %s', interface)
            ctx.update({'interface': interface})
            generator.write('{{interface|lower}}.h', 'plugin/interface.h', ctx, preserve=True)
            generator.write('{{interface|lower}}.cpp', 'plugin/interface.cpp', ctx, preserve=True)
            generator.write('generated/abstract{{interface|lower}}.h', 'plugin/generated/abstractinterface.h', ctx)
            generator.write('generated/abstract{{interface|lower}}.cpp', 'plugin/generated/abstractinterface.cpp', ctx)
        for struct in module.structs:
            log.debug('generate code for struct %s', struct)
            ctx.update({'struct': struct})
            generator.write('generated/{{struct|lower}}.h', 'plugin/generated/struct.h', ctx)
            generator.write('generated/{{struct|lower}}.cpp', 'plugin/generated/struct.cpp', ctx)
            generator.write('generated/{{struct|lower}}model.h', 'plugin/generated/structmodel.h', ctx)
            generator.write('generated/{{struct|lower}}model.cpp', 'plugin/generated/structmodel.cpp', ctx)


@click.command()
@click.option('--reload/--no-reload', default=False)
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=True))
def app(src, dst, reload):
    """Takes several files or directories as src and generates the code
    in the given dst directory."""
    if reload:
        script = Path(__file__).abspath()
        monitor(script, src, dst)
    else:
        run(src, dst)


if __name__ == '__main__':
    app()
