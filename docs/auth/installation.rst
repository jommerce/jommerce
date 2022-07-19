============
installation
============


1. Install the App
==================
Add ``"djplus.auth"`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "djplus.auth",
        # ...
    ]

2. Import default Settings
==========================
Add this line to the ``settings.py`` file:

.. code-block:: python

    from djplus.auth.settings import *


3. Add the URLs
===============
Add auth URLs to your project's URLconf:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        # ...
        path('auth/', include('djplus.auth.urls', namespace="auth")),
        # ...
    ]

This example uses the ``auth`` prefix, but you can use any prefix that
doesn't clash with your application's URLs.

4. Add the Middleware
=====================
Add ``"djplus.auth.middleware.AuthenticationMiddleware"`` to your ``MIDDLEWARE`` setting:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        "djplus.auth.middleware.AuthenticationMiddleware",
        # ...
    ]

