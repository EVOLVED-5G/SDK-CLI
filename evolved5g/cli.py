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
@click.option(
    "--config-file", type=str, help="Provide User config location for custom package"
)
@click.pass_context
def generate(ctx, config_file):
    """Generate EVOLVED-5G compliant NetApp from template"""
    ctx.obj["helper"].generate(config_file)


@cli.command()
@click.option(
    "--mode",
    type=click.Choice(
        ["build", "deploy", "destroy", "capif_nef", "capif_tsn", "code_analysis", "security_scan", "validation"],
        case_sensitive=False,
    ),
)
@click.option("--repo", type=str, help="Enter repo name")
@click.option("--user", type=str, help="Enter your username for pipelines")
@click.option("--passwd", type=str, help="Enter repo password for pipelines")

@click.pass_context
def run_verification_tests(ctx, mode, repo, user, passwd):
    """Launch different verification tests"""
    ctx.obj["helper"].run_verification_tests(mode, repo, user, passwd)


@cli.command()
@click.option("--id", type=int, help="Enter pipeline id")
@click.option("--user", type=str, help="Enter your username for pipelines")
@click.option("--passwd", type=str, help="Enter repo password for pipelines")
@click.pass_context
def check_job(ctx, id, user, passwd):
    """Check the status of a pipeline"""
    ctx.obj["helper"].check_job(id, user, passwd)


@cli.command()
@click.option(
    "--config_file_full_path",
    type=str,
    help="""The configuration file used to register and onboard the NetApp to CAPIF
                --folder_to_store_certificates: The folder where certificates and authorization files will be stored
                --capif_host: The host of the CAPIF Server (Ex. capifcore if you are running the docker container)
                --capif_http_port: The http port of the CAPIF Server (Ex. 8080 if you are running the docker container)
                --capif_https_port: The https port of theCAPIF Server (Ex. 443 if you are running the docker container)
                --capif_netapp_username: The CAPIF username of your netapp
                --capif_netapp_password: The CAPIF password  of your netapp
                --capif_callback_url: A url provided by you that will be used to receive HTTP POST notifications from CAPIF.
                --description: A short description of your netapp
                --csr_common_name: The CommonName that will be used in the generated X.509 certificate
                --csr_organizational_unit: The OrganizationalUnit that will be used in the generated X.509 certificate
                --csr_organization: The Organization that will be used in the generated X.509 certificate
                --crs_locality: The Locality that will be used in the generated X.509 certificatE
                --csr_state_or_province_name: The StateOrProvinceName that will be used in the generated X.509 certificate
                --csr_country_name: The CountryName that will be used in the generated X.509 certificate
                --csr_email_address: The email that will be used in the generated X.509 certificate              
              """,
)
@click.pass_context
def register_and_onboard_to_capif(ctx, config_file_full_path: str):
    ctx.obj["helper"].register_and_onboard_to_capif(config_file_full_path)
    # ctx.obj["helper"].test_capif_and_nef_published_to_capif_endpoints(config_file_full_path)


@cli.command()
@click.option(
    "--config_file_full_path",
    type=str,
    help="""The configuration file used to apply Time-Sensitive Network Functionalities to your NetApp. 
    --https: True to use HTTPS, False to use HTTP
    --tsn_api_host: The host of the TSN API Server 
    --tsn_api_port: The http port of the TSN API Server (Ex. 8888 if you are running the docker container) 
    --netapp_name: The name of your netapp --folder_to_store_clearance_token: The folder where tokens that can be 
    used to reset TSN configurations will be stored at
    """,
)
@click.pass_context
def get_tsn_profiles(ctx, config_file_full_path: str):
    """Lists all available TSN profiles"""
    ctx.obj["helper"].get_tsn_profiles(config_file_full_path)


@cli.command()
@click.option(
    "--config_file_full_path",
    type=str,
    help="""The configuration file used to apply Time-Sensitive Network Functionalities to your NetApp. 
    --https: True to use HTTPS, False to use HTTP
    --tsn_api_host: The host of the TSN API Server 
    --tsn_api_port: The http port of the TSN API Server (Ex. 8888 if you are running the docker container) 
    --netapp_name: The name of your netapp --folder_to_store_clearance_token: The folder where tokens that can be 
    used to reset TSN configurations will be stored at
    """,
)
@click.option(
    "--profile_name",
    type=str,
    help="""The name of the TSN profile you would like to apply to the NetApp""",
)
@click.pass_context
def apply_tsn_profile(ctx, config_file_full_path: str, profile_name: str):
    ctx.obj["helper"].apply_tsn_profile(config_file_full_path, profile_name)
