"""情報量と予想の整合性を使って、推理コストを計算する。"""

from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from math import log2

from .core import judge


SCORE_PER_UNIT = 100


def make_candidates(digits: int) -> list[str]:
    """重複のない正解候補をすべて作る。"""
    if not 1 <= digits <= 10:
        raise ValueError("digitsは1から10の範囲にしてください")
    return ["".join(candidate) for candidate in permutations("0123456789", digits)]


def information_gain(candidates: list[str], guess: str) -> float:
    """guessのHit・Blow結果から得られる期待情報量を返す。"""
    if not candidates:
        return 0.0

    result_counts = Counter(judge(secret, guess) for secret in candidates)
    total = len(candidates)
    return -sum(
        (count / total) * log2(count / total)
        for count in result_counts.values()
    )


@dataclass(frozen=True)
class TurnScore:
    """1回の予想に対するスコア計算結果。"""

    information: float
    best_information: float
    consistency: str
    turn_score: int
    total_after_turn: int
    finish_penalty: int
    final_score: int


class ScoreTracker:
    """残り候補と累計推理コストを管理する。"""

    def __init__(self, digits: int, candidates: list[str] | None = None):
        self.digits = digits
        self._starting_candidates = (
            list(candidates) if candidates is not None else make_candidates(digits)
        )
        self.reset()

    def reset(self) -> None:
        """候補と累計推理コストをゲーム開始時に戻す。"""
        self.candidates = list(self._starting_candidates)
        self._total_units = 0.0

    def _best_consistent_information(self) -> float:
        """現在の候補の中で得られる最大の期待情報量。"""
        return max(
            (information_gain(self.candidates, guess) for guess in self.candidates),
            default=0.0,
        )

    def record_guess(self, guess: str, hit: int, blow: int) -> TurnScore:
        """予想を1回記録し、候補と累計コストを更新する。"""
        candidates_before = self.candidates
        candidate_count_before = len(candidates_before)

        information = information_gain(candidates_before, guess)
        best_information = self._best_consistent_information()
        information_loss = max(0.0, best_information - information)

        is_consistent = guess in set(candidates_before)
        is_useful_probe = (
            not is_consistent
            and information > 0.0
            and information + 1e-12 >= best_information
        )

        if is_consistent:
            consistency = "整合的"
            consistency_penalty = 0
        elif is_useful_probe:
            consistency = "有効な探索"
            consistency_penalty = 0
        else:
            consistency = "不整合"
            consistency_penalty = 1

        turn_units = 1.0 + information_loss + consistency_penalty
        self._total_units += turn_units
        total_after_turn = round(SCORE_PER_UNIT * self._total_units)

        self.candidates = [
            secret
            for secret in candidates_before
            if judge(secret, guess) == (hit, blow)
        ]

        finish_units = 0.0
        if hit == self.digits and candidate_count_before > 0:
            finish_units = log2(candidate_count_before)
            self._total_units += finish_units

        return TurnScore(
            information=information,
            best_information=best_information,
            consistency=consistency,
            turn_score=round(SCORE_PER_UNIT * turn_units),
            total_after_turn=total_after_turn,
            finish_penalty=round(SCORE_PER_UNIT * finish_units),
            final_score=round(SCORE_PER_UNIT * self._total_units),
        )
