from __future__ import print_function
import json
import os.path
import pickle
from googleapiclient.http import MediaIoBaseUpload
import google
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery
from google.oauth2.credentials import Credentials
import io
from googleapiclient.errors import HttpError
import requests


class GoogleSheet:
    SPREADSHEET_ID = '1mu-ONFyjL0Sam3TRLuVPwxr7qC90k9Pspmp34P60AV8'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
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

    def delete_all(self):

        # Авторизация
        credentials = self.credentials
        service = build('sheets', 'v4', credentials=credentials)

        # Идентификатор таблицы и листа
        spreadsheet_id = '1haeDysc7udUwXAlUGwG0BWxt0lAdYZn57lIPp5jdkuU'
        sheet_id = 0  # номер листа (начинается с 0)
        sheet_name = 'парсер OZON WB'  # название листа

        # Очистка данных

        if sheet_name:
            sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute().get('sheets', '')
            for sheet in sheet_metadata:
                print(sheet['properties']['title'])
                if sheet['properties']['title'] == sheet_name:
                    sheet_id = sheet['properties']['sheetId']
                    print(sheet_id)
                    break
        body = {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 2000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 5
                        },
                        "fields": "userEnteredValue"
                    }
                }
            ]
        }
        request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    # Функция для загрузки файла по ссылке с Google Диска
    def download_google_file(self, link, file_name):

        try:
            # Извлекаем ID файла из ссылки
            file_id = link.split('/')[-2]
            # Создаем клиента Google Drive API
            credentials = Credentials.from_authorized_user_file("/Users/vladimirivliev/PycharmProjects/pythonProject1/credentials/credentials.json",
                                                  ["https://www.googleapis.com/auth/drive"])
            service = build('drive', 'v3', credentials=credentials)

            # Запрашиваем информацию о файле
            file = service.files().get(fileId=file_id).execute()
            print('here1')

            # Загружаем содержимое файла
            download_url = file.get('exportLinks').get('application/pdf')
            print('here')
            if download_url:
                response = requests.get(download_url)
                # Сохраняем содержимое файла в файл на диск
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print(f'Файл {file_name} успешно загружен.')
            else:
                print('Ссылка не содержит доступного формата для экспорта файла.')
        except HttpError as error:
            print(f'Произошла ошибка: {error}')
        except Exception as error:
            print(f'Произошла ошибка: {error}')

        # Устанавливаем учетные данные для доступа к API Google
        creds = None
        creds_file_path = '/Users/vladimirivliev/PycharmProjects/pythonProject1/credentials/credentials.json'
        if creds_file_path:
            with open(creds_file_path, 'r') as f:
                creds = google.oauth2.credentials.Credentials.from_authorized_user_info(json.load(f))

    def save_scrinchot(self, image_bytes, file_name):
        DRIVE_FOLDER_ID = '1H7tc9yEu1S1Ix7IkdaPLZUiCPNJl1Ry1'
        file_metadata = {'name': file_name, 'parents': [DRIVE_FOLDER_ID]}
        service = build('drive', 'v3', credentials=self.credentials)
        with io.BytesIO(image_bytes) as image_buffer:
            media = MediaIoBaseUpload(image_buffer, mimetype='image/png')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'File ID: {file.get("id")}')
        # Создаем медиа-файл для загрузки:

        # media = MediaIoBaseUpload(file, mimetype='png/plain')
        #
        # # Загружаем файл на Google Диск:
        # file = drive_service.files().create(body=file_metadata, media_body=media,
        #                                     fields='id').execute()

        print('File ID: %s' % file.get('id'))


def main():
    gs = GoogleSheet()
    gs.save_scrinchot()


if __name__ == '__main__':
    main()