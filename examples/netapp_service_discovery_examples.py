from evolved5g.sdk import CAPIFInvokerConnector, ServiceDiscoverer
from examples import emulator_utils


def showcase_service_discovery():
    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                           capif_host="capifcore",
                                           capif_https_port=443
                                           )
    endpoints = service_discoverer.discover_service_apis()
    print(endpoints)

def showcase_retrieve_endpoint_url_from_tsn():
    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                           capif_host="capifcore",
                                           capif_https_port=443
                                           )
    print("The endpoint for api name: /tsn/api/ and resource: TSN_LIST_PROFILES")
    url = service_discoverer.retrieve_specific_resource_name(
        "/tsn/api/",
        "TSN_LIST_PROFILES"
    )
    print(url)

def showcase_retrieve_endpoint_url_from_nef():
    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                           capif_host="capifcore",
                                           capif_https_port=443
                                           )
    url = service_discoverer.retrieve_specific_resource_name(
        "/nef/api/v1/3gpp-monitoring-event/",
        "MONITORING_SUBSCRIPTIONS"
    )
    print("The endpoint for api name: /nef/api/v1/3gpp-monitoring-event/ and resource: MONITORING_SUBSCRIPTIONS")
    print(url)


def showcase_access_token_retrieval_from_capif():
    service_discoverer = ServiceDiscoverer(folder_path_for_certificates_and_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                           capif_host="capifcore",
                                           capif_https_port=443
                                           )
    endpoints = service_discoverer.discover_service_apis()
    if len(endpoints)>0:
        ## The access token is always retrieved for a specific api name and a specific endpoint (that is mapped ton an api_id and aef_id)
        ## For the purposes of the example we retrieve the fist available
        api_name = endpoints["serviceAPIDescriptions"][0]["apiName"]
        api_id =  endpoints["serviceAPIDescriptions"][0]["apiId"]
        aef_id =  endpoints["serviceAPIDescriptions"][0]["aefProfiles"][0]["aefId"]
        print("Retrieving access token for api name: " + api_name  + " and api_id: " + api_id)
        access_token = service_discoverer.get_access_token(api_name,api_id,aef_id)
        print(access_token)
    else:
        print("no endpoints have been registered. Make sure NEF has registered to CAPIF first")

if __name__ == "__main__":
    #The following code assumes that you have already registered the net app to capif.
    showcase_service_discovery()
    showcase_retrieve_endpoint_url_from_tsn()
    showcase_access_token_retrieval_from_capif()
