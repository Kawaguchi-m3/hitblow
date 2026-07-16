"""ゲームのリスタート機能。"""

from .core import make_secret


def restart(digits):
    """新しい secret と tries=0 を返す（リスタート後の状態）。"""
    print("リスタートしました！")
    return make_secret(digits), 0