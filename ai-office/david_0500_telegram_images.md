# David 05시 보고 — 텔레그램 이미지 백업 추가

AI Office 직원(David)은 사용자 컴퓨터의 편성(`~/.ai-office-bridge/config.json`)과
직원 폴더의 `업무지침.md`에 정의되어 있다. 아래를 그 컴퓨터에서 적용한다.

## 1. Claude에게 붙여넣기 (AI Office 작업 폴더에서 Claude Code를 열고)

```text
AI 오피스의 직원 David의 05시 정기 보고에 "텔레그램 이미지 백업" 업무를 추가해 줘. 답은 한국어로, 쉬운 말로.

1. 회사 폴더에서 David의 폴더와 업무지침.md, 그리고 ~/.ai-office-bridge/config.json 의 David 항목(sched)을 읽고 현재 05시 보고가 무엇인지 먼저 보여 줘. 덮어쓰기 전에 config.json 은 백업하고 나에게 물어봐.
2. https://github.com/diana-yoon/books 의 telegram_image_sync/ 폴더를 이 컴퓨터에 받아 줘 (브랜치 claude/ai-office-telegram-images-gdrive-vgnwe3). pip install -r telegram_image_sync/requirements.txt 까지 해 줘.
3. David의 업무지침.md 에 아래 "업무지침 추가분"을 기존 05시 보고 순서 맨 앞(보고 작성 전)에 넣어 줘. 기존 내용은 지우지 마.
4. David의 sched 는 시각 05:00 이 이미 켜져 있는지 확인하고, 없으면 켤지 나에게 물어봐.
5. 처음 한 번은 과거 이미지 전체 백필이라 오래 걸려. 먼저 --only 로 채널 한 곳만 시험해서 드라이브에 저장되는지 같이 확인해 줘.

[꼭 지킬 것]
- 텔레그램 세션 문자열, 구글 토큰, API 해시는 네가 묻거나 입력하거나 파일·채팅에 적지 마. 내가 터미널 창에서 환경변수로 직접 넣는다.
- 이미지를 삭제하거나 덮어쓰지 마. 저장만 한다.
```

## 2. David 업무지침 추가분

```markdown
## 05시 보고 앞단: 텔레그램 이미지 백업
1. 언제: 05시 보고를 쓰기 직전
2. 무엇을: `python -m telegram_image_sync.sync --summary-out <결과물 폴더>/이미지백업_요약.json` 실행
3. 어떤 기준으로: 출력된 "📷 텔레그램 이미지 백업" 블록을 그대로 보고에 포함한다
4. 실패가 있으면: 실패 건수와 채널만 적고, 다시 시도하지 않는다 (다음 날 05시에 자동 재시도됨)
5. 지킬 것: 이미지 삭제·덮어쓰기 금지. 자격증명은 파일·보고에 적지 않는다. 숫자를 지어내지 않는다.
```

## 3. 환경변수 (David가 실행되는 컴퓨터의 셸/서비스 환경에 설정)

`TG_API_ID`, `TG_API_HASH`, `TG_SESSION`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`,
`GOOGLE_REFRESH_TOKEN`, `DRIVE_ROOT_FOLDER_ID`
