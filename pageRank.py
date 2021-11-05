import sqlite3

class Page:
    def __init__(self, name:str, intAusgehendeLinks:int, pageRank:float = 1, prIteration = 1):
        self.name = name
        self.ausgehendeLinks = intAusgehendeLinks
        self.oldRank = pageRank
        self.pageRank = pageRank
        self.prIteration = prIteration
        self.eingehendeLinks = []

    def setEingehendeLinks(self, *eingehendeLinks):
        for link in eingehendeLinks:
            self.eingehendeLinks.append(link)

    def setPageRank(self, newPageRank):
        self.pageRank = newPageRank
    
    def showPageRank(self):
        print(f"Pagerank von Seite {self.name} ist {self.pageRank}")
    


class Internet:
    def __init__(self, delta:float, allPages:list[Page]):
        self.allPages = allPages
        self.delta = delta
        self.iterationCnt = 0 

    def calculatePageRank(self, dampen:float = 0.85):
        notEnoughDiff = False
        while not notEnoughDiff: 
        #for i in range(3):
            notEnoughDiff = True                                                #Weiterrechnen solange Delta nicht niedrig genug
            self.iterationCnt += 1
            for page in self.allPages:                                          #Alle Seiten des Internets durchlaufen
                page.oldRank = page.pageRank   
                tempRank = (1-dampen)
                for eingehenderLink in page.eingehendeLinks:                    #Alle eingehenden Seiten der ausgewählten Seite durchlaufen
                    try:
                        tempRank += dampen * (eingehenderLink.oldRank / eingehenderLink.ausgehendeLinks)
                    except ZeroDivisionError:
                        tempRank += 0
                page.pageRank = tempRank
                
                page.showPageRank()
                #Check all pages
                notEnoughDiff = notEnoughDiff and self.__enoughDiff(page)
                
            print("---")

        self.showFullPageRank()    
        self.__showIteration()

    def showFullPageRank(self):
        fullRank = 0
        for page in self.allPages:
            fullRank += page.pageRank
        
        self.allPages.sort(key=lambda page: page.pageRank, reverse=True)

        for page in self.allPages:
            print(f"{page.name}: {round(page.pageRank, 3)}")
        print(f"Gesamt: {fullRank}") 

    def __showIteration(self):
        print(f"Iteration: {self.iterationCnt}")

    def __enoughDiff(self, page:Page):
        boolResult = abs(page.pageRank - page.oldRank) < self.delta

        return boolResult

if __name__ == '__main__':
    delta = 0.00000000000000000000000000000000000000000000005

    def getPageData():
        sqlPages = {}
        conn = sqlite3.connect("C:\Schule\School\Berufsschule\AJ3\my_wiki.sqlite")
        c = conn.cursor()
        c.execute("""SELECT p.page_title, COUNT(*) AS outLinks
                        FROM page p
                        INNER JOIN pagelinks pl 
                            ON pl.pl_from = p.page_id 
                        GROUP BY p.page_title;""")

        for page_title, outLinks in c:
            sqlPages.update({page_title : Page(page_title, outLinks)})
        
        sqlPages.update({"null" : Page("null", 0)})
        
        conn.commit()
        conn.close()
        return sqlPages
        
    def setLinks(sqlPages):
        conn = sqlite3.connect("C:\Schule\School\Berufsschule\AJ3\my_wiki.sqlite")

        for key in sqlPages:
            c = conn.cursor()
            c.execute("""SELECT p.page_title AS link_from, p2.pl_title AS link_for
                        FROM page p 
                        LEFT JOIN pagelinks p2 
                            ON p.page_id = p2.pl_from
                        LEFT JOIN page p3 
                            ON p2.pl_title = p3.page_title
                        WHERE link_for = ?
                        ORDER BY link_for;""", [key])

            for link_for, link_from in c:
                if link_for == None:
                    link_for = "null"
                
                if link_from == None:
                    link_from = "null"
                
                sqlPages[key].setEingehendeLinks(sqlPages[link_for])
            
    '''
    SELECT p.page_id AS source_id, p.page_title AS source_titel, p3.page_id AS ziel_id, p2.pl_title AS ziel_titel 
      FROM page p 
      LEFT JOIN pagelinks p2 
        ON p.page_id = p2.pl_from
      LEFT JOIN page p3 
        ON p2.pl_title = p3.page_title 
      ORDER BY p.page_id;
    '''

    #Version 1
    '''pageA1 = Page("A1", 1)
    pageB1 = Page("B1", 1)
    pageA1.setEingehendeLinks(pageB1)
    pageB1.setEingehendeLinks(pageA1)

    internet1 = Internet(delta, pageA1, pageB1)
    internet1.calculatePageRank()

    #Version 2
    pageA2 = Page("A2", 1) 
    pageB2 = Page("B2", 1) 
    pageC2 = Page("C2", 1)
    pageA2.setEingehendeLinks(pageB2)
    pageB2.setEingehendeLinks(pageC2)
    pageC2.setEingehendeLinks(pageA2)

    internet2 = Internet(delta, pageA2, pageB2, pageC2)
    internet2.calculatePageRank()

    #Version 3
    pageA3 = Page("A3", 2) 
    pageB3 = Page("B3", 2) 
    pageC3 = Page("C3", 0)
    pageA3.setEingehendeLinks(pageB3)
    pageB3.setEingehendeLinks(pageA3)
    pageC3.setEingehendeLinks(pageA3, pageB3)

    internet3 = Internet(delta, pageA3, pageB3, pageC3)
    internet3.calculatePageRank()

    #Version 4
    pageA4 = Page("A4", 1) 
    pageB4 = Page("B4", 1) 
    pageC4 = Page("C4", 0)
    pageB4.setEingehendeLinks(pageA4)
    pageC4.setEingehendeLinks(pageB4)

    internet4 = Internet(delta, pageA4, pageB4, pageC4)
    internet4.calculatePageRank()'''

    #
    '''Objekt = Page(Name, intAusgehendeVerlinkungen)
    Objekt.setEingehendeLinks(Objekte)'''

    sqlPages = getPageData()
    pagesArr = []


    setLinks(sqlPages)

    for key in sqlPages:
        pagesArr.append(sqlPages[key])
        for key2 in sqlPages[key].eingehendeLinks:
            print(key2.name)
    
    internet = Internet(delta, pagesArr)
    internet.calculatePageRank() 