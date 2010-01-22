Introduction
============

*qi.kb.classification* aims to provide a set of tools for automatic document
classification. Currently it makes use of the `Natural Language Toolkit`_ and
features a trainable document classifier based on Part Of Speech (POS)
tagging.

  .. _`Natural Language Toolkit`: http://www.nltk.org

What is this all about?
=======================

It's mostly about having fun! But you can do some useful things as well: On a large site with a lot of content and tags (or subjects in the plone lingo) it might be difficul

Installation
============

To get started you will simply need to add the package to your "eggs" and
"zcml" sections, run buildout, restart your Plone instance and install the
"qi.kb.classification" package using the quick-installer or via the "Add-on
Products" section in "Site Setup".

**WARNING: Upon first time installation linguistic data will be fetched from NLTK's repository and stored locally on your filesystem. It's about 225Mb, so not for the faint at disk space.**


