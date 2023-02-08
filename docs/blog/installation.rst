============
installation
============


1. Install the App
==================
Add ``dj.blog`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "dj.blog",
        # ...
    ]

2. Add the URLs
===============
Add blog URLs to your project's URLconf:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        # ...
        path('blog/', include('dj.blog.urls', namespace="blog")),
        # ...
    ]

This example uses the ``blog`` prefix, but you can use any prefix that
doesn't clash with your application's URLs.
