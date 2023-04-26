from evolved5g.sdk import CAPIFProviderConnector, CAPIFLogger, CAPIFAuditor
import capif_exposer_utils

def showcase_save_log_to_capif():
    """
        CAPIF Logger class can be used by providers (NEF emulator or TSN) in order to log API request and responses
        by invokers.

        This example demonstrates the usage of the CAPIF Logger class. Make sure you have:

        1.NEF registered and stored to CAPIF.
            After registration of NEF to CAPIF make sure that in the certificates folder you can view
            a) the generated certificates
            b) the capif_provider_details.json
            c) a json file for every service that you have published.  If during publish, you published a service file with name "nef_api_description_sample.json"
            then in this folder you will find a file with name "CAPIF_nef_api_description_sample.json".
            This contains the related CAPIF Ids. You need the api id from this file.

        2. A Net App registered to CAPIF.  This Net App should have an associated CAPIF_INVOKER_ID.
           You can find api invoker ids in the mongo database of CAPIF. http://localhost:8082/db/capif/invokerdetails
           If your CAPIF instance does not have any NetApps registered, you can run example "netapp_capif_connector_examples.py"
    """

    capif_logger = CAPIFLogger(certificates_folder=capif_exposer_utils.nef_exposer_get_certificate_folder(),
                               capif_host="capifcore",
                               capif_https_port="443"
                               )
    log_entries = []

    service_description = capif_logger.get_capif_service_description(capif_service_api_description_json_full_path=
                                                        capif_exposer_utils.nef_exposer_get_sample_api_description_path_that_is_stored_in_capif())

    api_id = service_description["apiId"]
    log_entry = CAPIFLogger.LogEntry(apiId = api_id,
                                     apiVersion="v1",
                                     apiName="/nef/api/v1/3gpp-monitoring-event/",
                                     resourceName="MONITORING_SUBSCRIPTIONS",
                                     uri="/{scsAsId}/subscriptions",
                                     protocol="HTTP_1_1",
                                     invocationTime= "2023-01-24T12:20:00+00:00",
                                     invocationLatency=10,
                                     operation="POST",
                                     result="200",
                                     inputParameters={},
                                     outputParameters={}
                                     )

    log_entries.append(log_entry)
    # In this example we will save a log entry for a specific api invoker id (for example a Network App)
    # When you register a Network App to CAPIF it is assigned an api invoker id.
    # You can find api invoker ids in the mongo database of CAPIF. http://localhost:8082/db/capif/invokerdetails
    # If your CAPIF instance does not have any Network Apps registered, you can run example "netapp_capif_connector_examples.py"
    api_invoker_id = capif_exposer_utils.get_demo_invoker_id()

    capif_logger.save_log(api_invoker_id,log_entries)

def showcase_quering_the_capif_log():
    capif_auditor = CAPIFAuditor(certificates_folder=capif_exposer_utils.nef_exposer_get_certificate_folder(),
                                 capif_host="capifcore",
                                 capif_https_port="443")

    # In this example we will save a log entry for a specific api invoker id (for example a Network App)
    # When you register a Network App to CAPIF it is assigned an api invoker id.
    # You can find api invoker ids in the mongo database of CAPIF. http://localhost:8082/db/capif/invokerdetails
    # If your CAPIF instance does not have any Network Apps registered, you can run example "netapp_capif_connector_examples.py"
    api_invoker_id = capif_exposer_utils.get_demo_invoker_id()

    print("Filtering log for invoker" + api_invoker_id)
    query_results_1 = capif_auditor.query_log(api_invoker_id= api_invoker_id)
    print(query_results_1)

    # Now let's further query the Log with the API ID parameter.
    # API ID is the id of our published service. We can find this parameter in the certificates folder,
    # in the relevant .json file that was created during onboarding of the Provider to CAPIF
    # The helper method below reads that file:
    service_description = capif_auditor.get_capif_service_description(capif_service_api_description_json_full_path=
                                                                      capif_exposer_utils.nef_exposer_get_sample_api_description_path_that_is_stored_in_capif())
    api_id = service_description["apiId"]
    print("Filtering log for invoker" + api_invoker_id + " and api_id " + api_id)
    query_results_2 = capif_auditor.query_log(api_invoker_id= api_invoker_id, api_id = api_id)
    print(query_results_2)


if __name__ == "__main__":
    showcase_save_log_to_capif()
    showcase_quering_the_capif_log()
