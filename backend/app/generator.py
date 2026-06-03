import random
from uuid import uuid4

def generate_digits(length: int) -> str:
    """指定された長さのランダムな数字文字列を生成する"""
    return "".join(random.choice("0123456789") for _ in range(length))

def generate_chars(length: int, chars: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """指定された長さのランダムな英字文字列を生成する"""
    return "".join(random.choice(chars) for _ in range(length))

def generate_zip_code_problem(level: str) -> tuple[str, str, list[str], list[str]]:
    """郵便番号問題のデータを生成する
    Returns:
        hint (str), correct_string (str), dummies (list[str]), correct_patterns (list[str])
    """
    # 正解の生成
    prefix = generate_digits(3)
    suffix = generate_digits(4)
    correct = f"{prefix}-{suffix}"

    if level == "hard":
        hint = "3桁の数字と4桁の数字がハイフンで繋がれたパターンを解除せよ"
        # Hardは正解に近いダミーを多く用意
        dummies = [
            f"{generate_digits(2)}-{generate_digits(5)}",       # 桁ずれ
            f"{generate_digits(4)}-{generate_digits(3)}",       # 桁ずれ
            f"{generate_digits(3)}-{generate_digits(3)}",       # 桁不足
            f"{generate_digits(3)}-{generate_digits(5)}",       # 桁過剰
            f"{generate_digits(3)}.{generate_digits(4)}",       # 区切り文字違い(.)
            f"{generate_digits(3)}_{generate_digits(4)}",       # 区切り文字違い(_)
            f"{generate_digits(2)}{generate_chars(1)}-{generate_digits(4)}",  # 英字混入
            f"{generate_digits(3)}-{generate_digits(3)}{generate_chars(1)}",  # 末尾英字
        ]
    else:
        hint = "3桁の数字、ハイフン、4桁の数字で構成される郵便番号（例: 123-4567）を解除せよ"
        # Easyはわかりやすいダミー
        dummies = [
            f"{generate_digits(2)}-{generate_digits(3)}",       # 明らかな桁不足
            f"{generate_digits(4)}-{generate_digits(4)}",       # 前半の桁過剰
            f"{generate_chars(3)}-{generate_chars(4)}",         # 英字のみ
            f"{generate_digits(3)}{generate_digits(4)}",        # ハイフンなし
        ]
        
    patterns = [r"^\d{3}-\d{4}$", r"^[0-9]{3}-[0-9]{4}$"]
    return hint, correct, dummies, patterns

def generate_date_problem(level: str) -> tuple[str, str, list[str], list[str]]:
    """日付問題のデータを生成する
    Returns:
        hint (str), correct_string (str), dummies (list[str]), correct_patterns (list[str])
    """
    # 正解の生成
    year = str(random.randint(1900, 2099))
    month = f"{random.randint(1, 12):02d}"
    day = f"{random.randint(1, 28):02d}" # 簡略化のため28日まで
    correct = f"{year}-{month}-{day}"

    if level == "hard":
        hint = "4桁の西暦、ハイフン、2桁の月、ハイフン、2桁の日で構成される日付（YYYY-MM-DD）"
        dummies = [
            f"{year}-{random.randint(1, 9):d}-{day}",               # 月が1桁
            f"{year}-{month}-{random.randint(1, 9):d}",               # 日が1桁
            f"{random.randint(10, 99):02d}-{month}-{day}",          # 年が2桁
            f"{year}/{month}/{day}",                                # 区切りが/
            f"{year}.{month}.{day}",                                # 区切りが.
            f"{year}-{month}-{random.randint(32, 99):02d}",          # 日の値が異常
            f"{year}-{random.randint(13, 99):02d}-{day}",          # 月の値が異常
            f"{year}-{month}a-{day}",                               # 英字混入
        ]
    else:
        hint = "西暦4桁-月2桁-日2桁の形式の日付（例: 2026-06-03）を解除せよ"
        dummies = [
            f"{year}/{month}/{day}",                                # 区切りが違う
            f"{generate_chars(4)}-{generate_chars(2)}-{generate_chars(2)}", # 英字
            f"{year}{month}{day}",                                  # ハイフンなし
            f"{random.randint(10, 99):d}-{month}-{day}",            # 年が明らかに短い
        ]

    patterns = [r"^\d{4}-\d{2}-\d{2}$", r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"]
    return hint, correct, dummies, patterns

def generate_phone_problem(level: str) -> tuple[str, str, list[str], list[str]]:
    """携帯電話番号問題のデータを生成する
    Returns:
        hint (str), correct_string (str), dummies (list[str]), correct_patterns (list[str])
    """
    carrier = random.choice(["090", "080"])
    part1 = generate_digits(4)
    part2 = generate_digits(4)
    correct = f"{carrier}-{part1}-{part2}"

    if level == "hard":
        hint = "090または080で始まり、4桁の数字、ハイフン、4桁の数字と続く携帯電話番号パターン"
        dummies = [
            f"070-{part1}-{part2}",                                # 070 (始まり違い)
            f"090-{generate_digits(3)}-{part2}",                   # 桁不足
            f"080-{part1}-{generate_digits(5)}",                   # 桁過剰
            f"{carrier}{part1}{part2}",                            # ハイフンなし
            f"{carrier}.{part1}.{part2}",                            # 区切りが.
            f"{carrier}-{part1}-{generate_digits(3)}{generate_chars(1)}", # 末尾に英字
            f"190-{part1}-{part2}",                                # 190 (始まり違い)
        ]
    else:
        hint = "090または080で始まり、ハイフンで区切られた11桁の携帯電話番号（例: 090-1234-5678）"
        dummies = [
            f"{carrier}{part1}{part2}",                            # ハイフンなし
            f"03-{part1}-{part2}",                                 # 市外局番(桁不足)
            f"abc-defg-hijk",                                      # 全て英字
        ]

    patterns = [r"^0[89]0-\d{4}-\d{4}$", r"^0(80|90)-\d{4}-\d{4}$", r"^0[89]0-[0-9]{4}-[0-9]{4}$"]
    return hint, correct, dummies, patterns

def generate_time_problem(level: str) -> tuple[str, str, list[str], list[str]]:
    """時刻問題のデータを生成する
    Returns:
        hint (str), correct_string (str), dummies (list[str]), correct_patterns (list[str])
    """
    hour = f"{random.randint(0, 23):02d}"
    minute = f"{random.randint(0, 59):02d}"
    correct = f"{hour}:{minute}"

    if level == "hard":
        hint = "2桁の時（00-23）と2桁の分（00-59）がコロンで区切られた24時間表記の時刻"
        dummies = [
            f"{random.randint(0, 9):d}:{minute}",                  # 時が1桁
            f"{hour}:{random.randint(0, 9):d}",                  # 分が1桁
            f"{random.randint(24, 99):02d}:{minute}",              # 時が範囲外
            f"{hour}:{random.randint(60, 99):02d}",              # 分が範囲外
            f"{hour}.{minute}",                                    # 区切りが.
            f"{hour}-{minute}",                                    # 区切りが-
            f"{hour}:{generate_digits(1)}{generate_chars(1)}",     # 英字混入
        ]
    else:
        hint = "HH:MM 形式の24時間表記の時刻（例: 14:30）を解除せよ"
        dummies = [
            f"{hour}{minute}",                                     # コロンなし
            f"25:00",                                              # 範囲外
            f"ab:cd",                                              # 英字のみ
        ]

    patterns = [r"^\d{2}:\d{2}$", r"^[0-9]{2}:[0-9]{2}$", r"^(0\d|1\d|2[0-3]):[0-5]\d$"]
    return hint, correct, dummies, patterns

def generate_pure_noise(count: int) -> list[str]:
    """完全なランダムノイズ（英数字や記号）を生成する"""
    noises = []
    options = [
        lambda: generate_chars(random.randint(2, 4)),                      # 英字
        lambda: generate_digits(random.randint(2, 4)),                     # 数字
        lambda: f"{generate_chars(1)}{generate_digits(1)}",                # 英数混合
        lambda: random.choice(["temp", "data", "id", "val", "test", "err"]),# 固定単語
        lambda: random.choice(["?", "!", "#", "@", "$", "*", "%"]),        # 記号単語
    ]
    for _ in range(count):
        noises.append(random.choice(options)())
    return noises

def generate_stage(level: str = "easy") -> dict:
    """難易度に応じたステージデータを生成する"""
    # 難易度の正規化とバリデーション
    level = level.lower()
    if level not in ("easy", "hard"):
        level = "easy"

    # 4つのテンプレートからランダムに1つを選択
    generators = [
        generate_zip_code_problem,
        generate_date_problem,
        generate_phone_problem,
        generate_time_problem
    ]
    generator = random.choice(generators)
    hint, correct_string, dummies, correct_patterns = generator(level)

    # 難易度に応じた純粋なノイズ数
    noise_count = random.randint(3, 6) if level == "easy" else random.randint(12, 18)
    pure_noises = generate_pure_noise(noise_count)

    # 全てをマージしてシャッフル
    # correct_string は必ず1つだけ配置する
    elements = [correct_string] + dummies + pure_noises
    random.shuffle(elements)

    # 空白区切りで結合
    noise_text = " ".join(elements)

    # 4択の選択肢を生成 (正解1つ + ダミー3つをランダム選択してシャッフル)
    selected_dummies = random.sample(dummies, 3)
    choices = [correct_string] + selected_dummies
    random.shuffle(choices)

    return {
        "stage_id": str(uuid4()),
        "hint": hint,
        "noise_text": noise_text,
        "correct_string": correct_string,
        "choices": choices,
        "correct_patterns": correct_patterns
    }
