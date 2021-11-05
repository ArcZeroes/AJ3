from pageRank import Page, Internet
import unittest

class PageTest(unittest.TestCase):
    def setUp(self):
        self.DELTA = 0.00000000000000000000000000000000000000000000005
            #Version 1
        self.pageA1 = Page("A1", 1)
        self.pageB1 = Page("B1", 1)
        self.pageA1.setEingehendeLinks(self.pageB1)
        self.pageB1.setEingehendeLinks(self.pageA1)

        self.internet1 = Internet(self.DELTA, [self.pageA1, self.pageB1])

        #Version 2
        self.pageA2 = Page("A2", 1) 
        self.pageB2 = Page("B2", 1) 
        self.pageC2 = Page("C2", 1)
        self.pageA2.setEingehendeLinks(self.pageB2)
        self.pageB2.setEingehendeLinks(self.pageC2)
        self.pageC2.setEingehendeLinks(self.pageA2)

        self.internet2 = Internet(self.DELTA, [self.pageA2, self.pageB2, self.pageC2])
        
        #Version 3
        self.pageA3 = Page("A3", 2) 
        self.pageB3 = Page("B3", 2) 
        self.pageC3 = Page("C3", 0)
        self.pageA3.setEingehendeLinks(self.pageB3)
        self.pageB3.setEingehendeLinks(self.pageA3)
        self.pageC3.setEingehendeLinks(self.pageA3, self.pageB3)

        self.internet3 = Internet(self.DELTA, [self.pageA3, self.pageB3, self.pageC3])

        #Version 4
        self.pageA4 = Page("A4", 1) 
        self.pageB4 = Page("B4", 1) 
        self.pageC4 = Page("C4", 0)
        self.pageB4.setEingehendeLinks(self.pageA4)
        self.pageC4.setEingehendeLinks(self.pageB4)

        self.internet4 = Internet(self.DELTA, [self.pageA4, self.pageB4, self.pageC4])

    def test_calculatePageRank(self):
        self.internet1.calculatePageRank()
        self.internet2.calculatePageRank()
        self.internet3.calculatePageRank()
        self.internet4.calculatePageRank()

        assert self.pageA1.pageRank == 1
        assert self.pageB1.pageRank == 1

        assert self.pageA2.pageRank == 1
        assert self.pageB2.pageRank == 1
        assert self.pageC2.pageRank == 1

        assert round(self.pageA3.pageRank, 3) == 0.261
        assert round(self.pageB3.pageRank, 3) == 0.261
        assert round(self.pageC3.pageRank, 3) == 0.372

        assert round(self.pageA4.pageRank, 3) == 0.15
        assert round(self.pageB4.pageRank, 3) == 0.278
        assert round(self.pageC4.pageRank, 3) == 0.386


