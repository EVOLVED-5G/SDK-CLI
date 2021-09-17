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
    
For example run the following command, to have the repoName as "firstNetApp" and all other values as the default ones:
 
.. code-block:: console
 
    $ evolved5g generate --no-input -r firstNetApp