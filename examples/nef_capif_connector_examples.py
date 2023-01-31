from evolved5g.sdk import CAPIFProviderConnector

def showcase_capif_nef_connector():
    """

    """
    capif_connector = CAPIFProviderConnector(certificates_folder="/home/alex/Projects/test_nef_certificate_folder",  #"/the_path_to_the_certificates_folder/",
                                             capif_host="capifcore",
                                             capif_http_port="8080",
                                             capif_https_port="443",
                                             capif_netapp_username="test_nef015",
                                             capif_netapp_password="test_netapp_password",
                                             description= "test_app_description",
                                             csr_common_name="test_nef_common_name",
                                             csr_organizational_unit="test_app_ou",
                                             csr_organization="test_app_o",
                                             crs_locality="Madrid",
                                             csr_state_or_province_name="Madrid",
                                             csr_country_name="ES",
                                             csr_email_address="test@example.com"
                                             )

    capif_connector.register_and_onboard_provider()

    capif_connector.publish_services(
        service_api_description_json_full_path="/home/alex/Projects/SciFY/evolved-5g/SDK-CLI/examples/capif_exposer_sample_files/service_api_description.json")


if __name__ == "__main__":
    #Let's register a NEF to CAPIF. This should happen exactly once
    showcase_capif_nef_connector()
