from .utils import cookiecutter_generate
import requests
import json
import json.decoder



class  CLI_helper:

    def __init__(self):

        self.url_curl = "https://epg-api.tid.es/api/executions"
        self.url_token = "https://epg-api.tid.es/api/auth"
        self.username_token = "usu_Evolved5g"
        self.password_token = "evolved5g"
        self.branch = "nginx-unprivileged"
        self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": None }

    def generate(self, no_input, repo_name, package_name, template):
        """Generate EVOLVED-5G compliant NetApp from template"""
        # extra = {}
        # if repo_name:
        #     extra['repoName'] = repo_name
        # if package_name:
        #     extra['packageName'] = package_name
        # if template:
        #     cookiecutter_generate(template,no_input=no_input,extra_context=extra)
        #     return
        location = "gh:EVOLVED-5G/template" 
        cookiecutter_generate(location, no_input=no_input) #extra_context=extra)

    def curl(self, tokeng, branchorpipe, mode):

        self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": tokeng }
        
        if mode == "build" or mode == "deploy" or  mode == "destroy":
            repo = input("Please write down your repo:\n")
            data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "dummy-netapp/'+ mode +'", "parameters": { "VERSION": "1.0", "GIT_URL": "https://github.com/EVOLVED-5G/' + repo +'", "GIT_BRANCH": "' + branchorpipe + '"} }'
            resp = requests.post(self.url_curl, headers=self.header, data=data)

            return (resp.json()["id"])

        if mode == "check":
            resp = requests.get(f"{self.url_curl}/{branchorpipe}", headers=self.header)

            return (resp.json())

    def generate_token(self):

        self.header = { "content-Type":"application/json", "accept": None, "Authorization": None }
        data = '{ "username": "usu_Evolved5g", "password": "evolved5g" }'
        resp = requests.post(self.url_token, headers=self.header, data=data)

        # print ("This is your token:\n", resp.json()["access_token"] + "\n")
        return(resp.json()["access_token"])

    
    def run_pipeline(self):
        """Run the build pipeline for the EVOLVED-5G NetApp"""
        mode = input("Type in which pipeline you want to run: build, deploy or destroy:\n ")
        result = self.curl(self.generate_token(), self.branch, mode)

        print ("The ID of your pipeline is:\n", result,"\n")

    
    def check_pipeline(self):

        """Check the status of the pipeline for the EVOLVED-5G NetApp"""
        pipelineid = input("Please write down the pipeline ID you want to check:\n")

        result = self.curl(self.generate_token(), pipelineid, "check")

        if result["status"] == "QUEUED":
            print(result)
        else:
            console = (json.dumps(result["console_log"]).split('\\n'))

            for element in console:
                if "] { (" in element:
                    print (element)
                elif "[Pipeline]" not in element:
                    print (element)
                elif "] stage" in element:
                    print (element)


        # if "message" in result:
        #     print (result["message"])

        # else:
        #     console = (json.dumps(result["console_log"]).split('\\n'))

        #     for element in console:
        #         if "] { (" in element:
        #             print (element)
        #         elif "[Pipeline]" not in element:
        #             print (element)
        #         elif "] stage" in element:
        #             print (element)


