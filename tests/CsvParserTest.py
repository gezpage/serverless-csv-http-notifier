import unittest

from CsvParser import CsvParser

csv_string = '''"First name", "Last name", "Email"
"Michal", "Przytulski", "mprzytulski@morneaushepell.com"
"Gez", "Page", "gezpage@gmail.com"
'''

expected_output = [
    '{"First name": "Michal", "Last name": "Przytulski", "Email": "mprzytulski@morneaushepell.com"}',
    '{"First name": "Gez", "Last name": "Page", "Email": "gezpage@gmail.com"}'
]


class TestCsvToJson(unittest.TestCase):
    def setUp(self):
        self.parser = CsvParser()

    def test_csv_string(self):
        self.assertEqual(expected_output, self.parser.string_to_json_list(csv_string))

    # def test_csv_file(self):
    #     TODO Remove this test as it reads from disk - should be an integration test
        # self.assertEqual(expected_output, self.parser.file_to_json_list("testdata.csv"))
