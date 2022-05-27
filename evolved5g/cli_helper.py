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
        self.branch = "evolved5g"
        self.branch_develop = "develop"
        self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": None }
        self.repository = "https://api.github.com/repos/EVOLVED-5G"

    def generate(self, repo_name, package_name, template):
        """Generate EVOLVED-5G compliant NetApp from template"""
        # extra = {}
        # if repo_name:
        #     extra['repoName'] = repo_name
        # if package_name:
        #     extra['packageName'] = package_name
        # if template:
        #     cookiecutter_generate(template,no_input=no_input,extra_context=extra)
        #     return
        location = "gh:EVOLVED-5G/NetApp-template" 
        directory = "template"
        cookiecutter_generate(location, directory) #extra_context=extra)

    def generate_token(self):

        self.header = { "content-Type":"application/json", "accept": None, "Authorization": None }
        data = '{ "username": "usu_Evolved5g", "password": "evolved5g" }'
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
                    data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "dummy-netapp/'+ mode +'", "parameters": { "VERSION": "1.0", "GIT_URL": "https://github.com/EVOLVED-5G/' + repo +'", "GIT_BRANCH": "' + self.branch + '"} }'
                    resp = requests.post(self.url_curl, headers=self.header, data=data)
                    echo(resp.json()["id"])
                else:
                    self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": self.generate_token() }
                    data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "dummy-netapp/'+ mode +'", "parameters": { "VERSION": "1.0", "GIT_URL": "https://github.com/EVOLVED-5G/' + repo +'", "GIT_BRANCH": "' + self.branch_develop + '"} }'
                    resp = requests.post(self.url_curl, headers=self.header, data=data)
                    echo(resp.json()["id"])            
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
   

