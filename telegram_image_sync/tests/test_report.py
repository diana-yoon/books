from telegram_image_sync.report import format_section


def test_format_section_with_failures():
    out = format_section({"saved": 3, "channels": {"A": 2, "B": 1, "C": 0}, "failed": ["A#9: TimeoutError"]})
    assert "신규 저장: 3장 (3개 채널 확인)" in out
    assert "· A: 2장" in out and "· C" not in out
    assert "실패 1건" in out


def test_format_section_clean():
    out = format_section({"saved": 0, "channels": {}, "failed": []})
    assert "실패: 없음" in out
