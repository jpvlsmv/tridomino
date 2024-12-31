# SPDX-FileCopyrightText: 2024-present Joe Moore <joe.moore@siemens.com>
#
# SPDX-License-Identifier: MIT
import click

from tridomino2.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="tridomino2")
def tridomino2():
    pass


@tridomino2.command()
def demo_rot():
    from tridomino2.demo import demo_rot as d

    d()


@tridomino2.command()
def demo_characterize():
    from tridomino2.demo import demo_characterize as d

    d()


@tridomino2.command()
def work():
    from tridomino2.work import main as d

    d()


@tridomino2.command()
def search():
    from tridomino2.search import main as do_search

    do_search()
