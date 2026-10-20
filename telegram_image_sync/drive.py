"""Google Drive 업로드 헬퍼. OAuth refresh token 방식."""
import json
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload

FOLDER = "application/vnd.google-apps.folder"
STATE_NAME = "_sync_state.json"


def _q(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


class Drive:
    def __init__(self):
        creds = Credentials(
            None,
            refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
            token_uri="https://oauth2.googleapis.com/token",
            scopes=["https://www.googleapis.com/auth/drive"],
        )
        self.svc = build("drive", "v3", credentials=creds, cache_discovery=False)
        self._folders = {}

    def _find(self, name, parent, mime=None):
        q = f"name = '{_q(name)}' and '{parent}' in parents and trashed = false"
        if mime:
            q += f" and mimeType = '{mime}'"
        res = self.svc.files().list(q=q, fields="files(id)", pageSize=1).execute()
        files = res.get("files", [])
        return files[0]["id"] if files else None

    def folder(self, parent, name):
        key = (parent, name)
        if key not in self._folders:
            fid = self._find(name, parent, FOLDER)
            if not fid:
                meta = {"name": name, "mimeType": FOLDER, "parents": [parent]}
                fid = self.svc.files().create(body=meta, fields="id").execute()["id"]
            self._folders[key] = fid
        return self._folders[key]

    def exists(self, name, parent):
        return self._find(name, parent) is not None

    def upload(self, path, name, parent):
        meta = {"name": name, "parents": [parent]}
        self.svc.files().create(
            body=meta, media_body=MediaFileUpload(path, resumable=True), fields="id"
        ).execute()

    def load_state(self, root):
        fid = self._find(STATE_NAME, root)
        if not fid:
            return {}
        data = self.svc.files().get_media(fileId=fid).execute()
        return json.loads(data)

    def save_state(self, root, state):
        media = MediaInMemoryUpload(
            json.dumps(state, ensure_ascii=False).encode(), mimetype="application/json"
        )
        fid = self._find(STATE_NAME, root)
        if fid:
            self.svc.files().update(fileId=fid, media_body=media).execute()
        else:
            meta = {"name": STATE_NAME, "parents": [root]}
            self.svc.files().create(body=meta, media_body=media, fields="id").execute()
