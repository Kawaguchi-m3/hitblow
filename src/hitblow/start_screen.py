"""ゲーム開始時のウェルカムメッセージとルール説明。"""


def show_start_screen(digits):
    """ウェルカムメッセージを表示し、希望された場合はルールを説明する。"""
    print("Hit & Blow へようこそ！")
    print(f"今回は {digits} 桁の数字を当てるゲームです。")

    while True:
        answer = input("ルールを表示しますか？ (y/n) > ").strip().lower()
        if answer == "y":
            print(f"- {digits} 桁の数字を予想してください。")
            print("- 答えに同じ数字は重複しません。")
            print("- Hit：数字と位置の両方が一致しています。")
            print("- Blow：数字は含まれていますが、位置が違います。")
            return
        if answer == "n":
            print("それでは、ゲームを始めます！")
            return
        print("y または n を入力してください。")
