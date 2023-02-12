============
installation
============


1. Install the App
==================
Add ``jommerce.auth`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "jommerce.auth",
        # ...
    ]

2. Add the Middleware
=====================
Add ``jommerce.auth.middleware.AuthenticationMiddleware`` to your ``MIDDLEWARE`` setting:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        "jommerce.auth.middleware.AuthenticationMiddleware",
        # ...
    ]

3. Add the URLs
===============
Add auth URLs to your project's URLconf:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        # ...
        path('auth/', include('jommerce.auth.urls', namespace="auth")),
        # ...
    ]

This example uses the ``auth`` prefix, but you can use any prefix that
doesn't clash with your application's URLs.

.. warning::

    Delete ``django.contrib.auth`` from your ``INSTALLED_APPS`` setting.
