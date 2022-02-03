SDK - Pipelines
===============

This feature enables to run the pipelines from the SDK CLI. 
Hereafter, the examples on how to usage will be described.

Examples of usage
-----------------

.. code-block:: console

    evolved5g run_pipeline --mode build --repo REPOSITORY_NAME

.. code-block:: console

    evolved5g run_pipeline --mode deploy --repo REPOSITORY_NAME

.. code-block:: console

    evolved5g run_pipeline --mode destroy --repo REPOSITORY_NAME

.. code-block:: console

    evolved5g check_pipeline --id YOUR_ID

The pipelines build, deploy or destroy will return an **ID** which can be used with the command :py:func:`check_pipeline` to see how the NetApp is performing.

Very important 
^^^^^^^^^^^^^^

Please check your NetApp repository has a branch **evolved5g**, otherwise the pipelines will fail.