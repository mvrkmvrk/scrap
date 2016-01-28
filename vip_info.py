import csv
import os

class VipInfo():
    def __init__(self):
        self.names_positions_organisations = self._get_name_position_organisation()
        self.full_names = set([r[0] for r in self.names_positions_organisations])
        self.positions = set([r[1] for r in self.names_positions_organisations])
        self.organisations = set([r[2] for r in self.names_positions_organisations])
        
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.keywords = open(os.path.join(directory, "keywords.txt"), "rb").read().split(os.linesep)
        self.keywords = set([kw.strip() for kw in self.keywords])
        
    def _get_name_position_organisation(self):
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        csv_file = os.path.join(csv_file, "Masterlist database_CSV.csv")
        
        with open(csv_file, 'rb') as csvfile:
            rows = csv.reader(csvfile, delimiter=',', quotechar='"')
            rows = [[r.lower().replace("\r", " ").replace("/", " ") for r in row] for row in rows]
        return rows[1:]
    
    def investigate(self, article):
        return True
    
    def is_there_vip_news(self, article):
        article_headline = article.title.encode("utf-8").lower().split()
        article_summary = article.summary.encode("utf-8").lower().split()
    
        investigate = False
        full_name = False
        position = False
        organisation = False
        keywords = False
        count = 0
        
        for n in self.full_names:
            if n in article_headline or n in article_summary:
                # print n, "--names"
                count += 1
                investigate = True
                full_name = True
                break
                
        for org in self.organisations:
            if org in article_headline or org in article_summary:
                # print org, "--orgs"
                count += 1
                investigate = True
                organisation = True
                break
        
        for pos in self.positions:
            if pos in article_headline or pos in article_summary:
                # print pos, "--pos"
                count += 1
                investigate = True
                position = True
                break
            
        for kw in self.keywords:
            if kw in article_headline or kw in article_summary:
                # print kw, "--keywords"
                count += 1
                investigate = True
                keywords = True
                break
                
        if investigate and count > 1 and (full_name or keywords):
            print "---MATCHED", count
            return self.investigate(article)
        return False
    
def test_3_columns_in_rows():
    rows = get_name_position_organisation()
    for r in rows:
        assert len(r) == 3
        
    assert len(rows) == 1481