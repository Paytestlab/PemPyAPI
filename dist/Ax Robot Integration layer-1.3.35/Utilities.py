import os
from os import listdir
from os.path import isfile, join

class Utilities(object):
    """Utilities for the robot"""
    @staticmethod
    def get_and_print_conf_list(path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        print("Enter terminal layout and press Enter:")
        i = 0;
        for files in onlyfiles:
            i += 1
            print(str(i) + ": " + files[:-4])

        return onlyfiles

    @staticmethod
    def select_conf(path, index):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
       
        return join(path, onlyfiles[index -1])




