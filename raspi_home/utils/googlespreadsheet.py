#!/usr/bin/env python
import os
import pprint

import pygsheets

CLIENT_SECRET_FILE = os.path.expanduser('~/.raspi-home-secrets/google_spreadsheet.json')


class Spreadsheet(object):
    'Utility class to use google spread sheet.'

    TOP_ROW = 0

    def __init__(self, doc_id, worksheet_index=0):
        self.check_credential_json()
        self.doc_id = doc_id
        self.worksheet_index = worksheet_index
        self.auth()

    def auth(self):
        self.gc = pygsheets.authorize(service_file=CLIENT_SECRET_FILE)
        self.spreadsheet = self.gc.open_by_key(self.doc_id)
        # check worksheet_index
        self.worksheet = self.spreadsheet.worksheet('index', self.worksheet_index)

    def check_credential_json(self, path=CLIENT_SECRET_FILE):
        if not os.path.exists(path):
            raise Exception('{} does not exists'.format(path))

    def get_sheet_count(self):
        return len(self.spreadsheet.worksheets())

    def get_column_count(self):
        return self.worksheet.cols

    def get_row_count(self):
        return self.worksheet.rows

    def insert_row(self, row, index=0):
        self.worksheet.insert_rows(row=index, number=1, values=row)

    def get_row(self, index=1, return_as_cell=False):
        return self.worksheet.get_row(index)


if __name__ == '__main__':
    # Test Spreadsheet API
    doc_id = os.environ['GOOGLE_SPREADSHEET_FOR_SPOTIFY']
    sheet = Spreadsheet(doc_id, 0)
    print('Testing {}'.format(doc_id))
    print('{} sheets'.format(sheet.get_sheet_count()))
    print('{}x{} size'.format(sheet.get_column_count(), sheet.get_row_count()))
    pp = pprint.PrettyPrinter(indent=4)
    first_row = sheet.get_row()
    print('first row: {}'.format(first_row))
    print('inserting a row at the top')
    first_element = int(first_row[0])
    sheet.insert_row([first_element + 1, first_element + 2,
                      first_element + 3, first_element + 4])
