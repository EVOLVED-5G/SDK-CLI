SDK - Libraries
===============


At the current release the SDK contains six classes

* **LocationSubscriber**: allows you to track devices and retrieve updates about their location.You can use LocationSubscriber to create subscriptions, where each one of them can be used to track a device.
* **QosAwareness**: allows you to request QoS from a set of standardized values for better service experience (Ex. TCP_BASED / LIVE Streaming / CONVERSATIONAL_VOICE etc). You can create subscriptions where each one of them has specific QoS parameters. A notification is sent back to the net-app if the QoS targets can no longer be full-filled.
* **ConnectionMonitor**: allows you to monitor devices in the 5G Network. You can use this class to retrieve notifications by the 5G Network for individual devices when connection is lost (for example the user device has not been connected to the 5G network for the past 10 seconds) or when connection is alive.
* **TSNManager** allows Network App developers to apply Time-Sensitive Networking (TSN) standards to time-sensitive NetApps. Allows the configuration of certain parameters in the underlying TSN infrastructure of the testbed.
* **CAPIFInvokerConnector** a low level class, that is used by the evolved-5G CLI in order to register NetApps to CAPIF
* **ServiceDiscoverer** allows Network App developers to connect to CAPIF in order to discover services. It's also used internally within the SDK in order to get access token from CAPIF before interacting with services like NEF or CAPIF.
* **CAPIFProviderConnector** a low level class, that allows an Exposer (like the NEF emulator or the TSN emulator) to register to CAPIF
* **CAPIFLogger**, that allows an API provider (like NEF Emulator) to save Log information, for example capture incoming requests and responses
* **CAPIFAuditor**, that allows an API provider (like NEF Emulator) to query the Log, for example filter all the Log information for a given Network APP



Examples of usage /Have a look at the code
------------------------------------------
Have a look at the examples folder for code samples on how to use the SDK Library.

* `LocationSubscriber example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/location_subscriber_examples.py>`_

* `QosAwareness example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/qos_awereness_examples.py>`_

* `ConnectionMonitor example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/connection_monitor_examples.py>`_

* `CAPIFInvokerConnector example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/netapp_capif_connector_examples.py>`_

* `CAPIFProviderConnector example for NEF <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/nef_capif_connector_examples.py>`_

* `CAPIFProviderConnector example for TSN <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/tsn_capif_connector_examples.py>`_

* `ServiceDiscoverer example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/netapp_service_discovery_examples.py>`_

* `TSNManager example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/tsn_manager_examples.py>`_

* `CAPIFLogger example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/nef_logger_and_audit_example.py>`_

* `CAPIFAuditor  example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/nef_logger_and_audit_example.py>`_


Prerequisites / How to start
----------------------------

Install the requirements_dev.txt

.. code-block:: console

   pip install evolved-5g

Make sure you have initiated the CAPIF server  (See  `here <https://github.com/EVOLVED-5G/CAPIF_API_Services>`_ for instructions).

Make sure you have initiated the TSN server  (See  `here <https://github.com/EVOLVED-5G/TSN_AF>`_ for instructions). TSN Server is required if you are using the **TSNManager** class in your code

Make sure you have initiated the NEF_EMULATOR at url (See  `here <https://github.com/EVOLVED-5G/NEF_emulator>`_  for instructions),
you have logged in to the interface, clicked on the map and have started the simulation. NEF Enumalator is required if you are using **LocationSubscriber** ,**QosAwareness** ,**ConnectionMonitor** in your code

Make sure that your Network App has been registered and onboarded to CAPIF. If this process is completed, then in the specified folder the following files should be present

    - ca.crt
    - capif_api_security_context_details.json
    - private.key
    - your_common_name_you_specified.crt

Then run a webserver in order to capture the callback post requests from NEF EMULATOR: On the terminal run the following commands to initialize the webserver.


.. code-block:: console

   export FLASK_APP=/home/user/evolved-5g/SDK-CLI/examples/api.py

.. code-block:: console

   export FLASK_ENV=development

.. code-block:: console

   python -m flask run --host=0.0.0.0

where FLASK_APP should point to the absolute path of the ``SDK-CLI/examples/api.py`` file.
These commands will initialize a web server at :py:func:`http://127.0.0.1:5000/`

Now you can run the
`Location subscriber example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/location_subscriber_examples.py>`_
(you should be able to view the location updates, printed in the terminal that runs the FLASK webserver)
or the
`QosAwereness example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/qos_awereness_examples.py>`_
(you should be able to retrieve notifications when the QoS thresholds can not be achieved, or have been restored)
or the  `ConnectionMonitor example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/connection_monitor_examples.py>`_
(you should be able to retrieve notifications when user devices connect or disconnect to the netowrk,  printed in the terminal that runs the FLASK webserver)




LocationSubscriber Library
----------------------------

Overview
###################
LocationSubscriber library has two methods. The first one allows you to create a subscription in order to track a given device (retrieve notifications every time it connects to a different cell)

