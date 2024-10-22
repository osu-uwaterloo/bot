import requests

from google.oauth2 import service_account as sva
from googleapiclient.discovery import build

class SheetsAPI:
    def __init__(self, sheet_id: str, sheet_name: str, cell_range: str, key: str = None,
                 service_acc_file: str = None,
                 scopes: "list[str]" = ["https://www.googleapis.com/auth/spreadsheets.readonly"], version: str = "v4") -> None:
        
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.cell_range = cell_range
        self.version = version

        if key is None and service_acc_file is None:
            raise ValueError("At least one of key, service_acc_file must be supplied.")
        
        if service_acc_file is not None and scopes is None:
            raise ValueError("Scopes cannot be None when using a service account.")
        
        self.key = key
        self.service_acc_file = service_acc_file
        self.scopes = scopes

    def get_creds_service_acc(self):
        return sva.Credentials.from_service_account_file(self.service_acc_file, scopes=self.scopes)


    def get_data(self) -> dict:
        if self.service_acc_file is not None:
            return self._get_data_service_acc()
        return self._get_data()
    
    def _get_data(self) -> dict:
        url = f"https://sheets.googleapis.com/{self.version}/spreadsheets/{self.sheet_id}/values/{self.sheet_name}!{self.cell_range}"
        params = {
            "alt": "json",
            "key": self.key
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    
    def _get_data_service_acc(self):
        creds = self.get_creds_service_acc()
        service = build("sheets", self.version, credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.sheet_id, range=f"{self.sheet_name}!{self.cell_range}")
            .execute()
        )

        return result


