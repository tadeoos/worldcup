#!/usr/bin/env python
import sys
import click

from api_parser import WorldCupData


@click.group(invoke_without_command=True)
def cli():
    """
    CLI tool for being up to date with 2018 World Cup
    """


@cli.command('nearest', short_help='Show nearest match info')
def nearest():
    wc_data = WorldCupData()
    click.secho(wc_data.match_as_str(wc_data.get_nearest_match()), bold=1, fg="blue")


@cli.command('groups', short_help='Show group info')
@click.argument('group_names', nargs=-1)
@click.option('-a', '--all-groups', default=False, help="Show info for all groups")
@click.option('--table/--no-table', default=True, help="Show group table")
def groups(group_names, all_groups, table):
    possible_groups = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')

    def check_args():
        for g in group_names:
            if g.lower() not in possible_groups:
                click.secho("There is no group {}".format(g.upper(), fg="red", err=True))
                sys.exit(1)

    check_args()
    if all_groups or not len(group_names):
        group_names = possible_groups
    wc_data = WorldCupData()
    if table:
        for g in group_names:
            group = g.lower()
            click.secho(wc_data.group_table_as_str(group), fg="green")
            click.echo()


if __name__ == '__main__':
    cli()
