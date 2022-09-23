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

If you access GitHub once you have seen that output in your terminal, you will see that the repository has been successfully created:

   .. image:: images/repo_creation.png

It will create a specific branch (evolved5g) which will be used by the CI/CD for verification purposes. A dummy example will be created in both branches (master and evolved5g) which allow to directly run a pipeline using such branch. You will see a Dockerfile and inside the src folder a dummy html file as an example. Below can see the file structure created.

   .. image:: images/repo_structure.png


   .. image:: images/dummy_html_example.png

When the repository is created you will be at branch evolved5g, so the push must be done there, in case you want to work with master (branch) you have to execute git checkout master and then do the push ``git push -u origin master``, to know in which branch you are, just execute git branch.
