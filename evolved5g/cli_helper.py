from re import template
from .utils import cookiecutter_generate
import requests
import json
import json.decoder
import logging
from click import echo

class  CLI_helper:

    def __init__(self):

        self.url_curl = "https://epg-api.tid.es/api/executions"
        self.url_token = "https://epg-api.tid.es/api/auth"
        self.username_token = "usu_Evolved5g"
        self.password_token = "evolved5g"
        self.netapp_branch = "evolved5g"
        self.branch_cicd_repo = "develop"
        self.header = { "Content-Type":"application/json", "accept": "application/json", "Authorization": None }
        self.repository = "https://api.github.com/repos/EVOLVED-5G"
        self.jenkinsjob = "003-NETAPPS/999-ToReview/"

    def generate(self, config_file):
        """Generate EVOLVED-5G compliant NetApp from template"""
        location = "gh:EVOLVED-5G/NetApp-template"
        directory = "template"
        cookiecutter_generate(location, config_file, directory, no_input=True)
        

    def generate_token(self):

        self.header = { "content-Type":"application/json", "accept": None, "Authorization": None }
        data = '{ "username": "' + self.username_token + '", "password": "' + self.password_token + '" }'
        resp = requests.post(self.url_token, headers=self.header, data=data)
        return(resp.json()["access_token"])

    def run_pipeline(self, mode, repo):
        """Run the build pipeline for the EVOLVED-5G NetApp"""
        r = requests.get(f"{self.repository}/{repo}")
        repo_exist = r.json()
        if "message" not in repo_exist:
            try:
                if mode == "build":
                    self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": self.generate_token() }
                    data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "'+self.jenkinsjob + mode+'", "parameters": { "VERSION": "1.0", "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo +'", "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '", "GIT_CICD_BRANCH": "' + self.branch_cicd_repo + '"} }'
                    resp = requests.post(self.url_curl, headers=self.header, data=data)
                    echo('Your pipeline ID is: %s' % resp.json()["id"])
                else:
                    self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": self.generate_token() }
                    data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "'+self.jenkinsjob + mode+'", "parameters": { "VERSION": "1.0", "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo +'", "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '", "GIT_CICD_BRANCH": "' + self.branch_cicd_repo + '"} }'
                    resp = requests.post(self.url_curl, headers=self.header, data=data)
                    echo('Your pipeline ID is: %s' % resp.json()["id"])
            except TypeError as e:
                echo("Please enter the correct command: evolved5g run_pipeline --mode build --repo REPOSITORY_NAME")
        else:
            echo(f"The {repo} repository you have chosen does not exist, please check the name you typed and try again.")


    def check_pipeline(self, id):

        """Check the status of the pipeline for the EVOLVED-5G NetApp"""

        try:
            self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": self.generate_token() }
            resp = requests.get(f"{self.url_curl}/{id}", headers=self.header)
            result = resp.json()

            if result["status"] == "QUEUED":
                echo(result)
            else:
                console = (json.dumps(result["console_log"]).split('\\n'))

                for element in console:
                    if "] { (" in element:
                        echo(element)
                    elif "[Pipeline]" not in element:
                        echo(element)
                    elif "] stage" in element:
                        echo(element)
        except ValueError as e:
            echo("Please add the ID: evolved5g check-pipeline --id <yourID>")


