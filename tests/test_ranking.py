"""永続化するランキングのテスト。"""

from hitblow.ranking import (
    RANKING_LIMIT,
    RankingEntry,
    add_ranking,
    handle_ranking,
    load_rankings,
    qualifies_for_ranking,
    rankings_for_digits,
    save_rankings,
    show_saved_ranking,
)


def make_entry(name: str, score: int, digits: int = 3) -> RankingEntry:
    return RankingEntry(name, score, 3, digits, "2026-07-23T12:00:00+09:00")


def test_saved_ranking_can_be_loaded_afterwards(tmp_path):
    path = tmp_path / "ranking.json"
    entries = [make_entry("太郎", 500)]

    save_rankings(entries, path)

    assert load_rankings(path) == entries


def test_ranking_keeps_only_ten_best_scores():
    entries = [make_entry(f"player{i}", 100 + i) for i in range(RANKING_LIMIT)]

    result = add_ranking(entries, make_entry("new", 50))

    ranking = rankings_for_digits(result, 3)
    assert len(ranking) == RANKING_LIMIT
    assert ranking[0].name == "new"
    assert ranking[-1].score == 108


def test_score_must_beat_tenth_place_when_ranking_is_full():
    entries = [make_entry(f"player{i}", 100 + i) for i in range(RANKING_LIMIT)]

    assert qualifies_for_ranking(entries, 108, 3)
    assert not qualifies_for_ranking(entries, 109, 3)
    assert not qualifies_for_ranking(entries, 110, 3)


def test_rankings_are_separated_by_digits():
    entries = [make_entry("three", 500, 3), make_entry("four", 100, 4)]

    assert rankings_for_digits(entries, 3) == [make_entry("three", 500, 3)]
    assert rankings_for_digits(entries, 4) == [make_entry("four", 100, 4)]


def test_name_is_requested_and_saved_only_for_ranking_score(tmp_path):
    path = tmp_path / "ranking.json"
    outputs = []

    handle_ranking(
        score=500,
        tries=3,
        digits=3,
        path=path,
        input_func=lambda prompt: "花子",
        output_func=outputs.append,
    )

    assert load_rankings(path)[0].name == "花子"
    assert "\nランキング入り！" in outputs


def test_name_is_not_requested_for_score_outside_ranking(tmp_path):
    path = tmp_path / "ranking.json"
    entries = [make_entry(f"player{i}", 100 + i) for i in range(RANKING_LIMIT)]
    save_rankings(entries, path)

    def fail_if_called(prompt):
        raise AssertionError("ランキング圏外で名前入力を求めない")

    handle_ranking(
        score=200,
        tries=10,
        digits=3,
        path=path,
        input_func=fail_if_called,
        output_func=lambda message: None,
    )

    assert load_rankings(path) == entries


def test_saved_ranking_can_be_displayed(tmp_path):
    path = tmp_path / "ranking.json"
    save_rankings([make_entry("太郎", 500)], path)
    outputs = []

    show_saved_ranking(3, path, outputs.append)

    assert "\n【ランキング : 3桁】" in outputs
    assert "   1 | 太郎         |      500" in outputs


def test_full_width_and_half_width_names_align_in_table(tmp_path):
    path = tmp_path / "ranking.json"
    save_rankings(
        [make_entry("太郎", 500), make_entry("Alice", 600)],
        path,
    )
    outputs = []

    show_saved_ranking(3, path, outputs.append)

    assert "   1 | 太郎         |      500" in outputs
    assert "   2 | Alice        |      600" in outputs


def test_name_is_limited_by_display_width():
    from hitblow.ranking import input_name

    names = iter(["あいうえおかき", "あいうえおか"])
    outputs = []

    name = input_name(lambda prompt: next(names), outputs.append)

    assert name == "あいうえおか"
    assert outputs == [
        "名前は表示幅12桁以内（半角12文字・全角6文字）で入力してください。"
    ]
