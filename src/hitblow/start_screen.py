"""ゲーム開始時のメニュー、ルール、オプション。"""


MIN_DIGITS = 2
MAX_DIGITS = 4


def show_rules(digits):
    """ゲームのルールを表示する。"""
    print("\n【ルール】")
    print(f"- {digits} 桁の数字を予想してください。")
    print("- 答えに同じ数字は重複しません。")
    print("- Hit：数字と位置の両方が一致しています。")
    print("- Blow：数字は含まれていますが、位置が違います。")
    print("- Score：予想の情報量から計算し、低いほど優秀です。")
    print("- 正解後、同じ桁数の上位10件に入ると名前を登録できます。")
    print(f"- 桁数はオプションで{MIN_DIGITS}桁から{MAX_DIGITS}桁に変更できます。")


def show_commands(digits):
    """ゲーム中に利用できる入力とコマンドを表示する。"""
    print("\n【コマンド】")
    print(f"- {digits} 桁の数字：答えを予想します。")
    print("- r / restart：答えと挑戦回数をリセットします。")
    print("- s / start：現在のゲームを破棄し、スタートメニューに戻ります。")
    print("- q / quit：ゲームを終了します。")


def show_score_details():
    """情報量スコアの計算方法を表示する。"""
    print("\n【スコア計算方法】")
    print("- 合計スコアが低いほど優秀です。")
    print("- 1回の予想 = 100 × (1 + 情報損失 + 不整合ペナルティ)")
    print("- 期待情報量 = -Σ p × log2(p)")
    print("- 情報損失は、整合的な最善手と入力した予想の情報量の差です。")
    print("- 過去の判定と矛盾し、情報上の利点もない予想に100を加えます。")
    print("- 正解時は 100 × log2(正解直前の候補数) を加えます。")


def show_credits():
    """ゲームのクレジットを表示する。"""
    print("\n【クレジット】")
    print("制作：情報科学演習II チーム4")
    print("Filament1110\nweekaaaa\nKawaguchi-m3\nSuoefer")


def change_digits(current_digits):
    """2桁から4桁の新しい桁数を返す。"""
    value = input(f"桁数を入力してください（{MIN_DIGITS}〜{MAX_DIGITS}） > ").strip()
    if value.isdigit() and MIN_DIGITS <= int(value) <= MAX_DIGITS:
        digits = int(value)
        print(f"{digits}桁に変更しました。")
        return digits

    print(f"桁数は{MIN_DIGITS}から{MAX_DIGITS}で入力してください。")
    return current_digits


def show_options(digits):
    """オプションを表示し、選択された桁数を返す。"""
    while True:
        print("\n【オプション】")
        print(f"1. 桁数変更（現在：{digits}桁）")
        print("2. スコア計算方法")
        print("3. クレジット")
        print("4. スタートメニューに戻る")
        choice = input("選択してください > ").strip()

        if choice == "1":
            digits = change_digits(digits)
            continue
        if choice == "2":
            show_score_details()
            continue
        if choice == "3":
            show_credits()
            continue
        if choice == "4":
            return digits

        print("1、2、3、4のいずれかを入力してください。")


def show_ranking_menu():
    """桁数を選んで保存済みランキングを表示する。"""
    from .ranking import show_saved_ranking

    while True:
        print("\n【ランキング表示】")
        print("1. 2桁ランキング")
        print("2. 3桁ランキング")
        print("3. 4桁ランキング")
        print("4. スタートメニューに戻る")
        choice = input("選択してください > ").strip()

        if choice in ("1", "2", "3"):
            show_saved_ranking(int(choice) + 1)
            continue
        if choice == "4":
            return

        print("1、2、3、4のいずれかを入力してください。")


def show_start_screen(digits):
    """開始メニューを表示し、選択された桁数を返す。"""
    print("=" * 32)
    print("  Hit & Blow へようこそ！")
    print("=" * 32)

    while True:
        print(f"\n1. ゲームスタート（{digits}桁）")
        print("2. ルール表示")
        print("3. コマンド表示")
        print("4. ランキング表示")
        print("5. オプション")
        choice = input("選択してください > ").strip()

        if choice == "1":
            print("ゲームを始めます！")
            return digits
        if choice == "2":
            show_rules(digits)
            continue
        if choice == "3":
            show_commands(digits)
            continue
        if choice == "4":
            show_ranking_menu()
            continue
        if choice == "5":
            digits = show_options(digits)
            continue

        print("1、2、3、4、5のいずれかを入力してください。")
