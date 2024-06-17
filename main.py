from TxtToCsv import TxtToCsv
from DataCleaner import DataCleaner

def main():

    # converter = TxtToCsv('./logs_txt/')
    # converter.process()
    # converter.export('final.csv')
    # converter.close()

    cleaner = DataCleaner('final.csv')
    cleaner.import_data()
    cleaner.clean()
    print(cleaner)

if __name__ == '__main__':
    main()