Introduction
============

*collective.classification* aims to provide a set of tools for automatic
document classification. Currently it makes use of the
`Natural Language Toolkit`_ and features a trainable document classifier based
on Part Of Speech (POS) tagging, heavily influenced by `topia.termextract`_.
This is not a finished product and is intended to be used for experimentation
and development.

  .. _`Natural Language Toolkit`: http://www.nltk.org
  .. _`topia.termextract`: http://pypi.python.org/pypi/topia.termextract/

What is this all about?
=======================

It's mostly about having fun! The package is in a very early experimental
stage and awaits eagerly contributions. You will get a good understanding of
what works or not by looking at the tests. You might also be able to do some
useful things with it: On a large site with a lot of content and tags (or
subjects in the plone lingo) it might be difficult to assign tags to new
content. In this case, a trained classifier could provide useful suggestions
to an editor responsible for tagging content.

How it works?
=============

At the moment there exist the following type of utilities:

  * *POS taggers*, utilities for classifying words in a document
    as `Parts Of Speech`_. Two are provided at the moment, a Penn TreeBank
    tagger and a trigram tagger. Both can be trained with some other language
    than english which is what we do here.
  * *Term extractors*, utilities responsible for extracting the important
    terms from some document. The extractor we use here, assumes that in a
    document only nouns matter and uses a POS tagger to find those mostly used
    in a document. For details please look at the code and the tests.

  * *Content classifiers*, utilities that can tag content in predefined
    categories. Here, a `naive Bayes`_ classifier is used. Basically, the
    classifier looks at already tagged content, performs term extraction and
    trains itself using the terms and tags as an input. Then, for new content,
    the classifier will provide suggestions for tags according to the
    extracted terms of the content.
  * *Clusterers*, utilities that without prior knowledge of content
    classification can group content into groups according to feature
    similarity. At the moment NLTK's `k-means`_ clusterer is used.


  .. _`Parts Of Speech`: http://en.wikipedia.org/wiki/Part-of-speech_tagging
  .. _`naive Bayes`: http://en.wikipedia.org/wiki/Naive_Bayes_classifier
  .. _`k-means`: http://en.wikipedia.org/wiki/K-means_clustering

Installation & Setup
====================

Before running buildout, make sure you have yaml and its python bindings
installed (use macports on osx, or your package installer on linux). If nltk
exists for your OS you might as well install that, otherwise it will be
fetched when you run buildout.

To get started you will simply need to add the package to your "eggs" and
"zcml" sections, run buildout, restart your Plone instance and install the
"collective.classification" package using the quick-installer or via the
"Add-on Products" section in "Site Setup".

**WARNING: Upon first time installation linguistic data will be fetched from
NLTK's repository and stored locally on your filesystem. It's about 225Mb, so
not for the faint at disk space.**

After installation, you should have a control panel entry to configure the product.

  * By default the product uses the Pen TreeBank tagger who is not very
    performant. It is a good idea to go to the term extractor configuration
    and change it so as to use an N-Gram tagger. Among the brown corpus
    categories choose the ones that seem to fit better with your content.
    Train the tagger. This will look for *all* content and perform term
    extraction. So go grab yourself something to drink, it will take a while.
  * After training the tagger, train the classifier. This will look for any
    content that is tagged and train the Bayes classifier.
  * By default the classifier does get re-trained every time content is
    added or updated. If you do not want this to happen automatically (that is
    if you have a site with a lot of content, and things get slow), in the
    control panel you can disable auto-training.

How to use it?
==============

  * In order to use the classifier and get suggested tags for some content,
    you can call *@@subjectsuggest* on the content. This comes down to
    appending @@subjectsuggest to the url in your browser. A form will come up
    with
    suggestions, choose the ones that seem appropriate and apply. You will
    need to have the right to edit the document in order to call the view.
  * For clustering you can just call the *@@clusterize* view from anywhere.
    The result is not deterministic but hopefully helpful;). You need manager
    rights for this so as to not allow your users to DOS your site!

