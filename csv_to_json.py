import csv
import json


def csv_file_to_json_list(csv_file):
    with open(csv_file) as csv_data:
        csv_iterator = csv.DictReader(csv_data, delimiter=',', quotechar='"', skipinitialspace=True, strict=True)
        return json.dumps(list(csv_iterator))


def csv_string_to_json_list(csv_string):
    iterator = iter(csv_string.splitlines())
    csv_iterator = csv.DictReader(iterator, delimiter=',', quotechar='"', skipinitialspace=True, strict=True)
    return json.dumps(list(csv_iterator))


if __name__ == '__main__':
    input = '''"First name", "Last name", "Email"
"Michal", "Przytulski", "mprzytulski@morneaushepell.com"
"Gez", "Page", "gezpage@gmail.com"'''
    print "CSV File:"
    print csv_file_to_json_list("tests/testdata.csv")
    print "CSV String:"
    print csv_string_to_json_list(input)
