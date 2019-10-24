.. _authentication:

.. highlight:: rst

.. role:: python(code)
    :language: python

.. role:: latex(code)
    :language: latex

==============
Authentication
==============

All access to Preseries.io needs to be authenticated. Authentication is performed by appending your username and Preseries API Key to the query string of every request. Click the link below to see an example of an authenticated API request which will list the companies.

    `https://{{project_name | lower}}.io/company?username=MY_NAME;api_key=1b90d33bd716bc4aee91f6750d6aaf3a5ab6e19b`

Your {{project_name | capfirst}} API Key is a unique identifier that is assigned exclusively to your account. Remember to keep your API key secret.

To use {{project_name | capfirst}}.io from the command line, we recommend setting your username and API key as environment variables. Using environment variables is also an easy way to keep your credentials out of your source code.

Copy and paste the snippet below in your terminal to make {{project_name | upper}}_AUTH ready to use.

.. code-block:: shell
   :linenos:
   :emphasize-lines: 3,5

    export PRESERIES_USERNAME=preseries_user
    export PRESERIES_API_KEY=1b90d33bd716bc4aee91f6750d6aaf3a5ab6e19b
    export PRESERIES_AUTH="username=$PRESERIES_USERNAME;api_key=$PRESERIES_API_KEY"

$ Setting Preseries_user's Authentication Parameters If you are a Windows command line user, use the following snippet instead:

.. code-block:: shell
   :linenos:

    set PRESERIES_USERNAME=preseries_user
    set PRESERIES_API_KEY=1b90d33bd716bc4aee91f6750d6aaf3a5ab6e19b
    set PRESERIES_AUTH=username^=%PRESERIES_USERNAME%;api_key^=%PRESERIES_API_KEY%

$ Setting Preseries_user's Authentication Parameters in Windows
Here is an example of an authenticated API request to list the companies from a command line.

.. code-block:: shell
   :linenos:

   curl "https://preseries.io/company?$PRESERIES_AUTH"


.. literalinclude:: ../crawler_11/api/views.py
   :language: python
   :pyobject: Crawler_11ResourceSearchViewSet


Alternative Keys

Alternative Keys allow you to give fine-grained access to your resources.
To create an alternative key you need to use the web interface. There you can define what resources an alternative key can access and what operations (i.e., create, list, retrieve, update or delete) are allowed with it. This is useful in scenarios where you want to grant different roles and privileges to different applications. For example, an application for the IT folks that collects data and creates sources in BigML, another that is accessed by data scientists to create and evaluate models, and a third that is used by the marketing folks to create predictions.

You can read more about alternative keys here.

Now here are latex command :latex:`\\setlength` and python command
:python:`import`, created by ``:python:`import```.  Here is a
:literal:`literal`, which stays a literal, and
:code:`.. highlight:: rst` makes code role look as it looks.
