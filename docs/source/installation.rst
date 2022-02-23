============
Installation
============

Stable release 
---------------

To install Evolved5G_CLI, please check you comply with the pre-requisites. Also, before running the installation command, please be sure to have the following software packages installed:

.. code-block:: console

    sudo apt update
    sudo apt install python3
    sudo apt install python3-pip python3-setuptools

Once you comply with the pre-requisites and the previous software packages, just run the following command in your terminal:

.. code-block:: console

    $ pip3 install evolved5g

This is the preferred method to install Evolved5G_CLI, as it will always install the most recent stable release.


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

    $ python3 setup.py install

Once it is installed you will be able to generate (create) a repository for your NetApp.

.. _Github repo: https://github.com/EVOLVED-5G/SDK-CLI
.. _tarball: https://github.com/EVOLVED-5G/SDK-CLI/tarball/master