import pandas as pd
import os

class FileReader():
    def __init__(self, directory, portion=1):
        self.directory = directory
        self.n_files = os.listdir(directory)
        self.data = None
        self.portion = portion

    def read_files_chunks(self):
        for filename in os.listdir(self.directory):
            size = os.path.getsize(os.path.join(self.directory, filename)) * self.portion
            with open(os.path.join(self.directory, filename), 'r') as file:
                while True:
                    chunk = file.read(128 * 128)
                    if (not chunk) or size <= 0:
                        break

                    size -= len(chunk)
                    lines = chunk.split('\n')
                    yield from lines