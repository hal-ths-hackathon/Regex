import random
from uuid import uuid4

def generate_digits(length: int) -> str:
    """指定された長さのランダムな数字文字列を生成する"""
    return "".join(random.choice("0123456789") for _ in range(length))

def generate_chars(length: int, chars: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """指定された長さのランダムな英字文字列を生成する"""
    return "".join(random.choice(chars) for _ in range(length))

# --- Ex1 ~ Ex20 の問題生成テンプレート ---

def generate_ex1_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "文字列 'xyz' にマッチする正規表現を記述しなさい。"
    correct = "xyz"
    dummies = ["xy", "yz", "abc", "abz", "xya", "temp"]
    correct_patterns = [r"xyz"]
    dummy_patterns = [r"xy", r"yz", r"abc", r"x.z"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex2_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "大文字・小文字を問わず、'xyz' または 'XYZ' にマッチする正規表現を記述しなさい。※大文字小文字無視フラグは使わず、正規表現で対応すること。"
    correct = random.choice(["xyz", "XYZ"])
    dummies = ["xy", "YZ", "abc", "XYz", "xYz", "temp"]
    correct_patterns = [r"(xyz|XYZ)", r"[xX][yY][zZ]"]
    dummy_patterns = [r"xyz", r"XYZ", r"[a-z]{3}", r"x.z"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex3_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "先頭が 'xyz' で始まる文字列にマッチする正規表現を記述しなさい。"
    correct = "xyz" + generate_chars(2)
    dummies = ["a" + correct, "abc", "xy", "temp"]
    correct_patterns = [r"^xyz"]
    dummy_patterns = [r"xyz", r"xyz$", r"^xy", r"^[a-z]{3}"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex4_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "末尾が 'xyz' で終わる文字列にマッチする正規表現を記述しなさい。"
    correct = generate_chars(2) + "xyz"
    dummies = [correct + "a", "abc", "xy", "temp"]
    correct_patterns = [r"xyz$"]
    dummy_patterns = [r"xyz", r"^xyz", r"yz$", r"[a-z]{3}$"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex5_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "文字列 'xyz' と完全に一致する文字列にマッチする正規表現を記述しなさい。"
    correct = "xyz"
    dummies = ["axyz", "xyza", "abc", "xy", "temp"]
    correct_patterns = [r"^xyz$"]
    dummy_patterns = [r"xyz", r"^xyz", r"xyz$", r"^[a-z]{3}$"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex6_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "'x'で始まり'z'で終わり、真ん中が任意の1文字である3文字のパターンにマッチする正規表現を記述しなさい。"
    mid = random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    correct = f"x{mid}z"
    dummies = ["xz", "xyza", "abc", "axza", "temp"]
    correct_patterns = [r"x.z"]
    dummy_patterns = [r"xyz", r"x[a-z]z", r"x.*z", r"^x.z$"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex7_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "'xyz' の前後にそれぞれ任意の1文字が存在する（計5文字）パターンにマッチする正規表現を記述しなさい。"
    correct = generate_chars(1) + "xyz" + generate_chars(1)
    dummies = ["axyz", "xyza", "xyz", "abc", "temp"]
    correct_patterns = [r".xyz."]
    dummy_patterns = [r"xyz", r"^.xyz.$", r".*xyz.*", r".{2}xyz"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex8_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "文字 'x' がちょうど5回繰り返され、その後に 'yz' が続く文字列にマッチする正規表現を記述しなさい。"
    correct = "xxxxxyz"
    dummies = ["xxxxyz", "xxxxxy", "abc", "temp"]
    correct_patterns = [r"x{5}yz"]
    dummy_patterns = [r"x{4}yz", r"x+yz", r"x*yz", r"x{5}"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex9_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "先頭が 'x' で、'x' が5回以上8回以下繰り返され、その後に 'yz' が続くパターンにマッチする正規表現を記述しなさい。"
    correct = ("x" * random.randint(5, 8)) + "yz"
    dummies = [
        "x" * 4 + "yz",       # 4個 (過少)
        "x" * 9 + "yz",       # 9個 (過剰)
        "a" + "x" * 6 + "yz", # 先頭ではない
        "abc", "temp"
    ]
    correct_patterns = [r"^x{5,8}yz"]
    dummy_patterns = [r"x{5,8}yz", r"^x{5,}yz", r"^x{5,8}", r"^x+yz"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex10_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "'xy' で始まり、3文字目が 'x', 'y', 'z' のいずれかであるパターンにマッチする正規表現を記述しなさい。"
    correct = "xy" + random.choice(["x", "y", "z"])
    dummies = ["xya", "xy", "abc", "xyp", "temp"]
    correct_patterns = [r"xy[xyz]"]
    dummy_patterns = [r"xy[a-z]", r"xy.", r"xy(x|y)", r"^[xyz]{3}$"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex11_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "任意の半角英小文字1文字にマッチする正規表現を記述しなさい。"
    correct = random.choice("abcdefghijklmnopqrstuvwxyz")
    dummies = ["A", "9", "-", "ａ", "temp"] # ａは全角
    correct_patterns = [r"[a-z]"]
    dummy_patterns = [r"[a-zA-Z]", r"[A-Z]", r"\w", r"[a-z]{1,}"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex12_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "任意の半角英数字が3文字続くパターンにマッチする正規表現を記述しなさい。"
    correct = generate_chars(1) + generate_digits(1) + generate_chars(1).upper()
    dummies = ["aa", "---", "ａａａ", "temp"]
    correct_patterns = [r"[a-zA-Z0-9]{3}"]
    dummy_patterns = [r"\w{3}", r"[a-z]{3}", r"[0-9]{3}", r"[a-zA-Z0-9]{2}"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex13_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "任意の数値3桁（全角の数字も許容）にマッチする正規表現を記述しなさい。"
    correct = random.choice(["000", "１２３", "９９９", "583"])
    dummies = ["00", "abc", "ーーー", "temp"]
    correct_patterns = [r"\d{3}"]
    dummy_patterns = [r"[0-9]{3}", r"\d{2}", r"\d+", r"\d{4}"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex14_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "英単語 'python' が独立して含まれるパターンにマッチする正規表現を記述しなさい（apythonなどは除外）。"
    correct = "python"
    # 単語境界のテストのため、前後に英数字をくっつけたダミーを用意
    dummies = ["apython", "pythona", "python1", "abc", "temp"]
    correct_patterns = [r"\bpython\b"]
    dummy_patterns = [r"python", r"^python$", r"\s*python\s*", r"\bpython"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex15_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "'Red', 'Green', 'Blue' のいずれかの単語が3回繰り返されるパターンにマッチする正規表現を記述しなさい。"
    correct = "".join(random.choice(["Red", "Green", "Blue"]) for _ in range(3))
    dummies = ["RGB", "Red", "RedRed", "RedGrean", "temp"]
    correct_patterns = [r"(Red|Green|Blue){3}"]
    dummy_patterns = [r"(Red|Green|Blue)+", r"[RGB]{3}", r"(Red|Green|Blue){3}$", r"(Red|Green|Blue){2}"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex16_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "'国営' または '国民' の '国' 部分にマッチする正規表現を記述しなさい（'国'単体や'国家'は除外）。※置換を想定した肯定の先読みを利用すること。"
    correct = "国" + random.choice(["営", "民"])
    # マッチするのは「国」の部分だけであるため、dummiesには「国」を含まない、または条件に合わないもの
    dummies = ["国", "国家", "市営", "民", "営", "temp"]
    correct_patterns = [r"国(?=(営|民))"]
    dummy_patterns = [r"国(営|民)", r"国", r"(?<=国)(営|民)", r"国(?=(国家|民))"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex17_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "'ラーメン' または 'ソーメン' の 'メン' 部分にマッチする正規表現を記述しなさい（'メン'単体や'タンメン'は除外）。※置換を想定した肯定の後戻りを利用すること。"
    correct = random.choice(["ラー", "ソー"]) + "メン"
    # マッチするのは「メン」の部分だけであるため、dummiesには「メン」を含まない、または条件に合わないもの
    dummies = ["メン", "タンメン", "ソー", "ラー", "サンマーメン", "temp"]
    correct_patterns = [r"(?<=(ラー|ソー))メン"]
    dummy_patterns = [r"(ラー|ソー)メン", r"メン", r"(?<=(ラー|ソー))", r"(?<=ラー|ソー)メン"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex18_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "ファイル名チェックで、末尾が '.jpg', '.png', '.gif', '.webp' のいずれかの拡張子で終わるパターンにマッチする正規表現を記述しなさい。"
    ext = random.choice([".jpg", ".png", ".gif", ".webp"])
    correct = generate_chars(4) + ext
    dummies = ["image.jpeg", "image.jpg.", "jpg", "image.jpga", "temp"]
    correct_patterns = [r"\.(jpg|png|gif|webp)$"]
    dummy_patterns = [r"(jpg|png|gif|webp)$", r"\.(jpg|png|gif|webp)", r"\.[a-z]{3,4}$", r"\.(jpe?g|png)$"]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex19_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "固定10桁のクラス記号（大文字英字2桁-数値2桁大文字英字1桁-数値3桁、例: IH-12B-111）にマッチする正規表現を記述しなさい。"
    correct = f"{generate_chars(2).upper()}-{generate_digits(2)}{generate_chars(1).upper()}-{generate_digits(3)}"
    dummies = [
        correct.replace("-", ""),                 # ハイフンなし
        correct.lower(),                          # 小文字
        correct[:-1] + "A",                       # 末尾が英字
        correct[1:] + "1",                        # 桁違い
        "temp"
    ]
    correct_patterns = [r"^[A-Z]{2}-[0-9]{2}[A-Z]-[0-9]{3}$", r"^[A-Z]{2}-\d{2}[A-Z]-\d{3}$"]
    dummy_patterns = [
        r"^[a-z]{2}-[0-9]{2}[A-Z]-[0-9]{3}$",
        r"^[A-Z]{2}-[0-9]{3}-[0-9]{3}$",
        r"^[A-Z]{2}-[0-9]{2}[a-z]-[0-9]{3}$",
        r"[A-Z]{2}-[0-9]{2}[A-Z]-[0-9]{3}"
    ]
    return hint, correct, dummies, correct_patterns, dummy_patterns

def generate_ex20_problem(level: str) -> tuple[str, str, list[str], list[str], list[str]]:
    hint = "地域(t/o/n)＋校種(h/m/i)＋固定s＋数値5桁で構成される固定8桁の学籍番号（例: ths00000）にマッチする正規表現を記述しなさい。"
    reg = random.choice("ton")
    school = random.choice("hmi")
    correct = f"{reg}{school}s{generate_digits(5)}"
    dummies = [
        correct[1:],                          # 7桁 (校種抜け)
        correct + "0",                        # 9桁 (桁過剰)
        "ahs" + generate_digits(5),           # 地域違い
        correct.upper(),                      # 大文字
        "temp"
    ]
    correct_patterns = [r"^[ton][hmi]s[0-9]{5}$", r"^[ton][hmi]s\d{5}$"]
    dummy_patterns = [
        r"^[a-z]{3}[0-9]{5}$",
        r"^[ton][hmi]s[0-9]{4}$",
        r"[ton][hmi]s[0-9]{5}",
        r"^[ton][hmi]s[a-z]{5}$"
    ]
    return hint, correct, dummies, correct_patterns, dummy_patterns

# --- 汎用ダミーパターン（間違いの選択肢が不足した場合の補完用） ---
COMMON_DUMMY_PATTERNS = [
    r"^.*$",
    r"^abc$",
    r"[a-z]+",
    r"\d+",
    r"^[a-zA-Z0-9]+$"
]

def generate_stage(level: str = "easy") -> dict:
    """難易度に応じたステージデータを生成する"""
    # 難易度の正規化とバリデーション
    level = level.lower()
    if level not in ("easy", "hard"):
        level = "easy"

    # Ex1 ~ Ex20 のジェネレーターからランダムに選択
    generators = [
        generate_ex1_problem, generate_ex2_problem, generate_ex3_problem, generate_ex4_problem, generate_ex5_problem,
        generate_ex6_problem, generate_ex7_problem, generate_ex8_problem, generate_ex9_problem, generate_ex10_problem,
        generate_ex11_problem, generate_ex12_problem, generate_ex13_problem, generate_ex14_problem, generate_ex15_problem,
        generate_ex16_problem, generate_ex17_problem, generate_ex18_problem, generate_ex19_problem, generate_ex20_problem
    ]
    generator = random.choice(generators)
    hint, correct_string, dummies, correct_patterns, dummy_patterns = generator(level)

    # 難易度に応じた純粋なノイズ数
    noise_count = random.randint(3, 6) if level == "easy" else random.randint(12, 18)
    pure_noises = [
        generate_chars(random.randint(2, 4)),                      # 英字
        generate_digits(random.randint(2, 4)),                     # 数字
        f"{generate_chars(1)}{generate_digits(1)}",                # 英数混合
        random.choice(["temp", "data", "id", "val", "test", "err"]),# 固定単語
        random.choice(["?", "!", "#", "@", "$", "*", "%"]),        # 記号
    ]
    # ノイズのプールからランダムにノイズを生成する
    selected_noises = [random.choice(pure_noises) for _ in range(noise_count)]

    # 全てをマージしてシャッフル (noise_textの構築用)
    # correct_string は必ず1つだけ配置する
    elements = [correct_string] + dummies + selected_noises
    random.shuffle(elements)

    # 空白区切りで結合
    noise_text = " ".join(elements)

    # --- 4択の選択肢 (choices) を生成 (すべて正規表現パターン) ---
    # 1. 正解パターンを1つ選択
    correct_pat = random.choice(correct_patterns)
    
    # 2. ダミーパターンを3つ選択 (ダミーリストから重複なく)
    unique_dummy_pats = list(set(dummy_patterns))
    
    # もしダミーパターンが足りない場合は、汎用ダミーパターンから補充
    if len(unique_dummy_pats) < 3:
        needed = 3 - len(unique_dummy_pats)
        for p in COMMON_DUMMY_PATTERNS:
            if p not in unique_dummy_pats and p not in correct_patterns:
                unique_dummy_pats.append(p)
                needed -= 1
                if needed == 0:
                    break
                    
    selected_dummies = random.sample(unique_dummy_pats, 3)
    
    # 3. マージしてシャッフル
    choices = [correct_pat] + selected_dummies
    random.shuffle(choices)

    return {
        "stage_id": str(uuid4()),
        "hint": hint,
        "noise_text": noise_text,
        "correct_string": correct_string,
        "choices": choices,
        "correct_patterns": correct_patterns
    }
