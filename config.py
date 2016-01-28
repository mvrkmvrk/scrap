import os
import json
from time import time
import os

import datetime
epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_seconds(dt):
    return (dt - epoch).total_seconds()

class Config(object):
    REPORT_START_DATE_TIME = unix_time_seconds(datetime.datetime(2016, 1, 25, 0, 0, 0))
    
    def __init__(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.config_file = os.path.join(directory, "config.data")
        
        #if there is no config or the file is empty then load a default config
        if not os.path.exists(self.config_file) or (os.path.exists(self.config_file) and not open(self.config_file, "rb").read().strip()):
            self._load_config()
            self._update()
        else:
            self.config = json.loads(open(self.config_file, "rb").read())
            
    def _load_config(self):
        self.config = {}
        self.last_report_date_time = -1
        self.last_script_run_date_time = -1
        self.report_interval = 7 * 24 * 60 * 60 # 7 days
        self.script_run_interval = 30 * 60 # 30 minutes
    
    def _get_last_report_date_time(self):
        return self.config["last_report_date_time"]   
    def _set_last_report_date_time(self, last_report_date_time):
        self.config["last_report_date_time"] = last_report_date_time
        self._update()
    last_report_date_time = property(_get_last_report_date_time, _set_last_report_date_time)
    
    def _get_last_script_run_date_time(self):
        return self.config["last_script_run_date_time"]   
    def _set_last_script_run_date_time(self, last_script_run_date_time):
        self.config["last_script_run_date_time"] = last_script_run_date_time
        self._update()
    last_script_run_date_time = property(_get_last_script_run_date_time, _set_last_script_run_date_time)
    
    def _get_report_interval(self):
        return self.config["report_interval"]   
    def _set_report_interval(self, report_interval):
        self.config["report_interval"] = report_interval
        self._update()
    report_interval = property(_get_report_interval, _set_report_interval)
    
    def _get_script_run_interval(self):
        return self.config["script_run_interval"]   
    def _set_script_run_interval(self, script_run_interval):
        self.config["script_run_interval"] = script_run_interval
        self._update()
    script_run_interval = property(_get_script_run_interval, _set_script_run_interval)

    def _update(self):
        json.dump(self.config, open(self.config_file, "wb"), sort_keys=True, indent=4, separators=(',', ': '))

CONF = Config()

def test_config():
    pass