============
installation
============


1. Install the App
==================
Add ``jommerce.blog`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "jommerce.blog",
        # ...
    ]

2. Add the URLs
===============
Add blog URLs to your project's URLconf:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        # ...
        path('blog/', include('jommerce.blog.urls', namespace="blog")),
        # ...
    ]

This example uses the ``blog`` prefix, but you can use any prefix that
doesn't clash with your application's URLs.
