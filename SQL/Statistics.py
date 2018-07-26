#!/usr/bin/python3

from SQL.SqlWorker import Sqlite3Worker
from threading import Lock
import time

class Statistics(object):
    """description of class"""
    def __init__(self):
        self.sqlWorker = Sqlite3Worker("statistics.db")
        self.mutex = Lock()

        query = (
            "CREATE TABLE if not exists statistics "
            "("
            "id INTEGER PRIMARY KEY,"
            "timestamp DATETIME,"
            "robot_id varchar(30),"
            "command_id varchar(20),"
            "command varchar(20)"
            ");"
            )
        self.sqlWorker.execute(query)

    def insert(self, robot_id, command_id, command):
        query =  (
            "INSERT INTO statistics "
            "("
            "timestamp, robot_id, command_id, command"
            ") "
            "VALUES "
            "( "
            "\"" + time.strftime('%Y-%m-%d %H:%M:%S') + "\", "
            "\"" + robot_id + "\", "
            "\"" + command_id + "\", "
            "\"" + command + "\""
            ")"
            )
        self.mutex.acquire()

        try:
            self.sqlWorker.execute(query)
        except:
            pass
        finally:
            self.mutex.release()
