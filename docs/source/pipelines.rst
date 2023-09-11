SDK - Pipelines
===============

This feature enables to run the pipelines from the SDK CLI. 
Hereafter, the examples on how to usage will be described.

Examples of usage
-----------------

.. code-block:: console

    evolved5g run-verification-tests --mode build --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD

.. code-block:: console

    evolved5g run-verification-tests --mode deploy --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD

.. code-block:: console

    evolved5g run-verification-tests --mode destroy --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD

.. code-block:: console

    evolved5g run-verification-tests --mode code_analysis --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD

.. code-block:: console

    evolved5g run-verification-tests --mode security_scan --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD

.. code-block:: console

    evolved5g run-verification-tests --mode capif_nef --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD --capifpath PATH_TO_CAPIF_REGISTRATION_JSON --certpath CERTIFICATES_FOLDER_STORE --verfpath FILE_TO_VERIFY

.. code-block:: console

    evolved5g run-verification-tests --mode capif_nef --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD --capifpath PATH_TO_CAPIF_REGISTRATION_JSON --certpath CERTIFICATES_FOLDER_STORE --verfpath FILE_TO_VERIFY

.. code-block:: console

    evolved5g validation --repo REPOSITORY_NAME --user USERNAME --passwd USER_PASSWORD --environment ENVIRONMENT_TO_DEPLOY

.. code-block:: console

    evolved5g check-job --id YOUR_ID --user USERNAME --passwd USER_PASSWORD

The verification pipelines (build, deploy, destroy, code_analysis, security_scan, capif_nef and capif_tsn) will return an **ID** which can be used with the command :py:func:`check-job` to see how the NetApp is performing.

Very important 
^^^^^^^^^^^^^^

Please check your NetApp repository has a branch **evolved5g**, otherwise the pipelines will fail.
