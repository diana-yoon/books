"""David의 05시 보고에 붙이는 '텔레그램 이미지 백업' 섹션."""


def format_section(summary: dict) -> str:
    channels = summary.get("channels", {})
    saved = summary.get("saved", 0)
    failed = summary.get("failed", [])

    lines = ["📷 텔레그램 이미지 백업", f"- 신규 저장: {saved}장 ({len(channels)}개 채널 확인)"]
    for title, count in sorted(channels.items(), key=lambda kv: -kv[1]):
        if count:
            lines.append(f"  · {title}: {count}장")
    if failed:
        lines.append(f"- 실패 {len(failed)}건 (다음 실행 때 재시도)")
        for item in failed[:5]:
            lines.append(f"  · {item}")
    else:
        lines.append("- 실패: 없음")
    return "\n".join(lines)
