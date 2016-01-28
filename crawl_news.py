import feedparser
import os
from time import time
from vip_info import VipInfo
from reporter import Reporter
from config import CONF
from time import mktime
from datetime import datetime

class Crawler():
    def __init__(self):
        self.vip_info = VipInfo()
        self.rss_links = self._load_rss_links()
        self.reporter = Reporter()
        
    def _load_rss_links(self):
        links = []
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rss")
        for root, dirs, fs in os.walk(directory):
            for f in fs:
                links.append(os.path.join(root, f))
        return links
    
    def is_article_scanned(self, article):
        #assuming that all aticle updated dae time is in GMT...this comparison can be made
        epoch_article_time = mktime(article.updated_parsed)
        if epoch_article_time >= CONF.last_script_run_date_time and epoch_article_time >= CONF.REPORT_START_DATE_TIME:
            return False
        return True
    
    def crawl(self):
        new_article_scanned = 0
        old_article_scanned = 0
        vip_article_found = 0
        
        #not the start time for crawling for this sceduled run
        crawl_start_time = time()
        
        for f in list(self.rss_links):
            text = open(f, "rb").read()
            urls = text.split(os.linesep)
            
            for url in urls:
                feed = feedparser.parse(url)
                
                for article in feed.entries:
                    # print "Working on", article.link
                    if not self.is_article_scanned(article):
                        new_article_scanned += 1
                        if self.vip_info.is_there_vip_news(article):
                            vip_article_found += 1
                            self.reporter.update(article)
                    else:
                        old_article_scanned += 1
        
        #update the crawl start time in config
        CONF.last_script_run_date_time = crawl_start_time
        
        #log
        print "new articles scanned:", new_article_scanned
        print "old articles skipped:", old_article_scanned
        print "vip articles found:", vip_article_found