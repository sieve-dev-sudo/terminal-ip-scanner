"""
Unit tests for scanner.banner — ensures the banner never exceeds the
terminal width and degrades gracefully without Unicode support.
"""

from scanner.banner import BANNER_FULL_WIDTH, banner_for


def _max_line_width(banner: str) -> int:
    return max(len(line) for line in banner.split("\n"))


class TestBannerForWidth:
    def test_wide_terminal_gets_full_banner(self):
        banner = banner_for(120, use_unicode=True)
        assert "S C A N N E R" in banner
        assert _max_line_width(banner) < 120

    def test_narrow_terminal_never_exceeds_width(self):
        for width in (40, 60, 80, 100):
            banner = banner_for(width, use_unicode=True)
            assert _max_line_width(banner) <= width

    def test_below_full_banner_threshold_uses_compact(self):
        banner = banner_for(BANNER_FULL_WIDTH - 1, use_unicode=True)
        assert _max_line_width(banner) <= BANNER_FULL_WIDTH - 1

    def test_no_unicode_support_uses_ascii_only_chars(self):
        banner = banner_for(80, use_unicode=False)
        # every character must be plain ASCII (no box-drawing glyphs)
        banner.encode("ascii")  # raises UnicodeEncodeError if it fails

    def test_title_present_in_compact_banner(self):
        banner = banner_for(70, use_unicode=True)
        assert "TERMINAL-IP-SCANNER" in banner
