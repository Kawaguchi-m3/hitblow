"""ゲーム終了後も残るランキングを管理する。"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable
from unicodedata import east_asian_width


RANKING_LIMIT = 10
NAME_COLUMN_WIDTH = 12
SCORE_COLUMN_WIDTH = 8
DEFAULT_RANKING_PATH = Path.home() / ".hitblow" / "ranking.json"


@dataclass(frozen=True)
class RankingEntry:
    """ランキング1件分の記録。"""

    name: str
    score: int
    tries: int
    digits: int
    recorded_at: str


def load_rankings(path: Path = DEFAULT_RANKING_PATH) -> list[RankingEntry]:
    """JSONファイルからランキングを読み込む。"""
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [RankingEntry(**item) for item in data]
    except (OSError, json.JSONDecodeError, TypeError, KeyError):
        print("ランキングファイルを読み込めませんでした。")
        return []


def save_rankings(
    entries: list[RankingEntry], path: Path = DEFAULT_RANKING_PATH
) -> None:
    """ランキングをJSONファイルへ安全に保存する。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps([asdict(entry) for entry in entries], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def rankings_for_digits(
    entries: list[RankingEntry], digits: int
) -> list[RankingEntry]:
    """同じ桁数の記録をスコアが低い順に返す。"""
    return sorted(
        (entry for entry in entries if entry.digits == digits),
        key=lambda entry: (entry.score, entry.recorded_at),
    )


def qualifies_for_ranking(
    entries: list[RankingEntry], score: int, digits: int
) -> bool:
    """スコアが同じ桁数の上位10件に入るかを返す。"""
    current = rankings_for_digits(entries, digits)
    if len(current) < RANKING_LIMIT:
        return True
    return score < current[RANKING_LIMIT - 1].score


def add_ranking(
    entries: list[RankingEntry], new_entry: RankingEntry
) -> list[RankingEntry]:
    """新しい記録を追加し、各桁数の上位10件だけを残す。"""
    other_digits = [entry for entry in entries if entry.digits != new_entry.digits]
    same_digits = rankings_for_digits(
        [*entries, new_entry], new_entry.digits
    )[:RANKING_LIMIT]
    return sorted(
        [*other_digits, *same_digits],
        key=lambda entry: (entry.digits, entry.score, entry.recorded_at),
    )


def input_name(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> str:
    """表示幅12桁以内の名前が入力されるまで繰り返す。"""
    while True:
        name = input_func("名前を入力してください > ").strip()
        if name and text_width(name) <= NAME_COLUMN_WIDTH:
            return name
        output_func("名前は表示幅12桁以内（半角12文字・全角6文字）で入力してください。")


def text_width(text: str) -> int:
    """全角文字を2桁として、文字列の表示幅を返す。"""
    return sum(2 if east_asian_width(character) in ("W", "F", "A") else 1 for character in text)


def fit_text(text: str, width: int) -> str:
    """文字列を表示幅に収め、右側を空白で揃える。"""
    fitted = ""
    fitted_width = 0
    for character in text:
        character_width = text_width(character)
        if fitted_width + character_width > width:
            break
        fitted += character
        fitted_width += character_width
    return fitted + " " * (width - fitted_width)


def show_ranking(
    entries: list[RankingEntry],
    digits: int,
    output_func: Callable[[str], None] = print,
) -> None:
    """同じ桁数のランキングを表示する。"""
    ranking = rankings_for_digits(entries, digits)
    output_func(f"\n【ランキング : {digits}桁】")
    if not ranking:
        output_func("まだ記録がありません。")
        return

    output_func(
        f"{fit_text('順位', 4)} | {fit_text('名前', NAME_COLUMN_WIDTH)}"
        f" | {fit_text('スコア', SCORE_COLUMN_WIDTH)}"
    )
    output_func(f"{'-' * 4}-+-{'-' * NAME_COLUMN_WIDTH}-+-{'-' * SCORE_COLUMN_WIDTH}")
    for rank, entry in enumerate(ranking, start=1):
        output_func(
            f"{rank:>4} | {fit_text(entry.name, NAME_COLUMN_WIDTH)}"
            f" | {entry.score:>{SCORE_COLUMN_WIDTH}}"
        )


def show_saved_ranking(
    digits: int,
    path: Path = DEFAULT_RANKING_PATH,
    output_func: Callable[[str], None] = print,
) -> None:
    """保存済みのランキングを読み込んで表示する。"""
    show_ranking(load_rankings(path), digits, output_func)


def handle_ranking(
    score: int,
    tries: int,
    digits: int,
    path: Path = DEFAULT_RANKING_PATH,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> None:
    """順位判定、名前入力、保存、ランキング表示を行う。"""
    entries = load_rankings(path)

    if qualifies_for_ranking(entries, score, digits):
        output_func("\nランキング入り！")
        name = input_name(input_func, output_func)
        new_entry = RankingEntry(
            name=name,
            score=score,
            tries=tries,
            digits=digits,
            recorded_at=datetime.now().astimezone().isoformat(timespec="seconds"),
        )
        entries = add_ranking(entries, new_entry)
        save_rankings(entries, path)
    else:
        output_func("\n今回はランキング圏外でした。")

    show_ranking(entries, digits, output_func)
