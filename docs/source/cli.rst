============
SDK - usage
============

Once the SDK is installed (:py:ref:`Installation<Installation>`) is installed you will be able to generate (create) a repository for your NetApp.
To know how to perform the different options available in the SDK, run the following command:

.. code-block:: console

    $ evolved5g

A help message will be shown, explaining the commands to execute.

Generate
------------

To generate a new NetApp repository run the following command.

.. code-block:: console

    $ evolved5g generate --config-file <path to the user configuration file>

You will need to pass a config (yaml) file with some inputs. You have to create your own yaml file as same as the one in the SDK-CLI repository, that can be found here: https://github.com/EVOLVED-5G/SDK-CLI/blob/master/evolved5g/my-custom-config.yaml

The help command, will show you how other available options

.. code-block:: console

    $ evolved5g generate --help

If you get an error saying **cookiecutter command not found** please do set the correct PATH as following:

In Linux:

* Uninstall cookiecutter

* # Add ~/.local/ to PATH

* .. code-block:: console

    $ export PATH=$HOME/.local/bin:$PATH

* .. code-block:: console

    $ source ~/.bash_profile

* Install cookiecutter

In Windows:

.. code-block:: console

    > set PATH=%PATH%;C:\YOUR\PATH\

Then run the following command ssh -vT git@github.com to check the SSH connection is up and running without any problem.

Now, you can execute ``evolved5g generate --config-file <path-to-your-config.yaml>`` providing the path of your yaml file.

.. only:: html

   .. figure:: images/generate.gif

Then the repository is created in your local computer as well as remotely in GitHub.

   .. figure:: images/netapp_creation.gif

If you go to https://github.com/EVOLVED-5G you will see that the repository has been successfully created:

   .. image:: images/repo_creation.png

It will create a specific branch (evolved5g) which will be used by the CI/CD for verification and validation purposes. An example is provided in master branch. You will see the src folder with a docker compose and a script (run.sh) to launch the Network App.
It is important to remind that in order to have a fully functional example, it is mandatory to have NEF and CAPIF already up and running in your machine/container. Below can see the file structure created.

   .. image:: images/repo_structure.png

   .. figure:: images/netapp_repo.gif