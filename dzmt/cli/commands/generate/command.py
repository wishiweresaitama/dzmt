import click

from .subcommands.modification import modification


@click.group()
def generate():
    pass


generate.add_command(modification)
