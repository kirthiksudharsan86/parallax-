import gspread
from google.oauth2.service_account import Credentials
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES,
)
client = gspread.authorize(creds)
sheet = client.open("Parallax Teams").sheet1
def get_role(email):
    records = sheet.get_all_records()
    for row in records:
        if row["Registration Email"].strip().lower() == email:
            return "team"
        if row["OC Email"].strip().lower() == email:
            return "oc"
    return None