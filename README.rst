*******************
Evolved5G CLI & SDK
*******************


.. image:: https://img.shields.io/pypi/v/evolved5g.svg
        :target: https://pypi.python.org/pypi/evolved5g


.. image:: https://readthedocs.org/projects/evolved5g_cli/badge/?version=latest
        :target: https://evolved5g_cli.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


* Free software: Apache Software License 2.0

========
Features
========

* Generate a new python NetApp from a template
* Assist in connecting the new NetApp & repo with EVOLVED-5G CI/CD pipeline
* SDK Libraries for interacting with the 5G-API
* Assist in running verification pipelines for NetApps

==================
Useful Information
==================

The purpose of this guide is to help developers, in the EVOLVED-5G project scope, to develop a NetApp.

First, the partner to be interested in developing a NetApp must send an email to approval@evolved-5g.eu to receive access to the GitHub organization.

The email must contain the GitHub username to be added to the GitHub organization.

You will receive an invitation which you will have to accept in order to have owner permissions in this organisation, which can be found here: https://github.com/EVOLVED-5G

Once the developer has access to the organisation, he will want to create a new repository from a template. To do this, a template repository has been created and will be visible in the organisation, which contains a tool called Cookiecutter along with some Python scripts. With such scripts, the developer will be asked to introduce some inputs necessary in order to create a new repository, such repository will contain all the necessary folder and files for the creation/development of a NetApp.

First of all, in order to be able to work with Cookiecutter, it is mandatory to install it on your local computer or virtual machine. Below are the commands that should be executed to work with Cookiecutter (these commands have been tested under Ubuntu, but it is also possible to use this tool on Windows and Mac (to be checked)).

This guide has been developed to work with Ubuntu OS, so all the commands have been only tested under Ubuntu, if other OS will be used, please have in mind some of this command will differ.

To install and use the tool, please refer to:

* Documentation: https://evolved5g-cli.readthedocs.io
