"""Console script for evolved5g."""
import sys
import click
from cookiecutter.main import cookiecutter
import os

# @click.command()
# def main(args=None):
#     """Console script for evolved5g."""
#     click.echo(
#         "The console script for Evolved5G, this messages comes from evolved5g.cli.main")
#     click.echo("See click documentation at https://click.palletsprojects.com/")
#     return 0

# Creating Command group


@click.group()
def cli():
    pass


@click.command()
@click.option('-r', '--repeat', type=int, help='times to repeat', default=1)
@click.option('-n', '--name', type=str, help='Name to greet', default='World')
def test(repeat, name):
    """For Testing purposes, TODO Delete"""
    for i in range(repeat):
        click.echo(f'Hello {name}')


@click.command()
def generate():
    """Generate EVOLVED-5G compliant NetApp from template"""
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__), ".."))
    click.echo(__location__)
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter(__location__ + '/cookiecutter_template/')
    # Create project from the cookiecutter-pypackage.git repo template in case we want to do it from Repo later
    # cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')


@click.command()
def connect():
    """Connect repository to CI/CD"""
    # Connect repository to CI/CD TODO
    click.echo("Connecting Repo to CI/CD")


cli.add_command(test)
cli.add_command(generate)
cli.add_command(connect)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
    cli()
