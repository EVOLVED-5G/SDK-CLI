=======
History
=======
0.8.9 (2023-01-03)
-------------------
* Bug fix on LocationSubscriber on method get_location_information.
    * Previously when calling this method the response object returned two properties:  a) cell_id and b) enode_b_id.  enode_b_id has been dropped in latest versions of the NEF emulator so it was always returned as None by the SDK.
    * With current version the following two properties are returned: a) cell_id and b) g_NB_Id
* New deploy pipeline updated and integrated.
* Added new verification tests CAPIF and NEF.
* Documentation updated including new verification tests CAPIF and NEF.

0.8.8 (2022-12-09)
-------------------
* Update SDK documentation:
    * Update documentation of the SDK libraries by updating the ConnectionMonitor Library information.
    * Update SDK pipelines by updating the commands to run and check pipelines and adding new pipelines.

0.8.7 (2022-11-23)
-------------------
* Update of the SDK library:
    * CAPIFExposerConnector and CAPIFInvokerConnector have capif_http_port and capif_https_port declared as "str" (via type hinting)
    * If the developer passes the parameter as integer we make sure it's casted to string and the code does not fail

0.8.6 (2022-11-23)
-------------------
* Update of the SDK library, on how the CAPIF endpoints are constructed.
    * When connecting to CAPIF if standard ports are used (80,443) we now don't include them to the capif url/endpoint

        * (ex. https://capifcore/register instead of https://capifcore:443/register)

        * (ex. http://capifcore/register instead of  http://capifcore:80/register)

    * If non standard ports are used (ex. 8080) then they are included in the capif url/endpoint
        * (ex.http://capifcore:8080/register)

0.8.5 (2022-10-27)
-------------------
* Update of the SDK library to be compatible with the latest release of NEF  v1.6.1

0.8.4 (2022-10-27)
-------------------
* The SDK Library now communicates first with CAPIF server in order to discover the NEF endpoints

0.8.3 (2022-10-17)
-------------------
* News SDK Library CAPIFExposerConnector, that allows exposers to register to CAPIF and publish services
* New CLI command evolved5G  register-and-onboard-to-capif  that allows NetApps to register their NetAPP to CAPIF via the command line


0.8.2 (2022-10-14)
-------------------
* Bug fix on import CAPIFConnector class from sdk

0.8.1 (2022-10-12)
-------------------
* New class at the Libraries: CAPIFConnector. Used in the CLI in order to onboard a netApp to CAPIF server
* New class at the Libraries: ServiceDiscoverer. Used by developers in order to discover services (endpoints) via the CAPIF server
* Bug fix on LocationSubscriber get_location_information()

0.8.0 (2022-09-23)
-------------------
* New verification tests have been implemented. Such verification tests are related to NetApp code and NetApp container image analysis.
* The execution of the verification tests has been also simplify

0.7.9  (2022-09-22)
-------------------
* Improvement at QosAwareness, for Guaranteed Bit Rate. Up to now, you could ask the 5G Network to send you notification when specific parameters of the QoS session cannot be guaranteed. For example a minimum 5ms delay at uplink. This notification was sent exactly once, when the environment has changed: For example when a minimum 5ms delay at uplink cannot be guaranteed, or when the a minimum 5ms delay at uplink has been established and can be guaranteed. Method create_guaranteed_bit_rate_subscription() has breaking changes. See below the change:

    .. code-block::
       :caption: Method signature create_guaranteed_bit_rate_subscription should be changed

        subscription = qos_awereness.create_guaranteed_bit_rate_subscription(
            ...
            wait_time_between_reports=10
            ...)

        Should be replaced by:

        subscription = qos_awereness.create_guaranteed_bit_rate_subscription(
            ...
            reporting_mode= QosAwareness.EventTriggeredReportingConfiguration(wait_time_in_seconds=10)
            ...)

* New SDK Class, ConnectionMonitor: Consider a scenario where a NetApp wants to monitor 100 devices in the 5G Network. The netapp wants to track, at any given time how many NetApps are connected to the 5G Network and how many netApps are disconnected.Using ConnectionMonitor the NetApp can retrieve notifications by the 5G Network for individual devices when Connection is lost (for example the user device has not been connected to the 5G network for the past 10 seconds) Connection is alive (for example the user device has been connected to the 5G network for the past 10 seconds)

* The documentation about the usability has been updated.

0.7.8  (2022-09-02)
-------------------
* It has been improved the usability. It has been added a configuration file to create the NetApp repository, rather than using a prompt input.
* Cleaning up the code.

0.7.7  (2022-07-04)
-------------------
* Updates on documentation

0.7.6  (2022-07-04)
-------------------
* Documentation has been updated accordingly
* Changes and optimizations for SDK pipeline integration

0.7.5  (2022-06-14)
-------------------
* New build pipeline has been implemented
* Documentation has been updated accordingly

0.7.4  (2022-05-27)
-------------------
* Check if the NetApp repository on which you want to run the pipeline exists on GitHub

0.7.3  (2022-05-09)
-------------------
* Bug fix on value LIVE_STREAMING of enum NonGBRQosReference.
* Rename method at examples>api.py

0.7.2  (2022-04-01)
-------------------
* LocationSubscriber now has a new method get_coordinates_of_cell() that allows a developer to retrieve the location of a cell, given the cell id.

0.7.1  (2022-03-14)
-------------------
* Update deploy and destroy pipelines.

0.7.0  (2022-02-28)
-------------------
* Adding manage exceptions features and documentation update.

0.6.9  (2022-02-23)
------------------
* Improvement for check-pipeline function

0.6.8 (2022-02-03)
------------------
* Changed Template repository location fode to NetApp Template

* Update on the NEF endpoints for monitoring event api and session with Qos.
 This ensures compatibility with latest NEF release

0.6.2 (2022-01-28)
------------------
* Improvements on LocationSubscriber.
A new method has been implemented with name
``get_location_information``

With the new method the net app developer has the option to request for location information for a device just once. No need to create subscriptions or maintain a local web server in order to get notified for location changes.
When a call to ``get_location_information`` is made, the 5G-API responds instantly with the location information (the cell id the device, that is being monitored, is connected to)

* Examples of usages have been updated
File location_subscriber_examples.py now showcases how the new method can be called

0.6.1 (2022-01-26)
------------------
* Added Pypi functionality to automate generate a new SDK pip package

0.6.0 (2021-06-12)
------------------
* Added QoSAwareness to SDK. A class that allows to establish and monitor Non-GBR and GBR QoS targets
* Support for the latest version of NEF  (v1.2.0)
* LocationSubscriber now only requires an external_id as user equipment identifier. IP_4 and IP_V6 have been removed from method create_subscription()


0.5.1 (2021-03-11)
------------------
* Added class LocationSubscriber to SDK. A class that allows to get location monitoring reports from the 5G-API
* Clean-up the code
* New cli_helper.py class created to improve the code
* cli.py class updated for better practices
* Added new command options to interact with the pipelines


0.1.9 (2021-20-09)
------------------
* Added version option to CLI
* Changed 'generate' command to point to EVOLVED-5G/template at Github
* Added template option to point to your user's template. Used in tests by default pointing at skolome/netapp-ckcutter-template


0.1.4 (2021-17-09)
------------------
* Added documentation to "generate" command
* Added documentation to readthedocs

0.1.1 (2021-07-08)
------------------
* Generate command more fleshed out
* Added more detailed pytests


0.1.0 (2021-06-30)
------------------
* First prototype implementation
