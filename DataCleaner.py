import pandas as pd

class DataCleaner():

    def __init__(self, path):
        self.path = path
        self.data = None

    def clean(self):
        self.remove_null()
        self.convert_types()
    
    def import_data(self):
        self.data = pd.read_csv(self.path)

    def remove_null(self):
        self.data.dropna(inplace=True)
        
    def convert_types(self):
        self.data['priority'] = self.data['priority'].astype(int)
        self.data['date'] = pd.to_datetime(self.data['date'])

    def __str__(self):
        string = '*' * 15 + 'INFO' + '*' * 15 + '\n'
        string += str(self.data.info())
        string = '*' * 15 + 'DESCRIBE' + '*' * 15 + '\n'
        string += str(self.data.describe())

        return string