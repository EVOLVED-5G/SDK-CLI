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
@click.option('--config-file', type=str, help="Provide User config location for custom package")
@click.pass_context
def generate(ctx,config_file):
    """Generate EVOLVED-5G compliant NetApp from template"""
    ctx.obj["helper"].generate(config_file)

@cli.command()
@click.option('--mode',type=click.Choice(['build', 'deploy','destroy', 'code_analysis', 'security_scan'], case_sensitive=False))
@click.option('--repo',type=str, help='Enter repo name')

@click.pass_context
def run_verification_tests(ctx, mode, repo):
    """Launch different verification tests"""
    ctx.obj["helper"].run_verification_tests(mode,repo)

@cli.command()
@click.option('--id',type=int, help='Enter pipeline id')
@click.pass_context
def check_job(ctx, id):
    """Check the status of a pipeline"""
    ctx.obj["helper"].check_job(id)


@cli.command()
@click.option('--folder_to_store_certificates',type=str, help='The folder where certificates and authorization files will be stored')
@click.option('--capif_host',type=str, help='The host of the CAPIF Server (Ex. capifcore if you are running the docker container)')
@click.option('--capif_http_port',type=str, help='The http port of the CAPIF Server (Ex. 8080 if you are running the docker container)')
@click.option('--capif_https_port',type=str, help='The https port of theCAPIF Server (Ex. 443 if you are running the docker container)')
@click.option('--capif_netapp_username',type=str, help='The CAPIF username of your netapp')
@click.option('--capif_netapp_password',type=str, help='The CAPIF password  of your netapp')
@click.option('--capif_callback_url',type=str, help='A url provided by you that will be used to receive HTTP POST notifications from CAPIF.')
@click.option('--description',type=str, help='A short description of your netapp')
@click.option('--csr_common_name',type=str, help='The CommonName that will be used in the generated X.509 certificate')
@click.option('--csr_organizational_unit',type=str, help='The OrganizationalUnit that will be used in the generated X.509 certificate')
@click.option('--csr_organization',type=str, help='The Organization that will be used in the generated X.509 certificate')
@click.option('--crs_locality',type=str, help=' The Locality that will be used in the generated X.509 certificate')
@click.option('--csr_state_or_province_name',type=str, help='The StateOrProvinceName that will be used in the generated X.509 certificate')
@click.option('--csr_country_name',type=str, help='The CountryName that will be used in the generated X.509 certificate')
@click.option('--csr_email_address',type=str, help='The email that will be used in the generated X.509 certificate')
@click.pass_context
def register_and_onboard_to_capif(ctx,
                                  folder_to_store_certificates: str,
                                  capif_host: str,
                                  capif_http_port: str,
                                  capif_https_port: str,
                                  capif_netapp_username,
                                  capif_netapp_password: str,
                                  capif_callback_url: str,
                                  description:str,
                                  csr_common_name: str,
                                  csr_organizational_unit: str,
                                  csr_organization: str,
                                  crs_locality: str,
                                  csr_state_or_province_name,
                                  csr_country_name:str,
                                  csr_email_address:str):

    ctx.obj["helper"].register_and_onboard_to_capif(folder_to_store_certificates,
                                                    capif_host,
                                                    capif_http_port,
                                                    capif_https_port,
                                                    capif_netapp_username,
                                                    capif_netapp_password,
                                                    capif_callback_url,
                                                    description,
                                                    csr_common_name,
                                                    csr_organizational_unit,
                                                    csr_organization,
                                                    crs_locality,
                                                    csr_state_or_province_name,
                                                    csr_country_name,
                                                    csr_email_address)
