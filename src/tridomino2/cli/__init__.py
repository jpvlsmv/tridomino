# SPDX-FileCopyrightText: 2024-present Joe Moore <joe.moore@siemens.com>
#
# SPDX-License-Identifier: MIT
import click

from tridomino2.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="tridomino2")
def tridomino2():
    click.echo("Hello world!")
