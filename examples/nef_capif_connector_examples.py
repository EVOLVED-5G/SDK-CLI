from evolved5g.sdk import CAPIFExposerConnector

def showcase_capif_nef_connector():
    """

    """
    capif_connector = CAPIFExposerConnector(certificates_folder="/home/alex/Projects/test_nef_certificate_folder/",
                                            capif_host="capifcore",
                                            capif_http_port="8080",
                                            capif_https_port="443",
                                            capif_netapp_username="test_nef36",
                                            capif_netapp_password="test_netapp_password",
                                            description= "test_app_description"
                                            )

    capif_connector.register_and_onboard_exposer(
        api_provider_domain_json_full_path="/home/alex/Projects/test_nef_certificate_folder/api_provider_domain.json"
    )

    capif_connector.publish_services(
        service_api_description_json_full_path="/home/alex/Projects/test_nef_certificate_folder/service_api_description.json")


if __name__ == "__main__":
    showcase_capif_nef_connector()
