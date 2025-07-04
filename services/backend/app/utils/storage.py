"""
Local-disk helpers
------------------
• upload_file(local_path, blob_name)  -> absolute path
• upload_bytes(data, blob_name, mime) -> absolute path
"""

from __future__ import annotations
import mimetypes, os, shutil
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

load_dotenv()  # reads .env at repo root (or nearest parent)

# ---------------------------------------------------------------------------
# 1️⃣  Destination root, e.g.  C:\speech-idol\files
# ---------------------------------------------------------------------------
SAVE_ROOT: Final = Path(os.getenv("SAVE_ROOT", r"C:\speech-idol\files")).resolve()
SAVE_ROOT.mkdir(parents=True, exist_ok=True)  # ensure folder exists

# ---------------------------------------------------------------------------
# 2️⃣  Helper: build full path & create sub-dirs on demand
# ---------------------------------------------------------------------------
def _fullpath(blob_name: str) -> Path:
    full = SAVE_ROOT / blob_name
    full.parent.mkdir(parents=True, exist_ok=True)
    return full

# ---------------------------------------------------------------------------
# 3️⃣  Public API – same signature the rest of the code already uses
# ---------------------------------------------------------------------------
def upload_file(local_path: str, blob_name: str) -> str:
    """
    Copy a file from elsewhere on disk into the SAVE_ROOT tree.

    Returns the absolute path to the stored copy.
    """
    dest = _fullpath(blob_name)
    shutil.copy2(local_path, dest)
    dest.touch()  # updates mtime so tests see a new file
    return str(dest)  # caller expects a string

def upload_bytes(data: bytes, blob_name: str, content_type: str) -> str:
    """
    Write raw bytes to disk.

    `content_type` is kept for signature compatibility but not used here.
    """
    dest = _fullpath(blob_name)
    dest.write_bytes(data)
    return str(dest)





# """
# Drive helpers
# -------------
# • upload_file(local_path, blob_name)  -> share-URL
# • upload_bytes(data, blob_name, mime) -> share-URL
# """

# from __future__ import annotations
# import io, json, mimetypes, pathlib
# from typing import Final
# import os

# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload
# from dotenv import load_dotenv

# load_dotenv()

# # ---------------------------------------------------------------------------
# # 1️⃣  Auth – load the OAuth token.json you created via drive_oauth_flow.py
# # ---------------------------------------------------------------------------
# TOKEN_FILE: Final = pathlib.Path(__file__).resolve().parents[3]  / "backend" / "token.json"

# creds = Credentials.from_authorized_user_file(
#     TOKEN_FILE, scopes=["https://www.googleapis.com/auth/drive.file"]
# )
# drive = build("drive", "v3", credentials=creds, cache_discovery=False)

# # ---------------------------------------------------------------------------
# # 2️⃣  Target folder in Drive (create it once, copy its ID here)
# # ---------------------------------------------------------------------------

# FOLDER_ID: Final = os.getenv("GDRIVE_FOLDER_ID")  # e.g. "1abCDeFG_hiJkLmNoPQRstuVWxyz"

# # ---------------------------------------------------------------------------
# # 3️⃣  Helpers
# # ---------------------------------------------------------------------------
# def _upload(media_body: MediaIoBaseUpload, name: str, mime: str) -> str:
#     file_meta = {"name": name, "parents": [FOLDER_ID]}
#     file = (
#         drive.files()
#         .create(body=file_meta, media_body=media_body, fields="id,webViewLink,webContentLink")
#         .execute()
#     )
#     return file["webContentLink"] or file["webViewLink"]  # fallback to preview link


# def upload_file(local_path: str, blob_name: str) -> str:
#     mime = mimetypes.guess_type(local_path)[0] or "application/octet-stream"
#     with open(local_path, "rb") as fh:
#         media = MediaIoBaseUpload(fh, mimetype=mime, resumable=False)
#         return _upload(media, blob_name, mime)


# def upload_bytes(data: bytes, blob_name: str, content_type: str) -> str:
#     media = MediaIoBaseUpload(io.BytesIO(data), mimetype=content_type, resumable=False)
#     return _upload(media, blob_name, content_type)
