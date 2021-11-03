*******************
Evolved5G CLI & SDK
*******************


.. image:: https://img.shields.io/pypi/v/evolved5g.svg
        :target: https://pypi.python.org/pypi/evolved5g


.. image:: https://readthedocs.org/projects/evolved5g_cli/badge/?version=latest
        :target: https://evolved5g_cli.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Evolved5G CLI prototype


* Free software: Apache Software License 2.0
* Documentation: https://evolved5g_cli.readthedocs.io.

========
Features
========

* Generate a new python NetApp from a template
* Assist in connecting the new NetApp & repo with EVOLVED-5G CI/CD pipeline
* SDK Libraries for interacting with the 5G-API
* Assist in running pipelines for NetApps

==================
Useful Information
==================

The purpose of this guide is to help developers, in the EVOLVED-5G project scope, to develop a NetApp.

First, the partner to be interested in developing a NetApp must send an email to evolved5g@gmail.com to receive access to the GitHub organization.

The email must contain the GitHub username to be added to the GitHub organization.

You will receive an invitation which you will have to accept in order to have owner permissions in this organisation, which can be found here: https://github.com/EVOLVED-5G

Once the developer has access to the organisation, he will want to create a new repository from a template. To do this, a template repository has been created and will be visible in the organisation, which contains a tool called Cookiecutter along with some Python scripts. With such scripts, the developer will be asked to introduce some inputs necessary in order to create a new repository, such repository will contain all the necessary folder and files for the creation/development of a NetApp.

First of all, in order to be able to work with Cookiecutter, it is mandatory to install it on your local computer or virtual machine. Below are the commands that should be executed to work with Cookiecutter (these commands have been tested under Ubuntu, but it is also possible to use this tool on Windows and Mac (to be checked)).

This guide has been developed to work with Ubuntu OS, so all the commands have been only tested under Ubuntu, if other OS will be used, please have in mind some of this command will differ.

==============
Pre-requisites
==============

To create a new repository within the EVOLVED-5G organization it is mandatory to create an SSH key since the communication with the repository will be through SSH connection, to create the SSH key can be done as follows:

.. code-block:: console

    ssh-keygen -t rsa

Some inputs will be asked, you just need to press enter to leave it by default.
If left as default the key pair generated can be found in the /home/ubuntu/.ssh directory of your ubuntu machine. To be able to work through SSH, you will need to copy the public key file you have generated and add it to your GitHub account, this can be done as follows:

.. code-block:: console

    cat ~/.ssh/id_rsa.pub

#. Copy the output to your clipboard 
#. In your GitHub account go to "Settings" (up right) and then you will see a tab called "SSH and GPG Keys"

.. image:: /docs/images/ssh_gpg.png

#. When you access this section, the first thing you will see is a button to create a new ssh key.

.. image:: /docs/images/ssh_key_button.png

#. Click on that button, and the following screen will appear: 

.. image:: /docs/images/ssh_key.png

As you can see in the example image above, you have to enter the public key you have previously generated on your machine and copied in the "Key" section and add a title to it if you want to have your key list more organized. Click on the "Add SSH Key" button and you will be able to work with GitHub via SSH.

Finally, before running the SDK tool, you need to create a Personal Access Token on Github. This is necessary because to create a new repository you need to be authorized to do so and this is achieved via a token. Below it is explained how to create this token in GitHub:

#. Go back to your profile, to the Settings section, but this time look for the "Developer settings" button and click on it to see the following:

.. image:: /docs/images/token1.png

#. As you can see in the image above, on that page there are three buttons, we choose to press “Personal access tokens”. And we will see the top right button "Generate new token". Click on this button and you will see the following page:

.. image:: /docs/images/token2.png

From the image you can add a note of what you want to use this token for, it is a matter of organization, as well as the days you want this token to last. Just below you will see that you are prompted to select the scope of the token, the recommendation is if you are going to use this token for the organization of EVOLVED-5G, select the maximum possible scope, i.e., select everything.
#. When you have selected the scope of your token, click on the "Generate token" button, copy the token when it appears and save it in a txt file or similar, because once you leave this page, you will only see a list of tokens with the name you have given, as you can see below:

.. image:: /docs/images/token3.png

