import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime

class GoogleSheetsClient:
    def __init__(self):
        load_dotenv()
        
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"), 
            scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
        self.worksheet = sheet.worksheet("Notes de frais")
    
    def append_expense(self, data: dict, image_url: str = None):
        row = [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            data.get("type_document"),
            data.get("fournisseur"),
            data.get("date"),
            data.get("montant_ttc"),
            data.get("tva"),
            data.get("devise"),
            data.get("description"),
            data.get("confiance"),
            image_url or ""
        ]
        self.worksheet.append_row(row)


if __name__ == "__main__":
    client = GoogleSheetsClient()
    client.append_expense({
        "type_document": "restaurant",
        "fournisseur": "Test",
        "date": "10/06/2026",
        "montant_ttc": 12.50,
        "tva": 1.25,
        "devise": "EUR",
        "description": "test",
        "confiance": "haute"
    })
    print("Ligne ajoutée !")