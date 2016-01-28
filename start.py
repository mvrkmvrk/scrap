import time
from config import CONF
from datetime import timedelta
from crawl_scheduler import start_crawler
from report_scheduler import start_report_scheduler

while(True):
    #load fresh updated config
    print "CONFIG:"
    print CONF.config
    
    start_crawler()
    start_report_scheduler()
    
    print "sleep for some time"
    time.sleep(30)
    