It is very important to copy and save your personal access token because **you won’t be able to see it again.**
For more information about token creation please refer to `GitHub <https://docs.github.com/es/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_

When you have done all the actions shown above, you are ready to run the SDK tool from your terminal and generate a new repository and your NetApp.

============
Installation
============


Stable release (NOT YET INTEGRATED)
-----------------------------------

To install Evolved5G_CLI, run this command in your terminal:

.. code-block:: console

    sudo apt update
    supo apt install python3
    sudo apt install python3-setuptools
    pip install evolved5g

This is the preferred method to install Evolved5G_CLI, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Evolved5G_CLI can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    git clone git://github.com/EVOLVED-5G/SDK-CLI

Or download the `tarball`_:

.. code-block:: console

    curl -OJL https://github.com/EVOLVED-5G/SDK-CLI/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    python setup.py install

Once it is installed you will be able to generate (create) a repository for your NetApp.

.. _Github repo: https://github.com/EVOLVED-5G/SDK-CLI
.. _tarball: https://github.com/EVOLVED-5G/SDK-CLI/tarball/master

=========
CLI Usage
=========

Run the following command to access the documentation/help page and read about the various options

.. code-block:: console

    evolved5g

Generate
--------

To generate a new NetApp project run the following command. You will be asked for some inputs such as the repoName, packageName etc

.. code-block:: console

    evolved5g generate

or to learn more about the available options

.. code-block:: console

    evolved5g generate --help

If you get an error saying **cookiecutter command not found** please do set the correct PATH as following:

In Linux:

* Uninstall cookiecutter

* # Add ~/.local/ to PATH

* .. code-block:: console

    export PATH=$HOME/.local/bin:$PATH

* .. code-block:: console

    source ~/.bash_profile

* Install cookiecutter

In Windows:

.. code-block:: console

    > set PATH=%PATH%;C:\YOUR\PATH\

Then run the following command ssh -vT git@github.com to check the SSH connection is up and running without any problem.
If the command “evolved5g generate” does not give you any problem, then automatically will start to ask you some inputs to create your NetApp repository. At some point you will be asked if you want to add a collaborator, if you choose **NO**, you will receive two more inputs regarding this, please just ignore it, press enter leaving it by default, no further action will be taken, no collaborator will be added, it is a bug which will be fixed any time soon.

Finally, when this command is executed, you will see something like the following image, in which you have to enter the values requested, like the example you can see between brackets, for the execution to be completed:

.. image:: /docs/images/generate_execution.png

If you access GitHub once you have seen that output in your terminal, you will see that the repository has been successfully created:

.. image:: /docs/images/repo_creation.png

It will create a specific branch (evolved5g) which will be used by the CI/CD for verification purposes. A dummy example (nginx server) will be created in both branches (master and evolved5g) which allow to directly run a pipeline using such branch i.e., build (following TID instructions) and check that it works. You will see a Dockerfile and inside the src folder a dummy html file as an example. Below can see the file structure created.

.. image:: /docs/images/repo_structure.png
   

.. image:: /docs/images/dummy_html_example.png

When the repository is created you will be at branch evolved5g, so the push must be done there, in case you want to work with master (branch) you have to execute git checkout master and then do the push (git push -u origin master), to know in which branch you are, just execute git branch.

===============
SDK - Pipelines
===============

This feature enables to run the pipelines from the SDK CLI. 
Hereafter, the examples on how to usage will be described.

Examples of usage
-----------------

.. code-block:: console
    
    evolved5g run-pipeline --mode build --repo REPOSITORY_NAME

.. code-block:: console

    evolved5g run-pipeline --mode deploy --repo REPOSITORY_NAME

.. code-block:: console

    evolved5g run-pipeline --mode destroy --repo REPOSITORY_NAME


.. code-block:: console

    evolved5g check-pipeline --id YOUR_ID

The pipelines build, deploy or destroy will return an **ID** which can be used with the command *check_pipeline* to see how the NetApp is performing.

**IMPORTANT** 
-------------

Please check your NetApp repository has a branch **evolved5g**, otherwise the pipelines will fail.

===============
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

.. code-block:: console

    pip install -r requirements_dev.txt

Make sure you have initiated the NEF_EMULATOR at url http://localhost:8888 (See  `here <https://github.com/EVOLVED-5G/NEF_emulator>`_  for instructions),
you have logged in to the interface, clicked on the map and have started the simulation.
Then run a webserver in order to capture the callback post requests from NEF EMULATOR: On the terminal run the following commands to initiaze the webserver.

.. code-block:: console

    export FLASK_APP=/home/user/evolved-5g/SDK-CLI/examples/api.py

    export FLASK_ENV=development

    python -m flask run --host=0.0.0.0

where FLASK_APP should point to the absolute path of the SDK-CLI/examples/api.py file.
These commands will initialize a web server at http://127.0.0.1:5000/

Now you can run `Location subscriber example <https://github.com/EVOLVED-5G/SDK-CLI/blob/libraries/examples/location_subscriber_examples.py>`_
You should be able to view the location updates, printed in the terminal that runs the FLASK webserver

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
