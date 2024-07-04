import pandas as pd
import os

class FileReader():
    def __init__(self, directory) -> None:
        self.directory = directory
        self.n_files = os.listdir(directory)
        self.data = None

    def read_files_chunks(self):
        for filename in os.listdir(self.directory):
            with open(os.path.join(self.directory, filename), 'r') as file:
                while True:
                    chunk = file.read(1024 * 1024)  # Read 1MB at a time
                    if not chunk:
                        break
                    lines = chunk.split('\n')
                    yield from lines