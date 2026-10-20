"""텔레그램 채널의 이미지를 구글 드라이브에 저장한다.

최초 실행은 전체 과거 이미지를 백필하고, 이후 실행은 채널별로 마지막으로
처리한 메시지 ID 이후의 새 이미지만 저장한다. 상태는 드라이브 루트 폴더의
_sync_state.json 에 둔다 (깃에 이미지/상태를 쌓지 않기 위함).

필수 환경변수:
  TG_API_ID, TG_API_HASH, TG_SESSION      (Telethon StringSession)
  GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN
  DRIVE_ROOT_FOLDER_ID                    (이미지를 저장할 드라이브 폴더)
"""
import argparse
import asyncio
import json
import os
import re
import tempfile
from datetime import datetime, timezone

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel

from .drive import Drive
from .report import format_section


def safe(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip() or "unnamed"


def image_ext(msg):
    if msg.photo:
        return ".jpg"
    doc = msg.document
    if doc and (doc.mime_type or "").startswith("image/"):
        return (msg.file.ext if msg.file and msg.file.ext else ".img")
    return None


async def sync(tg, drive, root, only=None):
    state = drive.load_state(root)
    summary = {"date": datetime.now(timezone.utc).isoformat(), "channels": {}, "saved": 0, "failed": []}

    async for dialog in tg.iter_dialogs():
        ent = dialog.entity
        if not isinstance(ent, Channel):
            continue
        title = ent.title
        if only and title not in only and str(dialog.id) not in only:
            continue

        key = str(dialog.id)
        last = state.get(key, 0)
        advance = last          # 실패한 메시지 이후로는 상태를 넘기지 않는다
        blocked = False
        saved = 0

        async for msg in tg.iter_messages(ent, min_id=last, reverse=True):
            ext = image_ext(msg)
            if ext:
                name = f"{key}_{msg.id}{ext}"
                month = msg.date.astimezone(timezone.utc).strftime("%Y-%m")
                parent = drive.folder(drive.folder(root, safe(title)), month)
                try:
                    if not drive.exists(name, parent):
                        with tempfile.TemporaryDirectory() as tmp:
                            path = await msg.download_media(file=os.path.join(tmp, name))
                            drive.upload(path, name, parent)
                        saved += 1
                except Exception as exc:  # noqa: BLE001 - 한 장 실패로 전체를 멈추지 않는다
                    blocked = True
                    summary["failed"].append(f"{title}#{msg.id}: {type(exc).__name__}")
            if not blocked:
                advance = msg.id

        state[key] = advance
        summary["channels"][title] = saved
        summary["saved"] += saved
        drive.save_state(root, state)

    return summary


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="채널 이름 또는 ID (생략 시 모든 채널)")
    ap.add_argument("--summary-out", help="요약 JSON 저장 경로")
    args = ap.parse_args()

    tg = TelegramClient(
        StringSession(os.environ["TG_SESSION"]),
        int(os.environ["TG_API_ID"]),
        os.environ["TG_API_HASH"],
    )
    async with tg:
        summary = await sync(tg, Drive(), os.environ["DRIVE_ROOT_FOLDER_ID"], args.only)

    if args.summary_out:
        with open(args.summary_out, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    print(format_section(summary))


if __name__ == "__main__":
    asyncio.run(main())
