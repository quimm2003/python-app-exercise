from sys import stderr
from io import StringIO
import csv
import pandas as pd
import requests
from datetime import date
from pathlib import Path

class ApiService:
    def __init__(self):
        """Initialize variables."""
        self._todos_url = 'https://jsonplaceholder.typicode.com/todos/'
        self._todos_json = None
        self._storage_path = None
        self._today = date.today().strftime('%Y_%m_%d')

    def __get_storage_path(self):
        """Get the storage folder absolute path."""
        script_path = None
        
        # In some python versions the __file__ object is not available. Test it
        if __file__:
            script_path = __file__
        else:
            # If __file__ is not available, get this script path using inspect
            from inspect import currentframe, getframeinfo
            script_path = getframeinfo(currentframe()).filename

        if script_path:
            self._storage_path = Path(script_path).resolve().parent.parent.parent.joinpath('storage')
        else:
            raise Exception("Can not retrieve the torage folder path")

    def __download_todos(self):
        """Use requests libraty to download todos in json format."""
        # Execute a get request
        todos = requests.get(self._todos_url)
        # Save the response in json format
        self._todos_json = todos.json()

    def __convert_todos_to_csv_files(self):
        """Convert the todos json items into csv format and store as csv files."""
        if self._todos_json:
            # Use pandas to create the DataFrame from todos in json format
            df = pd.json_normalize(self._todos_json)

            # Iterate the DataFrame by index
            for df_ix in range(len(df)):
                # Get the value of the id column
                ind = df.iloc[df_ix]['id']
                # Build the csv file path
                output_csv_file = "{0}/{1}_{2}.csv".format(self._storage_path, self._today, ind)
                # Save the DataFrame row into the csv file without header and index
                df.loc[[df_ix]].to_csv(output_csv_file, index=False, header=False, mode='a')

    def run(self):
        print('Running ApiService', file=stderr)

        try:
            self.__get_storage_path()
            self.__download_todos()
            self.__convert_todos_to_csv_files()
            print('ApiService finished its job')
        except Exception as exc:
            print(str(exc), file=stderr)
