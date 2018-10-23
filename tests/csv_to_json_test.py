import unittest
from csv_to_json import *

input = '''"First name", "Last name", "Email"
"Michal", "Przytulski", "mprzytulski@morneaushepell.com"
"Gez", "Page", "gezpage@gmail.com"
'''

output = '''[{"Last name": "Przytulski", "First name": "Michal", "Email": "mprzytulski@morneaushepell.com"}, {"Last name": "Page", "First name": "Gez", "Email": "gezpage@gmail.com"}]'''

class TestCsvToJson(unittest.TestCase):
    # def test_file_contents_matches_string(self):
    #     self.assertEqual(open("testdata.csv").read(), input)

    def test_csv_string_to_json_list(self):
        self.assertEqual(csv_string_to_json_list(open("testdata.csv").read()), output)

    def test_csv_file_to_json_list(self):
        self.assertEqual(output, csv_file_to_json_list("testdata.csv"))
