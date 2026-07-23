"""ゲーム中の画面遷移コマンドのテスト。"""

from hitblow import game, start_screen


def test_start_command_returns_to_menu_and_quit_ends_game(monkeypatch, capsys):
    menu_digits = []
    guesses = iter(["s", "q"])

    def fake_start_screen(digits):
        menu_digits.append(digits)
        return digits

    monkeypatch.setattr(start_screen, "show_start_screen", fake_start_screen)
    monkeypatch.setattr(game, "make_secret", lambda digits: "123")
    monkeypatch.setattr("builtins.input", lambda prompt: next(guesses))

    game.play(3)
    output = capsys.readouterr().out

    assert menu_digits == [3, 3]
    assert "スタートメニューに戻ります。" in output
    assert "ゲームを終了します。" in output
