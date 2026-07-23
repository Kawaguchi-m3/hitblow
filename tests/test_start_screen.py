"""開始メニューのテスト。"""

from hitblow import ranking
from hitblow.start_screen import (
    show_commands,
    show_credits,
    show_rules,
    show_score_details,
    show_start_screen,
)


def test_ranking_can_be_selected_before_game(monkeypatch):
    choices = iter(["4", "3", "4", "1"])
    displayed_digits = []
    monkeypatch.setattr("builtins.input", lambda prompt: next(choices))
    monkeypatch.setattr(
        ranking,
        "show_saved_ranking",
        lambda digits: displayed_digits.append(digits),
    )

    selected_digits = show_start_screen(2)

    assert displayed_digits == [4]
    assert selected_digits == 2


def test_digits_can_be_changed_in_options(monkeypatch, capsys):
    choices = iter(["5", "1", "4", "4", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(choices))

    selected_digits = show_start_screen(3)
    output = capsys.readouterr().out

    assert selected_digits == 4
    assert "1. ゲームスタート（4桁）" in output


def test_invalid_digits_keep_current_setting(monkeypatch):
    choices = iter(["5", "1", "5", "4", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(choices))

    assert show_start_screen(3) == 3


def test_score_details_explain_information_formula(capsys):
    show_score_details()

    output = capsys.readouterr().out
    assert "-Σ p × log2(p)" in output
    assert "正解直前の候補数" in output


def test_credits_are_displayed(capsys):
    show_credits()

    output = capsys.readouterr().out
    assert "情報科学演習II チーム4" in output
    assert "Filament1110" in output


def test_rules_include_score_ranking_and_digit_options(capsys):
    show_rules(3)

    output = capsys.readouterr().out
    assert "Score" in output
    assert "上位10件" in output
    assert "2桁から4桁" in output


def test_command_list_includes_restart_start_and_quit(capsys):
    show_commands(3)

    output = capsys.readouterr().out
    assert "r / restart" in output
    assert "s / start" in output
    assert "q / quit" in output
