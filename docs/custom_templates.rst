================
Custom templates
================
We have listed the path of html files here that you can customize by creating that file in that path,
and we have explained to each one where it is used?

.. |br| raw:: html

    <br>

base.html
---------

This is a **base** template and all other templates inherit from this file.
In this template, code only once and use it everywhere. (**Don't repeat yourself**)

If you want to extend our default base template,
you can do this by adding this line of code to the base template::

    {% extends 'jommerce/base.html' %}

.. literalinclude:: ../jommerce/templates/jommerce/base.html
    :language: html
    :linenos:
    :caption: jommerce/base.html

What are each of these blocks used for?                                         |br|
``{% block head_extra %}``  To add code to the head section ``{% endblock %}``  |br|
``{% block body_extra %}``  To add code to the body section ``{% endblock %}``  |br|
``{% block body_class %}``  To add classes to the body tag ``{% endblock %}``   |br|
``{% block css %}``  To add external css links or style tags ``{% endblock %}`` |br|
``{% block js %}``  To add external js links or script tags ``{% endblock %}``  |br|
``{% block content %}``  content section ``{% endblock %}``                     |br|
``{% block header %}``  header section ``{% endblock %}``                       |br|
``{% block footer %}``  footer section ``{% endblock %}``                       |br|


pages/home.html
---------------
This is a template for **home page**.
