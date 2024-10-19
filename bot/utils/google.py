import requests

class SheetsAPI:
    def __init__(self, sheet_id: str, sheet_name: str, cell_range: str, key: str, version: str = "v4") -> None:
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.cell_range = cell_range
        self.key = key
        self.version = version
    
    def get_data(self) -> dict:
        url = f"https://sheets.googleapis.com/{self.version}/spreadsheets/{self.sheet_id}/values/{self.sheet_name}!{self.cell_range}"
        params = {
            "alt": "json",
            "key": self.key
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
