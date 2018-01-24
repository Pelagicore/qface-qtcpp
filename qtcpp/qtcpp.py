#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import sys
import logging
import click
from path import Path
from qface.generator import FileSystem, RuleGenerator
from qface.helper.qtcpp import Filters
from qface.helper.doc import parse_doc
from qface.watch import monitor
from qface.contrib.logging import setup_log


here = Path(__file__).dirname()


setup_log(path=here / '../logging.yml')

log = logging.getLogger(__name__)


def run(src, dst):
    log.debug('run {0} {1}'.format(src, dst))
    system = FileSystem.parse(src)
    generator = RuleGenerator(search_path=here / 'templates', destination=dst)
    generator.filters.update(Filters.get_filters())
    generator.filters.update({'parse_doc': parse_doc})
    generator.process_rules(here / 'qtcpp.yaml', system)


@click.command()
@click.option('--reload/--no-reload', default=False)
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=False, file_okay=False))
def app(src, dst, reload):
    """Takes several files or directories as src and generates the code
    in the given dst directory."""
    if reload:
        argv = sys.argv.copy()
        argv.remove('--reload')
        monitor(here, src, dst, argv)
    else:
        run(src, dst)


if __name__ == '__main__':
    app()
