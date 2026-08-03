import os
import json
import gspread
from google.oauth2.service_account import Credentials
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
if os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"):
    service_account_info = json.loads(
        os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    )
    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES,
    )
else:
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES,
    )
client = gspread.authorize(creds)
def get_sheet():
    return client.open("Parallax Teams").sheet1
def get_participant(email):
    email = email.strip().lower()
    sheet = get_sheet()
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
    return get_sheet().get_all_records()
def update_team_selection(email, track_name=None, ps_code=None):
    email = (email or "").strip().lower()
    if not email:
        return False
    try:
        sheet = get_sheet()
        headers = sheet.row_values(1)
        records = sheet.get_all_records()
        row_index = None
        for i, row in enumerate(records, start=2):  # row 1 is the header
            reg_email = str(row.get("Registration Email", "")).strip().lower()
            if reg_email == email:
                row_index = i
                break
        if row_index is None:
            return False
        if track_name is not None and "Track" in headers:
            sheet.update_cell(row_index, headers.index("Track") + 1, track_name)
        if ps_code is not None and "PS" in headers:
            sheet.update_cell(row_index, headers.index("PS") + 1, ps_code)
        return True
    except Exception:
        return False
def update_team_name(email, team_name):
    email = (email or "").strip().lower()
    team_name = (team_name or "").strip()

    if not email or not team_name:
        return False

    try:
        sheet = get_sheet()
        headers = sheet.row_values(1)
        records = sheet.get_all_records()

        row_index = None

        for i, row in enumerate(records, start=2):
            reg_email = str(
                row.get("Registration Email", "")
            ).strip().lower()

            if reg_email == email:
                row_index = i
                break

        if row_index is None:
            return False

        if "Team Name" in headers:
            sheet.update_cell(
                row_index,
                headers.index("Team Name") + 1,
                team_name,
            )

        return True

    except Exception:
        return False    
def update_offline_registration(team_id, offline_registered):
    team_id = str(team_id).strip()

    if not team_id:
        return False

    try:
        sheet = get_sheet()
        headers = sheet.row_values(1)
        values = sheet.get_all_values()

        if "Team ID" not in headers:
            return False

        if "Offline Registration" not in headers:
            return False

        team_col = headers.index("Team ID")
        offline_col = headers.index("Offline Registration")

        for row_number in range(2, len(values) + 1):
            current_team_id = values[row_number - 1][team_col].strip()

            if current_team_id == team_id:
                sheet.update_cell(
                    row_number,
                    offline_col + 1,
                    "1" if offline_registered else "0",
                )
                return True

        return False

    except Exception:
        return False