import click

from dzmt.cli.commands.build import build
from dzmt.cli.commands.describe import describe
from dzmt.cli.commands.generate import generate
from dzmt.cli.commands.init import init
from dzmt.cli.commands.launch import launch


@click.group()
def cli(): ...


cli.add_command(generate)
cli.add_command(init)
cli.add_command(describe)
cli.add_command(build)
cli.add_command(launch)