.. code-block:: console

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    netapp_id = "myNetapp"
    location_subscriber = LocationSubscriber(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                             capif_host=emulator_utils.get_capif_host(),
                                             capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon. There you can retrieve the id
    external_id = "10003@domain.com"

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand

    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback



The second one allows you to immediately retrieve the Location information for a given device

.. code-block:: console

   netapp_id = "myNetapp"
    location_subscriber = LocationSubscriber(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                             capif_host=emulator_utils.get_capif_host(),
                                             capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon. There you can retrieve the id
    external_id = "10003@domain.com"

    location_info = location_subscriber.get_location_information(
        netapp_id=netapp_id,
        external_id=external_id
    )
    print(location_info)

Have a look at the related `example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/location_subscriber_examples.py>`_ to understand how it works


Prerequisite
###################
❗ Make sure you have initiated the CAPIF server and the NEF emulator to use this class


ConnectionMonitor Library
----------------------------

Overview
###################
ConnectionMonitor library supports two events as described briefly above. The first event is the loss of connectivity event where the network detects that a UE is no longer reachable for either signalling or user plane communication. The Network App may provide a Maximum Detection Time, which indicates the maximum period of time without any communication with the UE (after the UE is considered to be unreachable by the network). The respective monitoring type enumeration and the maximum detection time parameter are shown below:

.. code-block:: console

   subscription_when_not_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED,
        wait_time_before_sending_notification_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time

The second event is the ue reachability event where the network detects when the UE becomes reachable (for sending downlink data or SMS to the UE). The monitoring type enumeration is shown below:

.. code-block:: console

   subscription_when_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://172.17.0.1:5000/monitoring/callback",
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED,
        wait_time_before_sending_notification_in_seconds=5,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time

Have a look at the related `example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/connection_monitor_examples.py>`_ to understand how it works


Prerequisite
###################
❗ Make sure you have initiated the CAPIF server and the NEF emulator to use this class

❗An important prerequisite for the loss of connectivity event (INFORM_WHEN_NOT_CONNECTED) is that while a Network App successfully receives the callback notification from the NEF Emulator, subsequently NEF expects an ``HTTP Response`` with the ``JSON`` content shown below:

.. code-block:: console

   {"ack" : "TRUE"}

As a result, the developer should ensure that in the endpoint that is responsible for receiving the callback notifications (HTTP POST requests) from NEF, Network App always returns the aforementioned acknowledgement, in ``JSON`` format.


QosAwareness Library
----------------------------

Overview
###################
QosAwareness library has two methods.
The first one allows you to create a subscription in order in order to establish
a Guaranteed Bit Rate (NON-GBR) QoS session and retrieve alerts if the network can't guarantee the conditions you have specified

.. code-block:: console

   """
        This example showcases how you can create a subscription to the 5G-API in order to establish
        a Guaranteed Bit Rate (NON-GBR) QoS.

        In order to run this example, to follow the instructions in  readme.md (https://evolved5g-cli.readthedocs.io/en/latest/libraries.html) in order to
        a) run the CAPIF server (this should run always first, because NEF in step b) has to communicate with NEF)
        b) run the NEF emulator
        c) connect your NetAPP to the CAPIF server (you have to do this only once)
        d) run a local webserver that will print the notifications it retrieves from the emulator. A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """
    netapp_id = "myNetapp"

    qos_awereness = QosAwareness(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                 folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                 capif_host=emulator_utils.get_capif_host(),
                                 capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator.
    # Go to the Map and hover over a User icon.There you can retrieve the id address.
    # Notice that the NEF emulator is able to establish a guaranteed bit rate only if one and only one user is connected to a shell
    # This is done in purpose in the NEF emulator, to allow testing the lost of guaranteed connectivity to your code
    # in the NEF if a user "10.0.0.3" is connected to Cell only by her self (she is the only connection within range)
    # the NEF guarantees the connection. If another user walks by, within the same Cell range then the connection is no
    # more guaranteed and a callback notification will be retrieved.
    equipment_network_identifier = "10.0.0.3"
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    conversational_voice = QosAwareness.GBRQosReference.CONVERSATIONAL_VOICE
    # In this scenario we monitor UPLINK
    uplink = QosAwareness.QosMonitoringParameter.UPLINK
    # Minimum delay of data package during uplink, in milliseconds
    uplink_threshold = 20
    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration= None, # not supported
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152
    notification_destination="http://172.17.0.1:5000/monitoring/callback"


    subscription = qos_awereness.create_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        gbr_qos_reference=conversational_voice,
        usage_threshold=usage_threshold,
        qos_monitoring_parameter=uplink,
        threshold=uplink_threshold,
        # BREAKING CHANGE. At version v0.8.0 this parameter is removed!
        # wait_time_between_reports=10
        # You need to declare it as the following
        reporting_mode= QosAwareness.EventTriggeredReportingConfiguration(wait_time_in_seconds=10)
        # You can now choose also the PeriodicReportConfiguration for reporting mode
        #reporting_mode= QosAwareness.PeriodicReportConfiguration(repetition_period_in_seconds=10)

    )
    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback
    # every time:
    # a) two users connect to the same cell at the same time  (which is how NEF simulates loss of GBT), or
    # b) when Usage threshold is exceeded(notice this is not supported by the NEF, so you will never retrieve this notification while testing with the NEF)



The second one allows you to create a subscription in order in order to establish
 a Non-Guaranteed Bit Rate (NON-GBR) QoS and retrieve alerts if the network can't guarantee the conditions you have specified


.. code-block:: console

   """
    This example showcases how you can create a subscription to the 5G-API in order to establish
    a Non-Guaranteed Bit Rate (NON-GBR) QoS.


    In order to run this example you need to follow the instructions in  readme.md in order to a) run the NEF emulator
    and b) run a local webserver that will print the location notifications it retrieves from the emulator.
    A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    netapp_id = "myNetapp"
    qos_awereness = QosAwareness(nef_url=emulator_utils.get_url_of_the_nef_emulator(),
                                 folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
                                 capif_host=emulator_utils.get_capif_host(),
                                 capif_https_port=emulator_utils.get_capif_https_port())
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and hover over a User icon.
    # There you can retrieve the id address
    equipment_network_identifier = "10.0.0.3"
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    qos_reference = QosAwareness.NonGBRQosReference.LIVE_STREAMING

    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes. 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration=None,  # not supported
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152
    notification_destination="http://172.17.0.1:5000/monitoring/callback"

    subscription = qos_awereness.create_non_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        non_gbr_qos_reference=qos_reference,
        usage_threshold=usage_threshold
    )
    # From now on we should retrieve POST notifications to http://172.17.0.1:5000/monitoring/callback

    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ----")
    print(subscription)

Have a look at the related `example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/qos_awereness_examples.py>`_ to understand how it works

Prerequisite
###################
❗ Make sure you have initiated the CAPIF server and the NEF emulator to use this class


TSNManager Library
----------------------------

Overview
###################
TSNManager library has methods  in order to

1) Get TSN profiles


.. code-block:: console

    """
    Demonstrates how to retrieve information on all the available TSN profiles
    """
    profiles = tsn.get_tsn_profiles()
    print(f"Found {len(profiles)} profiles")
    for profile in profiles:
        profile_configuration = profile.get_configuration_for_tsn_profile()

        print(
            f"Profile {profile.name} with configuration parameters { profile_configuration.get_profile_configuration_parameters()}"
        )


2) Apply profile changes


.. code-block:: console

    """
    Demonstrates how to apply a TSN profile configuration to a NetApp
    """
    profiles = tsn.get_tsn_profiles()
    # For demonstration purposes,  let's select the last profile to apply,
    profile_to_apply = profiles[-1]
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
    # Let's create an TSN identifier for this Net App.
    # This tsn_netapp_identifier can be used in two scenarios
    # a) When you want to apply a profile configuration for your net app
    # b) When you want to clear a profile configuration for your net app
    tsn_netapp_identifier = tsn.TSNNetappIdentifier(netapp_name=netapp_name)


    print(
        f"Generated TSN traffic identifier for Netapp: {tsn_netapp_identifier.value}"
    )
    print(
        f"Apply {profile_to_apply.name} with configuration parameters"
        f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {netapp_name} "
    )
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply, tsn_netapp_identifier=tsn_netapp_identifier
    )
    print(
        f"The profile configuration has been applied to the netapp. The returned token {clearance_token} can be used "
        f"to reset the configuration"
    )

    return (tsn_netapp_identifier,clearance_token)


3) Clear profile configuration


.. code-block:: console

    """
    Demonstrates how to clear a previously applied TSN profile configuration from a NetApp
    """
    tsn.clear_profile_for_tsn_netapp_identifier(tsn_netapp_identifier,clearance_token)
    print(f"Cleared TSN configuration from {netapp_name}")



4) Override parameters


.. code-block:: console

    """
    Demonstrates how to override the parameters of a TSN profile and apply it to a NetApp.
    """

    profiles = tsn.get_tsn_profiles()
    # For demonstration purposes,  let's select the first profile to apply,
    profile_to_apply = profiles[-1]
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
    profile_parameters = profile_configuration.get_profile_configuration_parameters()

    for parameter, value in profile_parameters.items():
        # For this example we retrieve the existing profile parameters
        # if this parameter is boolean, we just reverse it (so True parameters become False, or False parameters become True)
        profile_parameters[parameter] = not value if isinstance(value, bool) else value

    tsn_netapp_identifier = tsn.TSNNetappIdentifier(netapp_name=netapp_name)


    print(
        f"Generated TSN traffic identifier for Netapp: {tsn_netapp_identifier.value}"
    )
    print(
        f"Apply {profile_to_apply.name} with configuration parameters"
        f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {netapp_name} "
    )
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply,
        tsn_netapp_identifier=tsn_netapp_identifier
    )
    print(
        f"The profile configuration has been applied to the netapp. The returned token {clearance_token} can be used "
        f"to reset the configuration\n"
    )

    return (tsn_netapp_identifier,clearance_token)


Have a look at the related `example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/tsn_manager_examples.py>`_ to understand how it works


Prerequisite
###################
❗ Make sure you have initiated the CAPIF server and the TSN server to use this class

