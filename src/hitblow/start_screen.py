"""ゲーム開始時のメニュー、ルール、コマンド説明。"""


def show_rules(digits):
    """ゲームのルールを表示する。"""
    print("\n【ルール】")
    print(f"- {digits} 桁の数字を予想してください。")
    print("- 答えに同じ数字は重複しません。")
    print("- Hit：数字と位置の両方が一致しています。")
    print("- Blow：数字は含まれていますが、位置が違います。")


def show_commands(digits):
    """ゲーム中に利用できる入力とコマンドを表示する。"""
    print("\n【コマンド】")
    print(f"- {digits} 桁の数字：答えを予想します。")
    print("- r / restart：答えと挑戦回数をリセットします。")


def show_start_screen(digits):
    """開始メニューを表示し、ゲーム開始まで選択を受け付ける。"""
    print("=" * 32)
    print("  Hit & Blow へようこそ！")
    print("=" * 32)

    while True:
        print("\n1. ゲームスタート")
        print("2. ルール表示")
        print("3. コマンド表示")
        print("4. ランキング表示")
        choice = input("選択してください > ").strip()

        if choice == "1":
            print("ゲームを始めます！")
            return
        if choice == "2":
            show_rules(digits)
            continue
        if choice == "3":
            show_commands(digits)
            continue
        if choice == "4":
            from .ranking import show_saved_ranking

            show_saved_ranking(digits)
            continue

        print("1、2、3、4のいずれかを入力してください。")
