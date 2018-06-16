# - *- coding: utf- 8 - *-
from __future__ import print_function, absolute_import

from click.testing import CliRunner
from worldcup18.worldcup import cli


def test_worldcup_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert result.output == """Usage: cli [OPTIONS] COMMAND [ARGS]...

  CLI tool for being up to date with 2018 World Cup

Options:
  --help  Show this message and exit.

Commands:
  groups    Show group info
  knockout  Show info about knockout phase
  next      Show nearest match info
  stats     Show info about specific country
"""


def test_worldcup_cli_nearest():
    runner = CliRunner()
    result = runner.invoke(cli, ['next'])
    assert result.exit_code == 0


def test_worldcup_cli_group():
    runner = CliRunner()
    result = runner.invoke(cli, ['groups', 'a'])
    assert result.exit_code == 0
