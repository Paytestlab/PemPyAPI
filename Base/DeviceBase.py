#!/usr/bin/python3

import threading
from SQL.Statistics import Statistics;

class DeviceBase(object):
    
    def __init__(self, enable_statistics=False):
        self.mutex = threading.Lock()
        if(enable_statistics is True):
            self.statistics = Statistics();
            
        else:
            self.statistics = None;

    def UpdateTable(self, id, action):
        if(self.statistics is not None):
            self.statistics.insert(id, action, self.terminalList[action].Value);
    
    def connect(self):
        pass;

    def close_connection(self):
        pass;