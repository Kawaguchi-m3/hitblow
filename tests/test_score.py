"""情報量スコアのテスト。"""

import pytest

from hitblow.score import ScoreTracker, information_gain, make_candidates


def test_three_digit_candidates_are_720_unique_numbers():
    candidates = make_candidates(3)

    assert len(candidates) == 720
    assert len(set(candidates)) == 720
    assert all(len(set(candidate)) == 3 for candidate in candidates)


def test_information_gain_is_zero_with_one_candidate():
    assert information_gain(["123"], "123") == 0.0


def test_consistent_guess_has_no_consistency_penalty():
    tracker = ScoreTracker(3, ["123", "132"])

    result = tracker.record_guess("123", 3, 0)

    assert result.consistency == "整合的"
    assert result.information == pytest.approx(1.0)
    assert result.turn_score == 100
    assert result.finish_penalty == 100
    assert result.final_score == 200


def test_useful_guess_outside_candidates_is_treated_as_probe():
    tracker = ScoreTracker(3, ["123", "132"])

    result = tracker.record_guess("120", 2, 0)

    assert result.consistency == "有効な探索"
    assert result.turn_score == 100


def test_unhelpful_guess_outside_candidates_gets_penalty():
    tracker = ScoreTracker(3, ["123", "132"])

    result = tracker.record_guess("456", 0, 0)

    assert result.consistency == "不整合"
    assert result.information == 0.0
    assert result.turn_score == 300


def test_reset_restores_candidates_and_score():
    tracker = ScoreTracker(3, ["123", "132"])
    tracker.record_guess("120", 2, 0)

    tracker.reset()
    result = tracker.record_guess("123", 3, 0)

    assert result.total_after_turn == 100
    assert result.final_score == 200
