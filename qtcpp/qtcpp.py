#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from path import Path

from qface.generator import FileSystem, RuleGenerator
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
    system = FileSystem.parse(src)
    generator = RuleGenerator(search_path=here/'templates', destination=dst)
    generator.filters.update(Filters.get_filters())
    generator.filters.update({'parse_doc': parse_doc})
    generator.process_rules(here/'qtcpp.yaml', system)


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
