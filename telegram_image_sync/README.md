# telegram_image_sync

텔레그램 채널 이미지를 구글 드라이브에 저장한다. 이미지는 드라이브, 코드와 설정은 이 저장소에서 관리한다.

- 최초 실행: 모든 채널의 과거 이미지를 백필
- 이후 실행: 채널별 마지막 메시지 ID 이후의 새 이미지만 저장 (상태는 드라이브 `_sync_state.json`)
- 저장 경로: `<DRIVE_ROOT_FOLDER_ID>/<채널명>/<YYYY-MM>/<채널ID>_<메시지ID>.jpg`
- 중복 방지: 같은 이름의 파일이 있으면 건너뜀. 실패한 메시지 이후로는 상태를 넘기지 않아 다음 실행에서 재시도

## 실행

```bash
pip install -r telegram_image_sync/requirements.txt
python -m telegram_image_sync.sync                    # 모든 채널
python -m telegram_image_sync.sync --only "채널명"     # 일부 채널만
```

환경변수는 `sync.py` 상단 docstring 참고. Telethon 사용자 세션(`TG_SESSION`)이 있어야 가입된 채널의 과거 이미지를 받을 수 있다.

## David 05시 보고 연결

보고 직전에 `sync`를 실행하고, 출력된 `report.format_section()` 텍스트를 보고에 붙인다.
