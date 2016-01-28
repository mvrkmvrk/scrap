import csv
import os
import feedparser
from time import time
from vip_info import VipInfo
from config import Config
from time import mktime
from datetime import datetime

class Reporter(object):
    def __init__(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.report_file = os.path.join(directory, "reports.csv")
    
    def update(self, article):
        with open(self.report_file, 'ab') as csvfile:
            #what is quotechar and quoting?
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([article.updated, article.link])
            
def test_update():
    def load_rss_links():
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rss")
        for root, dirs, fs in os.walk(directory):
            for f in fs:
                yield os.path.join(root, f)
            
    rep = Reporter()
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    rep.report_file = os.path.join(directory, "test_reports.csv")
        
    rss_links = load_rss_links()
    
    for f in rss_links:
        text = open(f, "rb").read()
        urls = text.split(os.linesep)
        
        for url in urls:
            feed = feedparser.parse(url)
            
            for article in feed.entries:
                rep.update(article)