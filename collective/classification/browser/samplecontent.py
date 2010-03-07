from zope.schema.vocabulary import SimpleVocabulary
from zope import schema
from zope.interface import Interface
from nltk.corpus import brown
from zope.formlib import form
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName

brownCategories = SimpleVocabulary.fromValues(brown.categories())

class ISampleContent(Interface):
    no_items = schema.Int(
        title=u"Number of documents per category to import",
        required=True,
        max = 20
    )

    brown_categories = schema.List(
        title=u"Brown corpus categories to import",
        value_type=schema.Choice(vocabulary = brownCategories),
        required=True
    )

class SampleContentView(formbase.PageForm):
    """Imports content from the brown corpus for testing.
    """
    
    form_fields = form.Fields(ISampleContent)
    
    @form.action(u"Import sample content from brown corpus")
    def action_import(self, action, data):
        """
        """
        urltool = getToolByName(self.context, "portal_url")
        portal  = urltool.getPortalObject()
        folder = portal.invokeFactory('Folder','sample_content')
        folder = portal[folder]
        no_items = data['no_items']
        categories = data['brown_categories']
        for category in categories:
            for articleid in brown.fileids(categories=category)[:no_items]:
                text = " ".join(brown.words(articleid))
                folder.invokeFactory('Document',articleid,
                                    title=articleid,
                                    text=text,subject=category)