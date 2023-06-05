from evolved5g.sdk import CAPIFInvokerConnector, ServiceDiscoverer
import emulator_utils

def showcase_offboard_and_deregister_netapp():
    capif_connector = CAPIFInvokerConnector(folder_to_store_certificates=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                            capif_host="capifcore",
                                            capif_http_port="8080",
                                            capif_https_port="443",
                                            capif_netapp_username="custom_netapp36",
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
    capif_connector.offboard_and_deregister_netapp()



if __name__ == "__main__":
    showcase_offboard_and_deregister_netapp()


