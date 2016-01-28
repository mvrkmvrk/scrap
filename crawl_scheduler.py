from crawl_news import Crawler
from config import CONF
from time import time

cr = Crawler()

def start_crawler():
    #get gresh updated config
    current_time = time()
    if current_time > CONF.last_script_run_date_time + CONF.script_run_interval:
        cr.crawl()