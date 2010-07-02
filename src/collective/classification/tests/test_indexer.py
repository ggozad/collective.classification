from Products.CMFCore.utils import getToolByName
from collective.classification.tests.base import ClassificationTestCase


class TestIndexer(ClassificationTestCase):
    """Tests the adapters for IATContentType
    """

    def test_indexer(self):
        """Creates an IATContentType and tests the catalog index
        """
        text = """
        Alice is sitting with her sister on the riverbank and is very bored.
        Suddenly she sees a White Rabbit running by her. It is wearing a
        waistcoat and takes a watch out of it, while muttering to himself 'Oh
        dear! Oh dear! I shall be late!'. Alice gets very curious and follows
        him down his rabbit-hole.

        The rabbit-hole suddenly goes straight down and Alice falls into it.
        She falls very slowly and while she is talking to herself she falls
        asleep. Suddenly she lands on a heap of sticks and dry leaves and the
        fall is over. She sees the White Rabbit running in front of her
        through a long passage and she continues to follow him.

        When she turns the corner the Rabbit is gone and Alice finds herself
        in a long, low hall, with doors all round it. She tries them, but
        they are all locked. Then she comes upon a little three-legged table
        on which a little golden key lies. The key fits in a little door
        behind a curtain and when she opens it she sees that it leads into a
        small passage. At the end of the passage Alice sees a beautiful
        garden. She really wants to get into the garden, but she is too big
        to fit through the door.

        When she goes back to the table she finds a little bottle on it with
        the words 'Drink me' printed on the label. Alice drinks from it and
        starts shrinking until she is only ten inches high. She now has the
        right size to enter the door, but she finds that the door is still
        locked and that she has left the little golden key on the table,
        which is now too high to reach.

        She starts crying, but soon sees a little glass box lying under the
        table containing a small cake marked with the words 'Eat me'. Hoping
        that this cake will make her grow or shrink too, she eats it.
        """

        self.folder.invokeFactory('Document', 'test',
                                  text=text,
                                  subject="A Subject")
        catalog = getToolByName(self.folder, 'portal_catalog')
        cr = catalog.searchResults(noun_terms="alice")
        self.failUnless(cr[0]['noun_terms'] ==\
                        ['alice', 'door', 'table', 'rabbit', 'passage'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIndexer))
    return suite
