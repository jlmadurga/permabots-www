Permabots
==============================

.. image:: https://travis-ci.org/jlmadurga/permabots.svg?branch=master
    :target: https://travis-ci.org/jlmadurga/permabots

.. image:: https://coveralls.io/repos/github/jlmadurga/permabots/badge.svg?branch=master 
	:target: https://coveralls.io/github/jlmadurga/permabots?branch=master
  
.. image:: https://requires.io/github/jlmadurga/permabots/requirements.svg?branch=master
     :target: https://requires.io/github/jlmadurga/permabots/requirements/?branch=master
     :alt: Requirements Status

Connect bots with your apis


LICENSE: MIT


Basic Commands
--------------

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd permabots
    celery -A permabots.taskapp worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

