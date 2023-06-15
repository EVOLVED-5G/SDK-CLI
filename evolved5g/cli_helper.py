from .nef_and_tsn_api_service_validation_pipeline import validate_all_endpoints_returned_by_service_discoverer
from .utils import cookiecutter_generate
import requests
import json
import json.decoder
import logging
from click import echo
from evolved5g.sdk import CAPIFInvokerConnector, TSNManager
import traceback


class CLI_helper:
    def __init__(self):

        self.url_curl = "https://evolvedpipes.apps.ocp-epg.tid.es/launch"
        self.url_curl_job = "https://evolvedpipes.apps.ocp-epg.tid.es/job"
        self.netapp_branch = "evolved5g"
        self.branch_cicd_repo = "develop"
        self.header = {
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        self.repository = "https://api.github.com/repos/EVOLVED-5G"

    def generate(self, config_file):
        """Generate EVOLVED-5G compliant NetApp from template"""
        location = "gh:EVOLVED-5G/NetApp-template"
        directory = "template"
        cookiecutter_generate(location, config_file, directory, no_input=True)

    def run_verification_tests(self, mode, repo, user, passwd, capifpath, certpath, verfpath, version):
        """Run the build pipeline for the EVOLVED-5G NetApp"""

        if repo is None:
            echo(
                "'None' value provided.\nPlease enter the correct command: evolved5g run-verification-tests --mode "
                "build --repo REPOSITORY_NAME "
            )
        else:
            r = requests.get(f"{self.repository}/{repo}")
            repo_exist = r.json()

            if "message" not in repo_exist:
                try:
                    if mode == "build":
                        self.header = {
                            "content-Type": "application/json",
                            "accept": "application/json",
                            "username": user,
                            "password": passwd,
                        }

                        data = (
                                '{ "action": "'
                                + mode
                                + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/'
                                + repo
                                + '", "VERSION_NETAPP": "'
                                + version
                                + '","GIT_NETAPP_BRANCH": "'
                                + self.netapp_branch
                                + '"} }'
                        )

                        resp = requests.post(
                            self.url_curl, headers=self.header, data=data
                        )

                        if (resp.json()['status'] == 403):
                            echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                        else:
                            echo(
                                f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")

                    elif mode == "deploy":
                        self.header = {
                            "content-Type": "application/json",
                            "accept": "application/json",
                            "username": user,
                            "password": passwd,
                        }

                        foldernetapp = repo.lower()
                        data = (
                                '{ "action": "'
                                + mode
                                + '", "parameters": { "FOLDER_NETWORK_APP": "'
                                + foldernetapp
                                + '","RELEASE_NAME": "'
                                + repo
                                + '"} }'
                        )

                        resp = requests.post(
                            self.url_curl, headers=self.header, data=data
                        )

                        if (resp.json()['status'] == 403):
                            echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                        else:
                            echo(
                                f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")

                    elif mode == "destroy":
                        self.header = {
                            "content-Type": "application/json",
                            "accept": "application/json",
                            "username": user,
                            "password": passwd,
                        }

                        data = (
                                '{ "action": "'
                                + mode
                                + '", "parameters": { "RELEASE_NAME": "'
                                + repo
                                + '"} }'
                        )

                        resp = requests.post(
                            self.url_curl, headers=self.header, data=data
                        )

                        if (resp.json()['status'] == 403):
                            echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                        else:
                            echo(
                                f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")


                    elif mode == "code_analysis":
                        self.header = {
                            "content-Type": "application/json",
                            "accept": "application/json",
                            "username": user,
                            "password": passwd,
                        }

                        data = (
                                '{ "action": "'
                                + mode
                                + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/'
                                + repo
                                + '","GIT_NETAPP_BRANCH": "'
                                + self.netapp_branch
                                + '"} }'
                        )

                        resp = requests.post(
                            self.url_curl, headers=self.header, data=data
                        )

                        if (resp.json()['status'] == 403):
                            echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                        else:
                            echo(f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")


                    elif mode == "security_scan":
                        self.header = {
                            "content-Type": "application/json",
                            "accept": "application/json",
                            "username": user,
                            "password": passwd,
                        }
                        data = (
                                '{ "action": "'
                                + mode
                                + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/'
                                + repo
                                + '","GIT_NETAPP_BRANCH": "'
                                + self.netapp_branch
                                + '"} }'
                        )
                        resp = requests.post(
                            self.url_curl, headers=self.header, data=data
                        )

                        if (len(resp.json()) > 3):  # List
                            echo(f"{resp.json()['detail']} Please wait until your previous pipeline has been finished.")
                        else:  # It is a List treated as Dictionary
                            echo(
                                f"Your pipeline ID is: {resp.json()[0]['job_id']}, {resp.json()[1]['job_id']} and {resp.json()[2]['job_id']} and the actual status for each is: {resp.json()[0]['status']}, "
                                f"{resp.json()[1]['status']} and {resp.json()[2]['status']}.")

                    elif mode == "capif_nef":

                        if (not capifpath or  not certpath or not verfpath):
                            print (f"Please provide all the files and folder required to launch the NEF pipeline.\n"
                                   f"You must provide the path for capif registration file, the path where to store the certification files"
                                   f"and the path of the file to be verified. You have actually provided:\n"
                                   f"Path for CAPIF registration file (json): {capifpath}\nPath for certification files: {certpath}\nPath for verification file: {verfpath}")
                        else:
                            self.header = {
                                "content-Type": "application/json",
                                "accept": "application/json",
                                "username": user,
                                "password": passwd,
                            }

                            data = (
                                    '{ "action": "'
                                    + mode
                                    + '", "parameters": { "NetApp_repo": "'
                                    + repo
                                    + '","CAPIF_REGISTRATION_CONFIG_PATH": "'
                                    + capifpath
                                    + '","CERTIFICATES_FOLDER_PATH": "'
                                    + certpath
                                    + '","VERIFICATION_FILE": "'
                                    + verfpath
                                    + '","NetApp_repo_branch": "'
                                    + self.netapp_branch
                                    + '"} }'
                            )

                            resp = requests.post(
                                self.url_curl, headers=self.header, data=data
                            )

                            if (resp.json()['status'] == 403):
                                echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                            else:
                                echo(
                                    f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")

                    elif mode == "capif_tsn":
                        if (not capifpath or  not certpath or not verfpath):
                            print (f"Please provide all the files and folder required to launch the NEF pipeline.\n"
                                   f"You must provide the path for capif registration file, the path where to store the certification files"
                                   f"and the path of the file to be verified. You have actually provided:\n"
                                   f"Path for CAPIF registration file (json): {capifpath}\nPath for certification files: {certpath}\nPath for verification file: {verfpath}")
                        else:
                            self.header = {
                                "content-Type": "application/json",
                                "accept": "application/json",
                                "username": user,
                                "password": passwd,
                            }

                            data = (
                                    '{ "action": "'
                                    + mode
                                    + '", "parameters": { "NetApp_repo": "'
                                    + repo
                                    + '","CAPIF_REGISTRATION_CONFIG_PATH": "'
                                    + capifpath
                                    + '","CERTIFICATES_FOLDER_PATH": "'
                                    + certpath
                                    + '","VERIFICATION_FILE": "'
                                    + verfpath
                                    + '","NetApp_repo_branch": "'
                                    + self.netapp_branch
                                    + '"} }'
                            )

                            #echo (data)

                            resp = requests.post(
                                self.url_curl, headers=self.header, data=data
                            )
                            print (resp.json())

                            if (resp.json()['status'] == 403):
                                echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                            else:
                                echo(
                                    f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")

                    else:
                        echo(
                            f"The {mode} you have chosen does not exist, please check the modes and try again"
                        )

                except ValueError as e:
                    echo(
                        "Please enter the correct command: evolved5g run-verification-tests --mode build --repo <your_REPOSITORY_NAME>, --user <yourUSERNAME>, --passwd <yourPASSWORD>"
                    )
            else:
                echo(
                    f"The {repo} repository you have chosen does not exist, please check the name you typed and try again."
                )

    def validation(self, repo, user, passwd, environment, deploy, email, version):
        """Run the build pipeline for the EVOLVED-5G NetApp"""

        if deploy is None: deploy = repo

        if repo is None:
            echo(
                "'None' value provided.\nPlease enter the correct command: evolved5g run-verification-tests --repo REPOSITORY_NAME ")
        else:
            r = requests.get(f"{self.repository}/{repo}")
            repo_exist = r.json()

            if "message" not in repo_exist:
                try:
                    self.header = {
                        "content-Type": "application/json",
                        "accept": "application/json",
                        "username": user,
                        "password": passwd,
                    }

                    data = (
                            '{ "action": "validation", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/'
                            + repo
                            + '", "ENVIRONMENT": "'
                            + environment
                            + '", "SEND_DEV_EMAIL": "'
                            + email
                            + '", "VERSION_NETAPP": "'
                            + version
                            + '", "DEPLOY_NAME": "'
                            + deploy
                            + '","GIT_NETAPP_BRANCH": "'
                            + self.netapp_branch
                            + '"} }'
                    )

                    #print(data)

                    resp = requests.post(
                        self.url_curl, headers=self.header, data=data
                    )

                    #echo(f"{resp.json()}")

                    if (resp.json()['status'] == 403):
                        echo(f"{resp.json()['detail']} Please wait until your previous pipeline has finished.")
                    else:
                        echo(f"Your pipeline ID is: {resp.json()['job_id']} and the actual status is: {resp.json()['status']}.")


                except ValueError as e:
                    echo(
                        "Please enter the correct command: evolved5g run-verification-tests --mode build --repo <your_REPOSITORY_NAME>, --user <yourUSERNAME>, --passwd <yourPASSWORD>")
            else:
                echo(
                    f"The {repo} repository you have chosen does not exist, please check the name you typed and try again.")

    def check_job(self, id, user, passwd):

        """Check the status of the pipeline for the EVOLVED-5G NetApp"""

        try:
            self.header = {
                "content-Type": "application/json",
                "accept": "application/json",
                "username": user,
                "password": passwd,
            }
            resp = requests.get(f"{self.url_curl_job}/{id}/status", headers=self.header)
            result = resp.json()

            if result["status"] == "QUEUED":
                # echo(result)
                echo(f"Your pipeline {id} status is {result['status']}, please {result['status'].split(',')[1]}")
            else:
                console = json.dumps(result["log"]).split("\\n")

                for element in console:
                    if "] { (" in element:
                        echo(element)
                    elif "[Pipeline]" not in element:
                        echo(element)
                    elif "] stage" in element:
                        echo(element)
                echo(result["status"])

        except ValueError as e:
            echo("Please add the ID: evolved5g check-job --id <yourID>, --user <yourUSERNAME>, --passwd <yourPASSWORD>")

    def register_and_onboard_to_capif(self, config_file_full_path: str) -> None:
        with open(config_file_full_path, "r") as openfile:
            config = json.load(openfile)
        capif_connector = CAPIFInvokerConnector(
            folder_to_store_certificates=config["folder_to_store_certificates"],
            capif_host=config["capif_host"],
            capif_http_port=config["capif_http_port"],
            capif_https_port=config["capif_https_port"],
            capif_netapp_username=config["capif_netapp_username"],
            capif_netapp_password=config["capif_netapp_password"],
            capif_callback_url=config["capif_callback_url"],
            description=config["description"],
            csr_common_name=config["csr_common_name"],
            csr_organizational_unit=config["csr_organizational_unit"],
            csr_organization=config["csr_organization"],
            crs_locality=config["crs_locality"],
            csr_state_or_province_name=config["csr_state_or_province_name"],
            csr_country_name=config["csr_country_name"],
            csr_email_address=config["csr_email_address"],
        )
        try:
            capif_connector.register_and_onboard_netapp()
            echo(
                "Your netApp has been successfully registered and onboarded to the CAPIF server."
                + "You can now start using the evolved5G SDK!"
            )
        except Exception:
            echo("An error occurred. Registration failed:")
            traceback.print_exc()

    def get_tsn_profiles(self, config_file_full_path: str) -> None:

        """Lists all available TSN profiles"""

        with open(config_file_full_path, "r") as openfile:
            config = json.load(openfile)

        tsn = TSNManager(  # Initialization of the TNSManager
            https=config["https"],
            tsn_host=config["tsn_api_host"],
            tsn_port=config["tsn_api_port"],
        )
        echo("Profiles:")
        echo(
            "\t\n".join(
                [
                    str(
                        {
                            profile.name: profile.get_configuration_for_tsn_profile().get_profile_configuration_parameters()
                        }
                    )
                    for profile in tsn.get_tsn_profiles()
                ]
            )
        )

    def apply_tsn_profile(self, config_file_full_path: str, profile_name: str) -> None:

        with open(config_file_full_path, "r") as openfile:
            config = json.load(openfile)

        tsn = TSNManager(  # Initialization of the TNSManager
            https=config["https"],
            tsn_host=config["tsn_api_host"],
            tsn_port=config["tsn_api_port"],
        )
        netapp_name = config["netapp_name"]
        netapp_tsn_id = tsn.TSNNetappIdentifier(netapp_name=netapp_name)
        tsn_profiles = tsn.get_tsn_profiles()
        matched_profiles = [p for p in tsn_profiles if p.name == profile_name]
        if not matched_profiles:
            raise ValueError(
                f"Error: the profile name {profile_name} does not match an available TSN profile.\n"
                f"Available TSN profile are the following: [{', '.join([p.name for p in tsn_profiles])}]"
            )
        profile = matched_profiles[0]
        clearance_token = tsn.apply_tsn_profile_to_netapp(netapp_tsn_id, profile)
        echo(
            f'The TSN profile "{profile_name}" has been successfully applied to your netapp "{netapp_name}".'
            f'\nStore the token "{clearance_token}" to clear the profile if you wish in the future.'
        )

    def validate_all_endpoints_returned_by_service_discoverer(self, config_file_full_path: str) -> None:
        validate_all_endpoints_returned_by_service_discoverer(config_file_full_path)


