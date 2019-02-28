#!/usr/bin/python3

import threading
from SQL.Statistics import Statistics;

class DeviceBase(object):
    
    def __init__(self, id, enable_statistics=False):
        self.mutex = threading.Lock()
        if(enable_statistics is True):
            self.statistics = Statistics();
            
        else:
            self.statistics = None;
        self.id = id;

    def UpdateTable(self, action):
        if(self.statistics is not None):
            self.statistics.insert(self.id, action, self.terminalList[action].Value);
    
    def connect(self):
        pass;

    def close_connection(self):
        pass;