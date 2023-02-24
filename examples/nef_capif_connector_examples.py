from evolved5g.sdk import CAPIFProviderConnector

def showcase_capif_nef_connector():
    """

    """

    certificates_folder_path ="/home/alex/Projects/test_nef_certificate_folder"
    service_api_description_json_full_path ="/home/alex/Projects/maggioli/evolved-5g/SDK-CLI/examples/capif_exposer_sample_files/nef_api_description_sample.json"

    capif_connector = CAPIFProviderConnector(certificates_folder=certificates_folder_path,
                                             capif_host="capifcore",
                                             capif_http_port="8080",
                                             capif_https_port="443",
                                             capif_netapp_username="test_nef_001",
                                             capif_netapp_password="testpassword",
                                             description= "test_app_description",
                                             csr_common_name="test_test_",
                                             csr_organizational_unit="test_app_ou",
                                             csr_organization="test_app_o",
                                             crs_locality="Madrid",
                                             csr_state_or_province_name="Madrid",
                                             csr_country_name="ES",
                                             csr_email_address="test@example.com"
                                             )

    capif_connector.register_and_onboard_provider()

    capif_connector.publish_services(
        service_api_description_json_full_path=service_api_description_json_full_path)


if __name__ == "__main__":
    #Let's register a NEF to CAPIF. This should happen exactly once
    showcase_capif_nef_connector()
