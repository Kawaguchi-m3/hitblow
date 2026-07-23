"""開始メニューのテスト。"""

from hitblow import ranking
from hitblow.start_screen import show_start_screen


def test_ranking_can_be_selected_before_game(monkeypatch):
    choices = iter(["4", "1"])
    displayed_digits = []
    monkeypatch.setattr("builtins.input", lambda prompt: next(choices))
    monkeypatch.setattr(
        ranking,
        "show_saved_ranking",
        lambda digits: displayed_digits.append(digits),
    )

    show_start_screen(3)

    assert displayed_digits == [3]
