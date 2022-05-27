=======
History
=======
0.7.4  (2022-05-27)
-------------------
* Check if the NetApp repository on which you want to run the pipeline exists on GitH

0.7.3  (2022-05-09)
-------------------
* Bug fix on value LIVE_STREAMING of enum  NonGBRQosReference.
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
