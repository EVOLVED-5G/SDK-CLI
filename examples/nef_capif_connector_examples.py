from evolved5g.sdk import CAPIFExposerConnector

def showcase_capif_nef_connector():
    """

    """
    capif_connector = CAPIFExposerConnector(certificates_folder="/the_path_to_the_certificates_folder/",
                                            capif_host="capifcore",
                                            capif_http_port="8080",
                                            capif_https_port="443",
                                            capif_netapp_username="test_nef01",
                                            capif_netapp_password="test_netapp_password",
                                            description= "test_app_description"
                                            )

    capif_connector.register_and_onboard_exposer()

    capif_connector.publish_services(
        service_api_description_json_full_path="/the_path_to_service_api_description_json")


if __name__ == "__main__":
    #Let's register a NEF to CAPIF. This should happen exactly once
    showcase_capif_nef_connector()
