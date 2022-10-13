from evolved5g.sdk import CAPIFConnector


def showcase_capif_connector():
    """
        This method showcases how one can use the CAPIFConnector class.
        This class is intended for use within the evolved5G Command Line interface.
        It is a low level class part of the SDK that is not required to use while creating NetApps
    """
    capif_connector = CAPIFConnector(folder_to_store_certificates= "/home/alex/Projects/test_certificate_folder",
                                     capif_host="capifcore",
                                     capif_http_port="8080",
                                     capif_https_port="443",
                                     capif_netapp_username="test_netapp17",
                                     capif_netapp_password="test_netapp_password",
                                     capif_callback_url="http://localhost:5000",
                                     description= "test_app_description",
                                     csr_common_name="test_app_common_name",
                                     csr_organizational_unit="test_app_ou",
                                     csr_organization="test_app_o",
                                     crs_locality="Madrid",
                                     csr_state_or_province_name="Madrid",
                                     csr_country_name="ES",
                                     csr_email_address="test@example.com"
                                     )

    capif_connector.register_and_onboard_netapp()


if __name__ == "__main__":
    showcase_capif_connector()
