from evolved5g.swagger_client.rest import ApiException

from evolved5g.sdk import LocationSubscriber
import emulator_utils
import datetime
import time
from jose import jwt
from OpenSSL import crypto


def extract_public_key(cert_path: str):
    try:
        with open(cert_path, 'r') as f:
            cert = f.read()
    except FileNotFoundError as e:
        print(e)

    crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    pubKeyObject = crtObj.get_pubkey()
    pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pubKeyObject)
    return pubKeyString

if __name__ == "__main__":

    location_subscriber = LocationSubscriber(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                             capif_host=emulator_utils.get_capif_host(),
                                             capif_https_port=emulator_utils.get_capif_https_port())

    configuration = location_subscriber.cell_api.api_client.configuration
    access_token_from_capif = configuration.access_token

    #try to decrypt the token using the capif_cert_Server.pem
    url_of_pem_file ="/home/alex/Projects/maggioli/evolved-5g/nef_medianetlab_dem/NEF_emulator/backend/app/app/core/certificates/capif_cert_server.pem"
    decoded_dic = jwt.decode(access_token_from_capif, extract_public_key(url_of_pem_file), algorithms=["RS256"] )
    print(decoded_dic)

