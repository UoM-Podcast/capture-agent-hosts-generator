from __future__ import print_function

__author__ = 'andrew wilson'

"""# Copyright 2018 Google LLC
# Copyright 2018 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import conf

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

def getsheet():
    """Shows basic usage of the Sheets API.
    Gets values from a spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = conf.get_spreadsheet_id()
    RANGE_NAME = conf.get_worksheet_name()
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    spread_filt = []
    head_num = 0
    if not values:
        print('No data found.')
    else:
        for header in values[0]:
            print(head_num, header)
            head_num += 1

        for row in values:
            if len(row) >= 51:
                spread_filt.append(row[:51])
    return spread_filt
