|Travis Badge|

**This library allows you to quickly and easily use the SendGrid Web API
via Python.**

Announcements
=============

**BREAKING CHANGE as of 2016.06.14**

Version ``3.X.X`` is a breaking change for the entire library.

Version 3.X.X brings you full support for all Web API v3 endpoints. We
have the following resources to get you started quickly:

-  `SendGrid
   Documentation <https://sendgrid.com/docs/API_Reference/Web_API_v3/index.html>`__
-  `Usage
   Documentation <https://github.com/sendgrid/sendgrid-python/tree/master/USAGE.md>`__
-  `Example
   Code <https://github.com/sendgrid/sendgrid-python/tree/master/examples>`__
-  `Migration from v2 to
   v3 <https://sendgrid.com/docs/Classroom/Send/v3_Mail_Send/how_to_migrate_from_v2_to_v3_mail_send.html>`__

Thank you for your continued support!

All updates to this library is documented in our
`CHANGELOG <https://github.com/sendgrid/sendgrid-python/blob/master/CHANGELOG.md>`__.

Installation
============

Setup Environment Variables
---------------------------

First, get your free SendGrid account
`here <https://sendgrid.com/free?source=sendgrid-python>`__.

Next, update your environment with your
`SENDGRID\_API\_KEY <https://app.sendgrid.com/settings/api_keys>`__.

.. code:: bash

    echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
    echo "sendgrid.env" >> .gitignore
    source ./sendgrid.env

Install Package
---------------

.. code:: bash

    pip install sendgrid

or

.. code:: bash

    easy_install sendgrid

Dependencies
------------

-  The SendGrid Service, starting at the `free
   level <https://sendgrid.com/free?source=sendgrid-python>`__)
-  `Python-HTTP-Client <https://github.com/sendgrid/python-http-client>`__

Quick Start
===========

Hello Email
-----------

.. code:: python

    import sendgrid
    import os
    from sendgrid.helpers.mail import *

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("test@example.com")
    subject = "Hello World from the SendGrid Python Library"
    to_email = Email("test@example.com")
    content = Content("text/plain", "some text here")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

General v3 Web API Usage
------------------------

.. code:: python

    import sendgrid
    import os

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.api_keys.get()
    print(response.status_code)
    print(response.body)
    print(response.headers)

Usage
=====

-  `SendGrid
   Documentation <https://sendgrid.com/docs/API_Reference/index.html>`__
-  `Usage
   Documentation <https://github.com/sendgrid/sendgrid-python/tree/master/USAGE.md>`__
-  `Example
   Code <https://github.com/sendgrid/sendgrid-python/tree/master/examples>`__
-  `v3 Web API Mail Send
   Helper <https://github.com/sendgrid/sendgrid-python/tree/master/sendgrid/helpers/mail>`__
   - build a request object payload for a v3 /mail/send API call.

Roadmap
-------

If you are intersted in the future direction of this project, please
take a look at our
`milestones <https://github.com/sendgrid/sendgrid-python/milestones>`__.
We would love to hear your feedback.

How to Contribute
-----------------

We encourage contribution to our libraries, please see our
`CONTRIBUTING <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md>`__
guide for details.

Quick links:

-  `Feature
   Request <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md#feature_request>`__
-  `Bug
   Reports <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md#submit_a_bug_report>`__
-  `Sign the CLA to Create a Pull
   Request <https://github.com/sendgrid/sendgrid-open-source-templates/tree/master/CONTRIBUTING.md#cla>`__
-  `Improvements to the
   Codebase <https://github.com/sendgrid/sendgrid-python/blob/master/CONTRIBUTING.md#improvements_to_the_codebase>`__

About
=====

sendgrid-python is guided and supported by the SendGrid `Developer
Experience Team <mailto:dx@sendgrid.com>`__.

sendgrid-python is maintained and funded by SendGrid, Inc. The names and
logos for sendgrid-python are trademarks of SendGrid, Inc.

|SendGrid Logo|

.. |SendGrid Logo| image:: https://uiux.s3.amazonaws.com/2016-logos/email-logoTuesday, July 12, 16 at 9:29:10 AM America/Los_Angeles.png
   :target: https://www.sendgrid.com

.. |Travis Badge| image:: https://travis-ci.org/sendgrid/sendgrid-python.svg?branch=master
   :target: https://travis-ci.org/sendgrid/sendgrid-python


