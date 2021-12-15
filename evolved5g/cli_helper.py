from .utils import cookiecutter_generate
import requests
import json
import json.decoder
from click import echo
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

class  CLI_helper:

    def __init__(self):

        self.url_curl = "https://epg-api.tid.es/api/executions"
        self.url_token = "https://epg-api.tid.es/api/auth"
        self.username_token = "usu_Evolved5g"
        self.password_token = "evolved5g"
        self.branch = "evolved5g"
        self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": None }

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
        location = "gh:EVOLVED-5G/template" 
        directory = "template"
        cookiecutter_generate(location, directory) #extra_context=extra)

    def generate_token(self):

        self.header = { "content-Type":"application/json", "accept": None, "Authorization": None }
        data = '{ "username": "usu_Evolved5g", "password": "evolved5g" }'
        resp = requests.post(self.url_token, headers=self.header, data=data)
        return(resp.json()["access_token"])

    def run_pipeline(self, mode, repo):
        """Run the build pipeline for the EVOLVED-5G NetApp"""
        self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": self.generate_token() }
        data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "dummy-netapp/'+ mode +'", "parameters": { "VERSION": "1.0", "GIT_URL": "https://github.com/EVOLVED-5G/' + repo +'", "GIT_BRANCH": "' + self.branch + '"} }'
        resp = requests.post(self.url_curl, headers=self.header, data=data)
        echo(resp.json()["id"])

    def check_pipeline(self, id, pdf):

        """Check the status of the pipeline for the EVOLVED-5G NetApp"""
        self.header = { "content-Type":"application/json", "accept": "application/json", "Authorization": self.generate_token() }
        resp = requests.get(f"{self.url_curl}/{id}", headers=self.header)
        result = resp.json()
        pdfoutput=""

        if result["status"] == "QUEUED":
            echo(result)
        else:
            console = (json.dumps(result["console_log"]).split('\\n'))
            
            for element in console:
                if "] { (" in element:
                    echo(element)
                    pdfoutput='\n'.join([pdfoutput, element])
                elif "[Pipeline]" not in element:
                    if "Lanzada" in element:
                        pass
                    else:
                        echo (element)
                        pdfoutput='\n'.join([pdfoutput, element])
                        if ".groovy" in element:
                            first_word = element.split("-")[1]
                            mode = first_word.split(".")[0]
                elif "] stage" in element:
                    echo(element)
                    pdfoutput='\n'.join([pdfoutput, element])

            if pdf:
                self.generate_pdf(pdfoutput, mode)
        
    def generate_pdf (self, output, mode):
        doc = SimpleDocTemplate(mode+"_Report.pdf", pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=5, bottomMargin=20)

        Story = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        logo = "https://evolved-5g.eu/wp-content/uploads/2021/01/site-logo_2.png"
        im = Image(logo, 8 * cm, 4 * cm)
        Story.append(im)
        Story.append(Paragraph("This is a "+mode+" report.", styles['Heading3']))
        Story.append(Spacer(0,5))
        Story.append(Paragraph(output.replace("\n", "<br />"), styles["Normal"]))

        doc.build(Story)
