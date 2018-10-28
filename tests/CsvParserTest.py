import unittest

from handler.CsvParser import CsvParser

csv_string = '''"First name", "Last name", "Email"
"Dave", "Banks", "dbanks@email.com"
"George", "Digby", "gdigby@email.com"
'''

expected_output = [
    '{"First name": "Dave", "Last name": "Banks", "Email": "dbanks@email.com"}',
    '{"First name": "George", "Last name": "Digby", "Email": "gdigby@email.com"}'
]


class CsvParserTest(unittest.TestCase):
    """ Use simple input and output strings to check JSON is correct

    If other CSV schemas become supported, use a data provider with different CSV strings

    TODO Test file_to_json_list with mocked open() builtin
    """

    def setUp(self):
        self.parser = CsvParser()

    def test_csv_string(self):
        json_list = self.parser.string_to_json_list(csv_string)

        self.assertEqual(expected_output, json_list)
        self.assertEqual(2, len(json_list))
