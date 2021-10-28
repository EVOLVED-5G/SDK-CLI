SDK - Libraries
===============

At the current release the SDK contains one class "**LocationSubscriber**"
that allows you to track devices and retrieve updates about their location.
You can use LocationSubscriber to create subscriptions, where each one of them can be used to track a device.

Examples of usage /Have a look at the code
------------------------------------------
Have a look at the examples folder for code samples on how to use the SDK Library.

`Location subscriber example <https://github.com/EVOLVED-5G/SDK-CLI/blob/libraries/examples/location_subscriber_examples.py>`_

Prerequisites / How to start
----------------------------

Install the requirements_dev.txt

    pip install -r requirements_dev.txt

Make sure you have initiated the NEF_EMULATOR at url http://localhost:8888 (See  `here <https://github.com/EVOLVED-5G/NEF_emulator>`_  for instructions),
you have logged in to the interface, clicked on the map and have started the simulation.

Then run a webserver in order to capture the callback post requests from NEF EMULATOR: On the terminal run the following commands to initialize the webserver.


    export FLASK_APP=/home/user/evolved-5g/SDK-CLI/examples/api.py

    export FLASK_ENV=development

    python -m flask run --host=0.0.0.0

where FLASK_APP should point to the absolute path of the SDK-CLI/examples/api.py file.
These commands will initialize a web server at http://127.0.0.1:5000/

Now you can run `Location subscriber example <https://github.com/EVOLVED-5G/SDK-CLI/blob/libraries/examples/location_subscriber_examples.py>`_
You should be able to view the location updates, printed in the terminal that runs the FLASK webserver
