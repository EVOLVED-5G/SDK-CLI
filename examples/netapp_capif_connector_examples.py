from evolved5g.sdk import CAPIFInvokerConnector, ServiceDiscoverer


def showcase_capif_connector():
    """
        This method showcases how one can use the CAPIFConnector class.
        This class is intended for use within the evolved5G Command Line interface.
        It is a low level class part of the SDK that is not required to use while creating NetApps
    """
    capif_connector = CAPIFInvokerConnector(folder_to_store_certificates="/home/alex/Projects/test_certificate_folder",
                                            capif_host="capifcore",
                                            capif_http_port="8080",
                                            capif_https_port="443",
                                            capif_netapp_username="custom_netapp15",
                                            capif_netapp_password="pass123",
                                            capif_callback_url="http://localhost:5000",
                                            description= "Dummy NetApp",
                                            csr_common_name="test02",
                                            csr_organizational_unit="test_app_ou",
                                            csr_organization="test_app_o",
                                            crs_locality="Madrid",
                                            csr_state_or_province_name="Madrid",
                                            csr_country_name="ES",
                                            csr_email_address="test@example.com"
                                            )

    capif_connector.register_and_onboard_netapp()

def showcase_service_discovery():
    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key="/home/alex/Projects/test_certificate_folder",
                                           capif_host="capifcore",
                                           capif_https_port=443
                                           )
    endpoints = service_discoverer.discover_service_apis()
    print(endpoints)

def showcase_access_token_retrieval_from_capif():
    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key="/home/alex/Projects/test_certificate_folder",
                                           capif_host="capifcore",
                                           capif_https_port=443
                                           )
    endpoints = service_discoverer.discover_service_apis()
    if len(endpoints)>0:
        api_name = endpoints["serviceAPIDescriptions"][0]["apiName"]
        api_id =  endpoints["serviceAPIDescriptions"][0]["apiId"]
        aef_id =  endpoints["serviceAPIDescriptions"][0]["aefProfiles"][0]["aefId"]
        access_token = service_discoverer.get_access_token(api_name,api_id,aef_id)
        print(access_token)
    else:
        print("no endpoints have been registered. Make sure NEF has registered to CAPIF first")

if __name__ == "__main__":
    #Let's register NetApp to CAPIF. This should happen exactly once
    showcase_capif_connector()
    showcase_service_discovery()
    showcase_access_token_retrieval_from_capif()
