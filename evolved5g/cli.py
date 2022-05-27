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
# @click.option('--no-input', type=bool, is_flag=True,
#               help='Enables no prompt from the CLI during template generation', default=False)
# @click.option('--directory', type=str, help='Directory within repo that holds cookiecutter.json file for advanced repositories  with multi templates in it', default=False)
@click.option('-r', '--repo-name', type=str, help='Enter Repository name')
@click.option('-p', '--package-name', type=str, help='Enter package name')
@click.option('-t', '--template', type=str, help="Provide template location for custom package")
@click.pass_context
def generate(ctx, repo_name, package_name, template):
    """Generate EVOLVED-5G compliant NetApp from template"""
    ctx.obj["helper"].generate(repo_name, package_name, template) 

@cli.command()
@click.option('--mode',type=click.Choice(['build', 'deploy','destroy'], case_sensitive=False))
@click.option('--repo',type=str, help='Enter repo name')

@click.pass_context
def run_pipeline(ctx, mode, repo):
    """Launch a pipeline (build, deploy or destroy)"""
    ctx.obj["helper"].run_pipeline(mode,repo) 

@cli.command()
@click.option('--id',type=int, help='Enter pipeline id')
@click.pass_context
def check_pipeline(ctx, id):
    """Check the status of a pipeline"""
    ctx.obj["helper"].check_pipeline(id)

