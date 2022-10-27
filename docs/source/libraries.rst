SDK - Libraries
===============


At the current release the SDK contains six classes

* **LocationSubscriber**: allows you to track devices and retrieve updates about their location.You can use LocationSubscriber to create subscriptions, where each one of them can be used to track a device.
* **QosAwareness**: allows you to request QoS from a set of standardized values for better service experience (Ex. TCP_BASED / LIVE Streaming / CONVERSATIONAL_VOICE etc). You can create subscriptions where each one of them has specific QoS parameters. A notification is sent back to the net-app if the QoS targets can no longer be full-filled.
* **ConnectionMonitor**: allows you to monitor devices in the 5G Network. You this class to p can retrieve notifications by the 5G Network for individual devices when connection is lost (for example the user device has not been connected to the 5G network for the past 10 seconds) or when connection is alive (for example the user device has been connected to the 5G network for the past 10 seconds).
* **CAPIFInvokerConnector** a low level class, that is used by the evolved-5G CLI in order to register NetApps to CAPIF
* **CAPIFExposerConnector** a low level class, that allows an Exposer (like the NEF emulator) to register to CAPIF
* **ServiceDiscoverer** allows NetApp developer to connect to CAPIF in order to discover services




Examples of usage /Have a look at the code
------------------------------------------
Have a look at the examples folder for code samples on how to use the SDK Library.

* `LocationSubscriber example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/location_subscriber_examples.py>`_

* `QosAwareness example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/qos_awereness_examples.py>`_

* `ConnectionMonitor example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/connection_monitor_examples.py>`_

* `CAPIFInvokerConnector example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/netapp_capif_connector_examples.py>`_

* `CAPIFExposerConnector example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/nef_capif_connector_examples.py>`_

* `ServiceDiscoverer example <https://github.com/EVOLVED-5G/SDK-CLI/blob/master/examples/nef_capif_connector_examples.py>`_


Prerequisites / How to start
----------------------------

Install the requirements_dev.txt

.. code-block:: console

   pip install -r requirements_dev.txt

Make sure you have initiated the NEF_EMULATOR at url :py:func:`http://localhost:8888` (See  `here <https://github.com/EVOLVED-5G/NEF_emulator>`_  for instructions),
you have logged in to the interface, clicked on the map and have started the simulation.

Make sure that your NetApp has been registered and onboarded to CAPIF. If this process is completed, then in the specified folder the following files should be present

    - ca.crt
    - capif_api_details.json
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
