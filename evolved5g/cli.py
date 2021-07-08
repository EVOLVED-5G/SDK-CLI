"""Console script for evolved5g."""
import click
from cookiecutter.main import cookiecutter
import os

def cookiecutter_generate(location, no_input=False,**kwargs):
    extra_context = kwargs['extra_context']
    cookiecutter(location, no_input=no_input, extra_context=extra_context)

@click.command()
def main(args=None):
    """Console script for evolved5g."""
    click.echo(
        "The console script for Evolved5G, this messages comes from evolved5g.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

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
@click.option('--no-input', type=bool, is_flag=True,
              help='Enables no prompt from the CLI during template generation', default=False)
@click.option('-r', '--repo-name', type=str, help='Enter Repository name')
@click.option('-p', '--package-name', type=str, help='Enter package name')
def generate(no_input, repo_name, package_name):
    """Generate EVOLVED-5G compliant NetApp from template"""
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__), ".."))
    location = (__location__ + '/cookiecutter_template/')
    # click.echo(__location__)  # -- for debug
    extra = {}
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter_generate(location, no_input=no_input, extra_context=extra)
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
