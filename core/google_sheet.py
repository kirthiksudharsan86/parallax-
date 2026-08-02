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
    """Write the participant's selected Track and/or PS code back to their
    row in the Google Sheet, matched by Registration Email. Only touches
    the columns that are explicitly passed in (None = leave untouched).
    Returns True if a matching row was found and updated, False otherwise.
    Never raises — callers should treat a False/exception as non-fatal,
    since the DB (Team.track / Team.problem_statement) is the source of
    truth the dashboard actually reads from.
    """
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
def update_offline_registration(team_id, offline_registered):
    """Write the offline-registration checkbox back to the sheet, matched by
    Team ID (not Registration Email, since the OC toggle only has the team
    code to work with). Only touches the "Offline Registration" column if it
    exists on the sheet. Never raises, and never blocks the DB save that
    already happened; the DB (Team.offline_registered) remains the source of
    truth the dashboard actually reads from. Returns True if a matching row
    was found and updated, False otherwise.
    """
    team_id = (team_id or "").strip()
    if not team_id:
        return False
    try:
        sheet = get_sheet()
        headers = sheet.row_values(1)
        if "Offline Registration" not in headers:
            return False
        records = sheet.get_all_records()
        row_index = None
        for i, row in enumerate(records, start=2):  # row 1 is the header
            if str(row.get("Team ID", "")).strip() == team_id:
                row_index = i
                break
        if row_index is None:
            return False
        sheet.update_cell(
            row_index,
            headers.index("Offline Registration") + 1,
            "Yes" if offline_registered else "No",
        )
        return True
    except Exception:
        return False