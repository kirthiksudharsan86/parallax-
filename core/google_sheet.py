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


def get_participant(email):
    email = email.strip().lower()

    records = sheet.get_all_records()

    for row in records:
        reg_email = str(row.get("Registration Email", "")).strip().lower()
        oc_email = str(row.get("OC Email", "")).strip().lower()

        if reg_email == email:
            row["role"] = "team"
            return row

        if oc_email == email:
            row["role"] = "oc"
            return row

    return None


def get_role(email):
    participant = get_participant(email)

    if participant:
        return participant["role"]

    return None
def get_all_teams():
    return sheet.get_all_records()