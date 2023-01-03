from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery


class GoogleSheet:
    SPREADSHEET_ID = '1mu-ONFyjL0Sam3TRLuVPwxr7qC90k9Pspmp34P60AV8'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None
    new_id = '1jkuLyTbRLN98RFLo35qbGH0FwAFcR_qhESe9DPO05wk'

    def __init__(self, SPREADSHEET_ID=None, new_id=None):
        creds = None
        if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.SPREADSHEET_ID = SPREADSHEET_ID
        self.credentials = creds
        self.service = build('sheets', 'v4', credentials=creds)

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().clear(spreadsheetId=self.SPREADSHEET_ID,
                                                                  body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def append_data(self, range: str = None, value_range_body: list = None):

        credentials = self.credentials
        service = discovery.build('sheets', 'v4', credentials=credentials)

        # The ID of the spreadsheet to update.
        spreadsheet_id = self.SPREADSHEET_ID  # TODO: Update placeholder value.

        # The A1 notation of a range to search for a logical table of data.
        # Values will be appended after the last row of the table.
        range_ = range # TODO: Update placeholder value.

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

        # How the input data should be inserted.
        insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

        value_range_body = value_range_body

        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range,
                                                         valueInputOption=value_input_option,
                                                         insertDataOption=insert_data_option, body={'values': value_range_body})
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        pprint(response)

    def delete_rows(self, startIndex: int = 1, endIndex: int = 2, sheetId: int = 145524572):
        credentials = self.credentials
        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = self.SPREADSHEET_ID
        spreadsheet_data = [{"deleteDimension": {
            "range": {"sheetId": sheetId, "dimension": "ROWS", "startIndex": startIndex, "endIndex": endIndex}}}]
        update_data = {"requests": spreadsheet_data}
        request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=update_data)
        request = request.execute()
        pprint(request)

    def get_first_date_from_my_googolist(self):
        credentials = self.credentials
        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = self.SPREADSHEET_ID
        sh = service.spreadsheets()
        responce = sh.values().get(spreadsheetId=spreadsheet_id, range='Все цены!F2:E100000').execute()
        result = sorted(set(map(lambda x: x[0], responce['values'])))[1]
        endIndex = responce['values'].index([result]) + 1
        return endIndex

    def get_links(self):
        credentials = self.credentials
        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = self.new_id
        sh = service.spreadsheets()
        responce = sh.values().get(spreadsheetId=spreadsheet_id, range='Data!A2:A100').execute()
        print(responce)
        result = sorted(set(map(lambda x: x[0], responce['values'])))
        return result[0]


def main():

    gs = GoogleSheet()
    endIndex = gs.get_links()


if __name__ == '__main__':
    main()