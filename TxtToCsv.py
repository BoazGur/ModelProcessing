import pandas as pd
import os

class TxtToCsv():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = None

    def process(self):
        for idx, file in enumerate(os.listdir(self.folder_path)):
            if idx == 0:
                self.data = pd.read_csv(self.folder_path + file, sep='\t')
            else:
                df = pd.read_csv(self.folder_path + file, sep='\t')
                self.data = pd.concat([self.data, df])

    def export(self, path):
        self.data.to_csv(path)

    def close(self):
        self.data = None