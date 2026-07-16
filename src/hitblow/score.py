# score.py

def evaluate_score(tries: int) -> tuple[int, str]:
    """回数に応じてスコアと評価メッセージを返す関数"""
    # 基本点10,000点から、1回につき1,000点減点（最低500点）
    score = max(500, 10000 - (tries * 1000))
    
    # 回数に応じたメッセージとランクの判定
    if tries <= 1:
        message = "神レベル！驚異的な運と勘です！"
    elif tries <= 4:
        message = "達人レベル！無駄のない完璧なロジックです！"
    elif tries <= 8:
        message = "優秀レベル！手堅く素晴らしい推理でした！"
    elif tries <= 12:
        message = "一般レベル！粘り強く正解にたどり着きましたね！"
    else:
        message = "見習いレベル！次はもっと少ない回数を目指そう！"
        
    return score, message