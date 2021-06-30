"""Console script for evolved5g."""
import sys
import click
from cookiecutter.main import cookiecutter
import os 


@click.command()
def main(args=None):
    """Console script for evolved5g."""
    click.echo("Replace this message by putting your code into "
               "evolved5g.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

@click.group()
def cli():
    pass


@click.command()
@click.option('-n', '--name', type=str, help='Name to greet', default='World')
def hello(name):
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    click.echo(__location__)
    click.echo(f'Hello {name}')

@click.command()
@click.option('-r', '--repeat', type=int, help='times to repeat', default=1)
@click.option('-n', '--name', type=str, help='Name to greet', default='World')
def test(repeat,name):
    for i in range(repeat):
        click.echo(f'Hello {name}')

@click.command()
def generate():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), ".."))
    click.echo(__location__)
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter( __location__ + '/cookiecutter_template/')
    # Create project from the cookiecutter-pypackage.git repo template
    # cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
    

cli.add_command(hello)
cli.add_command(test)
cli.add_command(generate)
cli()



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
