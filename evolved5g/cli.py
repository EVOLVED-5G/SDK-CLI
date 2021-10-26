"""Console script for evolved5g."""
import click
from .utils import cookiecutter_generate
from evolved5g.cli_helper import CLI_helper


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """Console interface for EVOLVED-5G H2020 project"""
    ctx.ensure_object(dict)
    ctx.obj["helper"] = CLI_helper()


@cli.command()
@click.option('--no-input', type=bool, is_flag=True,
              help='Enables no prompt from the CLI during template generation', default=False)
@click.option('-r', '--repo-name', type=str, help='Enter Repository name')
@click.option('-p', '--package-name', type=str, help='Enter package name')
@click.option('-t', '--template', type=str, help="Provide template location for custom package")
@click.pass_context
def generate(ctx,no_input, repo_name, package_name, template):
    """Generate EVOLVED-5G compliant NetApp from template"""
    ctx.obj["helper"].generate(no_input, repo_name, package_name, template) 

@cli.command()
def run_pipeline():
    """
    """
    cli_helper = CLI_helper()
    cli_helper.run_pipeline() 

@cli.command()
def check_pipeline():
    """
    """
    cli_helper = CLI_helper()
    cli_helper.check_pipeline() 
