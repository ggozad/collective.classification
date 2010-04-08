from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form
from zope import schema
from zope.interface import Interface
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName
from collective.classification import ClassificationMessageFactory as _
from collective.classification.classifiers.clustering import KMeans

class IClusterize(Interface):
    """
    """
    
    no_clusters = schema.Int(
        title = _(u"Number of clusters"),
        description = _(u""),
        required = True,
    )

    no_noun_ranks = schema.Int(
        title=_(u"Important nouns to keep"),
        description=_(u"Indicates how many nouns to keep when building the" \
            "list of most frequent nouns in the text."),
        default=20,
        required=True)

    repeats = schema.Int(
        title = _(u"Number of runs"),
        description = _(u""),
        default = 10,
        required = True,
    )

class ClusterizeView(formbase.PageForm):
    """
    """

    form_fields = form.Fields(IClusterize)
    template = ViewPageTemplateFile('clusterize.pt')

    @form.action(_(u"Clusterize"))
    def action_clusterize(self, action, data):
        """
        """
        catalog = getToolByName(self.context,'portal_catalog')
        clusterer = KMeans()
        clusters = clusterer.clusterize(
            data['no_clusters'],
            data['no_noun_ranks'],
            repeats=data['repeats'])
        result = []
        for cluster in clusters.values():
            clusterlist = []
            for uid in cluster:
                item = catalog.searchResults(UID=uid)[0]
                clusterlist.append(
                    (item.getURL(),
                     item.Title,
                     item.Description))
            result.append(clusterlist)
        self.clusters = result