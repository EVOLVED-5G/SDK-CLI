from evolved5g.sdk import CAPIFProviderConnector
import capif_exposer_utils

def showcase_capif_nef_connector():
    """

    """
    capif_connector = CAPIFProviderConnector(certificates_folder=capif_exposer_utils.nef_exposer_get_certificate_folder(),
                                             capif_host="capifcore",
                                             capif_http_port="8080",
                                             capif_https_port="443",
                                             capif_netapp_username="test_nef_004",
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
        service_api_description_json_full_path=capif_exposer_utils.nef_exposer_get_sample_api_description_path())


if __name__ == "__main__":
    #Let's register a NEF to CAPIF. This should happen exactly once
    showcase_capif_nef_connector()
