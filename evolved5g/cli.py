"""Console script for evolved5g."""
import click
from .utils import cookiecutter_generate
import os


@click.command()
def main(args=None):
    """Console script for evolved5g."""
    click.echo(
        "The console script for Evolved5G, this messages comes from evolved5g.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

# Creating Command group


@click.group()
@click.version_option()
def cli():
    """Console interface for EVOLVED-5G H2020 project"""
    pass


@click.command()
@click.option('--no-input', type=bool, is_flag=True,
              help='Enables no prompt from the CLI during template generation', default=False)
@click.option('-r', '--repo-name', type=str, help='Enter Repository name')
@click.option('-p', '--package-name', type=str, help='Enter package name')
@click.option('-t', '--template', type=str, help="Provide template location for custom package")
def generate(no_input, repo_name, package_name, template):
    """Generate EVOLVED-5G compliant NetApp from template"""
    # __location__ = os.path.realpath(os.path.join(
    #    os.getcwd(), os.path.dirname(__file__), ".."))
    # location = (__location__ + '/cookiecutter_template/')
    # click.echo(__location__)  # -- for debug
    extra = {}
    if repo_name:
        extra['repoName'] = repo_name
    if package_name:
        extra['packageName'] = package_name
    if template:
        cookiecutter_generate(template,no_input=no_input,extra_context=extra)
        return
    location = "gh:EVOLVED-5G/template" # location to github package
    # Create project from the github package template
    cookiecutter_generate(location, no_input=no_input, extra_context=extra)


# @click.command()
# def connect():
#     """Connect repository to CI/CD"""
#     # Connect repository to CI/CD TODO
#     click.echo("Connecting Repo to CI/CD")

# @click.command()
# @click.option('-r', '--repeat', type=int, help='times to repeat', default=1)
# @click.option('-n', '--name', type=str, help='Name to greet', default='World')
# def test(repeat, name):
#     """For Testing purposes, TODO Delete"""
#     for i in range(repeat):
#         click.echo(f'Hello {name}. This is a test')

#cli.add_command(test)
# cli.add_command(connect)

cli.add_command(generate)