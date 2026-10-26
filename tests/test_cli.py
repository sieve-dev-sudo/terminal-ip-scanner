"""
Unit tests for scanner.cli. Argument parsing and run_targets orchestration.
"""

from scanner import cache
from scanner.cli import build_parser, entrypoint, interactive_menu, normalize_choice, run_targets


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


class TestNormalizeChoice:
    def test_single_digit_gets_zero_padded(self):
        assert normalize_choice("1") == "01"
        assert normalize_choice("2") == "02"

    def test_already_two_digit_unchanged(self):
        assert normalize_choice("01") == "01"
        assert normalize_choice("04") == "04"

    def test_extra_leading_zeros_collapse(self):
        assert normalize_choice("001") == "01"
        assert normalize_choice("0004") == "04"

    def test_lone_zero_becomes_exit_code(self):
        assert normalize_choice("0") == "00"

    def test_whitespace_is_stripped(self):
        assert normalize_choice("  2  ") == "02"

    def test_non_numeric_passes_through_unchanged(self):
        assert normalize_choice("q") == "q"
        assert normalize_choice("quit") == "quit"


class TestEntrypoint:
    def test_keyboard_interrupt_shows_session_closed(self, mocker):
        mocker.patch("scanner.cli.main", side_effect=KeyboardInterrupt)
        mock_closed = mocker.patch("scanner.display.print_session_closed")
        mock_exit = mocker.patch("scanner.cli.sys.exit")

        entrypoint()

        mock_closed.assert_called_once()
        mock_exit.assert_called_once_with(130)


class TestInteractiveMenu:
    def test_option_00_exits_immediately(self, mocker):
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch("scanner.display.prompt", return_value="00")
        mock_closed = mocker.patch("scanner.display.print_session_closed")

        interactive_menu()
        mock_closed.assert_called_once()

    def test_option_01_prompts_for_ip_then_looks_it_up(self, mocker):
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch("scanner.display.prompt", side_effect=["01", "8.8.8.8", "00"])
        mocker.patch("scanner.display.print_session_closed")
        mock_run = mocker.patch("scanner.cli.run_targets", return_value=[])

        interactive_menu()
        mock_run.assert_any_call(["8.8.8.8"], timeout=mocker.ANY)

    def test_flexible_numeric_input_matches_option_01(self, mocker):
        """"1", not just "01", should trigger the same specific-IP option."""
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch("scanner.display.prompt", side_effect=["1", "8.8.8.8", "00"])
        mocker.patch("scanner.display.print_session_closed")
        mock_run = mocker.patch("scanner.cli.run_targets", return_value=[])

        interactive_menu()
        mock_run.assert_any_call(["8.8.8.8"], timeout=mocker.ANY)

    def test_option_02_prompts_for_several_ips(self, mocker):
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch("scanner.display.prompt", side_effect=["02", "8.8.8.8 1.1.1.1", "00"])
        mocker.patch("scanner.display.print_session_closed")
        mock_run = mocker.patch("scanner.cli.run_targets", return_value=[])

        interactive_menu()
        mock_run.assert_any_call(["8.8.8.8", "1.1.1.1"], timeout=mocker.ANY)

    def test_option_03_shows_empty_history_before_any_lookup(self, mocker):
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch("scanner.display.prompt", side_effect=["03", "00"])
        mocker.patch("scanner.display.print_session_closed")
        mock_history = mocker.patch("scanner.display.print_history")

        interactive_menu()
        mock_history.assert_called_once_with([])

    def test_option_03_shows_accumulated_history_after_a_lookup(self, mocker):
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch(
            "scanner.display.prompt", side_effect=["01", "8.8.8.8", "03", "00"]
        )
        mocker.patch("scanner.display.print_session_closed")
        fake_result = {"ip": "8.8.8.8", "city": "Mountain View", "country": "US"}
        mocker.patch("scanner.cli.run_targets", return_value=[fake_result])
        mock_history = mocker.patch("scanner.display.print_history")

        interactive_menu()
        mock_history.assert_called_once_with([fake_result])

    def test_invalid_choice_shows_error_and_continues(self, mocker):
        mocker.patch("scanner.display.print_banner")
        mocker.patch("scanner.display.print_menu")
        mocker.patch("scanner.display.prompt", side_effect=["99", "00"])
        mocker.patch("scanner.display.print_session_closed")
        mock_invalid = mocker.patch("scanner.display.print_invalid_choice")

        interactive_menu()
        mock_invalid.assert_called_once_with("99")
