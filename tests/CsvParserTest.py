import unittest

from handler.CsvParser import CsvParser

csv_string = '''"First name", "Last name", "Email"
"Michal", "Przytulski", "mprzytulski@morneaushepell.com"
"Gez", "Page", "gezpage@gmail.com"
'''

expected_output = [
    '{"First name": "Michal", "Last name": "Przytulski", "Email": "mprzytulski@morneaushepell.com"}',
    '{"First name": "Gez", "Last name": "Page", "Email": "gezpage@gmail.com"}'
]


class CsvParserTest(unittest.TestCase):
    """ Use simple input and output strings to check JSON is correct

    If other CSV schemas become supported, use a data provider with different CSV strings
    """
    def setUp(self):
        self.parser = CsvParser()

    def test_csv_string(self):
        self.assertEqual(expected_output, self.parser.string_to_json_list(csv_string))
