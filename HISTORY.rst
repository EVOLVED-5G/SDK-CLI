=======
History
=======


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
