from SQL.Statistics import Statistics

def main():
    statistics = Statistics()
    statistics.insert("ingenico", "PRESS 1", "G0 TEST")
    statistics.insert("ingenico", "PRESS 2", "G0 TEST")
    statistics.insert("ingenico", "PRESS 3", "G0 TEST")
    statistics.insert("ingenico", "PRESS 4", "G0 TEST")


main()


