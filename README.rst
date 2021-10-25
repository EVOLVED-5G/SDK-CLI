*************
Evolved5G_CLI
*************


.. image:: https://img.shields.io/pypi/v/evolved5g.svg
        :target: https://pypi.python.org/pypi/evolved5g


.. image:: https://readthedocs.org/projects/evolved5g_cli/badge/?version=latest
        :target: https://evolved5g_cli.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Evolved5G CLI prototype


* Free software: Apache Software License 2.0
* Documentation: https://evolved5g_cli.readthedocs.io.

=============
Features
=============

* Generate a new python NetApp from a template
* Assist in connecting the new NetApp & repo with EVOLVED-5G CI/CD pipeline

============
Installation
============


Stable release (NOT YET INTEGRATED)
-----------------------------------

To install Evolved5G_CLI, run this command in your terminal:

.. code-block:: console

    $ pip install evolved5g

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

    $ git clone git://github.com/EVOLVED-5G/SDK-CLI

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/EVOLVED-5G/SDK-CLI/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/EVOLVED-5G/SDK-CLI
.. _tarball: https://github.com/EVOLVED-5G/SDK-CLI/tarball/master

============
Usage
============


Run the following command to access the documentation/help page and read about the various options

.. code-block:: console

    $ evolved5g

Generate
------------

To generate a new NetApp project run the following command. You will be asked for some inputs such as the repoName, packageName etc

.. code-block:: console

    $ evolved5g generate

or to learn more about the available options

.. code-block:: console

    $ evolved5g generate --help


============
Running the examples
============

This repository displays examples on how to use the evolved-5G SKD and CLI.
See project folder examples for user cases.
Install the requirements_dev.txt
.. code-block:: console
    pip install -r requirements_dev.txt

- Make sure initiated the NEF_EMULATOR at url http://localhost:8888 (See https://github.com/EVOLVED-5G/NEF_emulator for instructions)
- Run a webserver in order to capture the callback post requests from NET EMULATOR
On the terminal run the following commands to initiaze the webserver.
Make sure you set the correct path to the examples/api.py file
.. code-block:: console
    export FLASK_APP=/home/user/evolved-5g/SDK-CLI/examples/api.py

    export FLASK_ENV=development

    python -m flask run

This will initialize a web server at http://127.0.0.1:5000/
Opening it should display a message "echo evolved5G web server started"

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
