==========================================
Welcome to django-reviews's documentation!
==========================================

Installation
============

To install just do:

1. ``python setup.py install`` or ``easy_install django-reviews``

2. Add reviews to *INSTALLED_APPS*.

3. Add django-reviews' urls to urls.py

4. Add *django.core.context_processors.request* to *TEMPLATE_CONTEXT_PROCESSORS*
   (If it isn't already).

Settings
========

There are several settings which you can use within settings.py:

REVIEWS_IS_MODERATED

    If True the admin has to publish a review manually. Otherwise a review is
    public right after it has been added.

REVIEWS_SHOW_PREVIEW

    If True a preview is displayed to the user before he can submit the review.

REVIEWS_IS_EMAIL_REQUIRED

    If True the e-mail field of the review is mandatory. (if the user is anonymous)

REVIEWS_IS_NAME_REQUIRED

    If True the name field of the review is mandatory. (if the user is anonymous)

Usage
=====

Add the provided tags to your templates::

    {% load reviews_tags %}

    <html>
        <head>
            <title>{{ flatpage.title }}</title>
        </head>
        <body>
            {{ flatpage.content }}
            {% average_for_instance flatpage %}

            <hr>
            {% reviews_for_instance flatpage %}
        
        </body>
    </html>


Example
=======

There is a simple example provided with this product. 

To install it just make sure *django.contrib.flatpages* has been installed (a
flatpage will serve as our test content) and add reviews.example to 
*INSTALLED_APPS*.

Now add a flatpage and browse to it. You should be able to add reviews to the
flatpage now.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

