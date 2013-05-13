Django Multiple Include
======================================

A version of ``{% include %}`` that accepts multiple template names.

Usage
-----
::
    $ pip install django-multiple-include

Add ``multiple_include`` to ``INSTALLED_APPS``.

Then, in your template::

    {% load multiple_include %}

    {% multiple_include "template1.html" "template2.html" "template2.html" with object=item %}

The templatetag will include the first existing template from the list. This allows more interesting uses as::

    {% load multiple_include %}

    {% with "story_"|add:object.category_slug|add:".html" as category_template %}
    {% multiple_include category_template "news/story_default.html" %}
    {% endwith %}

Note: For a cleaner string concatenation, you can use the ``capture`` tag shipped with  `Django Basic Apps <https://github.com/nathanborror/django-basic-apps/>`_:

In your settings::

    INSTALLED_APPS += ('basic.tools')

Template::

    {% load multiple_include capture %}

    {% capture as category_template %}
        story_{{ object.category_slug}}.html
    {% endcapture %}

    {% multiple_include category_template "news/story_default.html" %}
