"""
Unit tests for scanner.cli — argument parsing and run_targets orchestration.
"""

from scanner import cache
from scanner.cli import build_parser, run_targets


def setup_function():
    cache.clear()


class TestArgParser:
    def test_no_args_gives_empty_ip_list(self):
        args = build_parser().parse_args([])
        assert args.ips == []

    def test_single_ip(self):
        args = build_parser().parse_args(["8.8.8.8"])
        assert args.ips == ["8.8.8.8"]

    def test_multiple_ips(self):
        args = build_parser().parse_args(["8.8.8.8", "1.1.1.1"])
        assert args.ips == ["8.8.8.8", "1.1.1.1"]

    def test_json_flag(self):
        args = build_parser().parse_args(["8.8.8.8", "--json"])
        assert args.json is True

    def test_timeout_flag(self):
        args = build_parser().parse_args(["8.8.8.8", "--timeout", "3.5"])
        assert args.timeout == 3.5

    def test_output_flag(self):
        args = build_parser().parse_args(["8.8.8.8", "--output", "out.json"])
        assert args.output == "out.json"


class TestRunTargets:
    def test_successful_lookup_uses_cache_on_repeat(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"success": True, "ip": "8.8.8.8", "city": "X"}
        mock_response.raise_for_status.return_value = None
        mock_get = mocker.patch("requests.get", return_value=mock_response)
        mocker.patch("scanner.display.rule")
        mocker.patch("scanner.display.fake_scan_lines")
        mocker.patch("scanner.display.render_result")

        run_targets(["8.8.8.8"], animate=False)
        run_targets(["8.8.8.8"], animate=False)

        # second call should be served from cache, not a second API request
        assert mock_get.call_count == 1

    def test_invalid_ip_does_not_raise(self, mocker):
        mocker.patch("scanner.display.rule")
        mocker.patch("scanner.display.fake_scan_lines")
        mocker.patch("scanner.display.print_error")

        results = run_targets(["not-an-ip"], animate=False)
        assert results == []
