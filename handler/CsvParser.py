import csv
import json
from typing import List


class CsvParser:
    """ Uses the built in csv library to parse data from files or strings

    Override default CSV reader defaults in constructor for different schema types
    """

    def __init__(self, delimiter=',', quotechar='"', skipinitialspace=True):
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.skipinitialspace = skipinitialspace

    def file_to_json_list(self, file: str) -> list:
        """ Read a csv file from its path and return a list of JSON strings """
        with open(file) as csv_data:
            return self.__dict_to_json_list(self.__make_dict_reader(csv_data))

    def string_to_json_list(self, string: str) -> list:
        """ Convert a CSV multiline string to a list of JSON strings"""
        iterator = iter(string.splitlines())
        dict_reader = self.__make_dict_reader(iterator)

        return self.__dict_to_json_list(dict_reader)

    @staticmethod
    def __dict_to_json_list(dict_reader: csv.DictReader) -> list:
        """ Convert a DictReader type to a list of JSON strings """
        json_list: List[str] = list()
        for row in dict_reader:
            json_list.append(json.dumps(row))

        return json_list

    def __make_dict_reader(self, f) -> csv.DictReader:
        """ Instantiates a csv DictReader with parameters set during construction """
        return csv.DictReader(
            f,
            delimiter=self.delimiter,
            quotechar=self.quotechar,
            skipinitialspace=self.skipinitialspace,
            strict=True
        )


if __name__ == '__main__':
    parser = CsvParser()
    csv_string = '''"First name", "Last name", "Email"
    "Dave", "Wells", "dwells@email.com"
    "Dan", "Hardway", "dahardway@email.com"'''
    print("CSV File:")
    print(parser.file_to_json_list("data/testdata.csv"))
    print("CSV String:")
    print(parser.string_to_json_list(csv_string))
