import random
from uuid import uuid4
from datetime import datetime


def generate_digits(length: int) -> str:
    """指定された長さのランダムな数字文字列を生成する"""
    return "".join(random.choice("0123456789") for _ in range(length))

def generate_chars(length: int, chars: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """指定された長さ of ランダムな英字文字列を生成する"""
    return "".join(random.choice(chars) for _ in range(length))

GENERAL_LOG_TEMPLATES = [
    "{value}",
]


LOG_TEMPLATES = {
    "ip_address": [
        "[{timestamp}] INFO: Connection established from {value}",
        "[{timestamp}] WARNING: Security alert - login attempt failed from {value} (user: root)",
        "[{timestamp}] ERROR: Access denied to critical resources from {value}",
        "[{timestamp}] INFO: System update downloaded from {value}",
    ],
    "email": [
        "[{timestamp}] MAIL: Delivered message to recipient <{value}> successfully.",
        "[{timestamp}] MAIL: Spam warning - quarantine flag set for sender <{value}>.",
        "[{timestamp}] MAIL: Bounce warning - target mailbox <{value}> is full.",
        "[{timestamp}] MAIL: Incoming session started from mailserver <{value}>.",
    ],
    "url": [
        "[{timestamp}] HTTP: GET requests targeting link: {value}",
        "[{timestamp}] HTTP: Redirected resource to backup node at {value}",
        "[{timestamp}] ERROR: Dead link warning reported at URL {value}",
        "[{timestamp}] INFO: Crawled external reference target: {value}",
    ],
    "mac_address": [
        "[{timestamp}] DHCP: Assigning lease to hardware ID {value}",
        "[{timestamp}] DHCP: ARP spoofing warning from address {value}",
        "[{timestamp}] INFO: Client associated with MAC {value}",
    ],
    "date": [
        "[{timestamp}] INFO: Database backup created on {value}",
        "[{timestamp}] WARN: License validation required since {value}",
        "[{timestamp}] ERROR: Log rotation task failed on date {value}",
    ]
}

def build_realistic_log(value_type: str, correct_val: str, dummies: list[str], noises: list[str]) -> str:
    """正解、ダミー、ノイズを埋め込んだ没入感のある複数行ログテキストを生成する"""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    thread_id = random.randint(1000, 9999)
    
    templates = LOG_TEMPLATES.get(value_type, GENERAL_LOG_TEMPLATES)
    lines = []
    
    # 1. 正解行を1つ追加
    correct_temp = random.choice(templates)
    lines.append(correct_temp.format(timestamp=timestamp, value=correct_val, thread_id=thread_id))
    
    # 2. ダミー行を追加
    for dummy in dummies:
        temp = random.choice(templates)
        lines.append(temp.format(timestamp=timestamp, value=dummy, thread_id=thread_id))
        
    # 3. ノイズ行を追加
    for noise in noises:
        temp = random.choice(templates)
        lines.append(temp.format(timestamp=timestamp, value=noise, thread_id=thread_id))
        
    random.shuffle(lines)
    return "\n".join(lines)

# --- Ex1 ~ Ex20 の問題生成テンプレート ---

def generate_ex1_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "文字列 'xyz' にマッチする正規表現を記述しなさい。"
    correct = "xyz"
    dummies = ["xy", "yz", "abc", "abz", "xya", "temp"]
    correct_patterns = [r"xyz"]
    dummy_patterns = [r"xy", r"yz", r"abc", r"x.z"]
    # xyzを含まないノイズのみ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!", "#", "@"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex2_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "大文字・小文字を問わず、'xyz' または 'XYZ' にマッチする正規表現を記述しなさい。※大文字小文字無視フラグは使わず、正規表現で対応すること。"
    correct = random.choice(["xyz", "XYZ"])
    dummies = ["xy", "YZ", "abc", "XyA", "xYa", "temp"]
    correct_patterns = [r"(xyz|XYZ)", r"[xX][yY][zZ]"]
    dummy_patterns = [r"xyz", r"XYZ", r"[a-z]{3}", r"x.z"]
    # xyz, XYZ を含まないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!", "#"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex3_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "先頭が 'xyz' で始まる文字列にマッチする正規表現を記述しなさい。"
    correct = "xyz" + generate_chars(2)
    dummies = ["a" + correct, "abc", "xy", "temp"]
    correct_patterns = [r"^xyz"]
    dummy_patterns = [r"xyz", r"xyz$", r"^xy", r"^[a-z]{3}"]
    # xyzを含まないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex4_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "末尾が 'xyz' で終わる文字列にマッチする正規表現を記述しなさい。"
    correct = generate_chars(2) + "xyz"
    dummies = [correct + "a", "abc", "xy", "temp"]
    correct_patterns = [r"xyz$"]
    dummy_patterns = [r"xyz", r"^xyz", r"yz$", r"[a-z]{3}$"]
    # xyzを含まないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex5_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "文字列 'xyz' と完全に一致する文字列にマッチする正規表現を記述しなさい。"
    correct = "xyz"
    dummies = ["axyz", "xyza", "abc", "xy", "temp"]
    correct_patterns = [r"^xyz$"]
    dummy_patterns = [r"xyz", r"^xyz", r"xyz$", r"^[a-z]{3}$"]
    # xyzを含まないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex6_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "'x'で始まり'z'で終わり、真ん中が任意の1文字である3文字のパターンにマッチする正規表現を記述しなさい。"
    mid = random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    correct = f"x{mid}z"
    dummies = ["xz", "xya", "yza", "abc", "axza", "temp"]
    correct_patterns = [r"x.z"]
    dummy_patterns = [r"xyz", r"x[a-z]z", r"x.*z", r"^x.z$"]
    # x.zにマッチしないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex7_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "'xyz' の前後にそれぞれ任意の1文字が存在する（計5文字）パターンにマッチする正規表現を記述しなさい。"
    correct = generate_chars(1) + "xyz" + generate_chars(1)
    dummies = ["axyz", "xyza", "xyz", "abc", "temp"]
    correct_patterns = [r".xyz."]
    dummy_patterns = [r"xyz", r"^.xyz.$", r".*xyz.*", r".{2}xyz"]
    # .xyz.にマッチしないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex8_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "文字 'x' がちょうど5回繰り返され、その後に 'yz' が続く文字列にマッチする正規表現を記述しなさい。"
    correct = "xxxxxyz"
    dummies = ["xxxxyz", "xxxxxy", "abc", "temp"]
    correct_patterns = [r"x{5}yz"]
    dummy_patterns = [r"x{4}yz", r"x+yz", r"x*yz", r"x{5}"]
    # xが5個以上連続しないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex9_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
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
    # xの繰り返しがないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex10_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "'xy' で始まり、3文字目が 'x', 'y', 'z' のいずれかであるパターンにマッチする正規表現を記述しなさい。"
    correct = "xy" + random.choice(["x", "y", "z"])
    dummies = ["xya", "xy", "abc", "xyp", "temp"]
    correct_patterns = [r"xy[xyz]"]
    dummy_patterns = [r"xy[a-z]", r"xy.", r"xy(x|y)", r"^[xyz]{3}$"]
    # xy[xyz]を含まないノイズ
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex11_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "任意の半角英小文字1文字にマッチする正規表現を記述しなさい。※先頭かつ末尾（完全一致）"
    correct = random.choice("abcdefghijklmnopqrstuvwxyz")
    # [a-z] が部分一致してしまわないよう、ダミーやノイズには「小文字を一切含まない」大文字・数字・記号のみを使用
    dummies = ["A", "9", "-", "ーー", "TEMP"]
    correct_patterns = [r"^[a-z]$"]
    dummy_patterns = [r"[a-z]", r"^[a-zA-Z]$", r"^[A-Z]$", r"^\w$"]
    pure_noises = ["TEMP", "DATA", "VAL", "TEST", "ERR", "12", "99", "83", "?", "!", "#", "@", "$", "*", "%"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex12_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "任意の半角英数字が3文字続くパターンにマッチする正規表現を記述しなさい。※先頭かつ末尾（完全一致）"
    correct = generate_chars(1) + generate_digits(1) + generate_chars(1).upper()
    # [a-zA-Z0-9]{3} が誤マッチしないよう、ダミーやノイズには「3文字以上の連続英数字を含まない」もの（2文字以下、または記号）を使用
    dummies = ["aa", "12", "X", "z", "ーーー", "ab", "99"]
    correct_patterns = [r"^[a-zA-Z0-9]{3}$"]
    dummy_patterns = [r"[a-zA-Z0-9]{3}", r"^\w{3}$", r"^[a-z]{3}$", r"^[0-9]{3}$", r"^[a-zA-Z0-9]{2}$"]
    pure_noises = ["ab", "XY", "12", "9", "A", "z", "?", "!!!", "@#$", "ーーー", "◇◇◇"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex13_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "任意の数値3桁（全角の数字も許容）にマッチする正規表現を記述しなさい。※先頭かつ末尾（完全一致）"
    correct = random.choice(["000", "１２３", "９９９", "583"])
    # \d{3} が誤マッチしないよう、ダミー・ノイズには「3桁の連続数字（全半角）を含まない」ものを使用
    dummies = ["00", "abc", "ーーー", "temp"]
    correct_patterns = [r"^\d{3}$"]
    dummy_patterns = [r"\d{3}", r"^[0-9]{3}$", r"^\d{2}$", r"^\d+$", r"^\d{4}$"]
    pure_noises = ["abc", "temp", "val", "test", "err", "12", "99", "A", "Z", "?", "!", "#", "ーーー"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex14_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "英単語 'python' が独立して含まれるパターンにマッチする正規表現を記述しなさい（apythonなどは除外）。"
    correct = "python"
    # 単語境界のテストのため、前後に英数字をくっつけたダミーを用意
    dummies = ["apython", "pythona", "python1", "abc", "temp"]
    correct_patterns = [r"\bpython\b"]
    dummy_patterns = [r"python", r"^python$", r"\s*python\s*", r"\bpython"]
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex15_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "'Red', 'Green', 'Blue' のいずれかの単語が3回繰り返されるパターンにマッチする正規表現を記述しなさい。"
    correct = "".join(random.choice(["Red", "Green", "Blue"]) for _ in range(3))
    dummies = ["RGB", "Red", "RedRed", "RedGrean", "temp"]
    correct_patterns = [r"(Red|Green|Blue){3}"]
    dummy_patterns = [r"(Red|Green|Blue)+", r"[RGB]{3}", r"(Red|Green|Blue){3}$", r"(Red|Green|Blue){2}"]
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex16_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "'国営' または '国民' の '国' 部分にマッチする正規表現を記述しなさい（'国'単体や'国家'は除外）。※置換を想定した肯定の先読みを利用すること。"
    correct = "国" + random.choice(["営", "民"])
    # マッチするのは「国」の部分だけであるため、dummiesには「国」を含まない、または条件に合わないもの
    dummies = ["国", "国家", "市営", "民", "営", "temp"]
    correct_patterns = [r"国(?=(営|民))"]
    dummy_patterns = [r"国(営|民)", r"国", r"(?<=国)(営|民)", r"国(?=(国家|民))"]
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex17_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "'ラーメン' または 'ソーメン' の 'メン' 部分にマッチする正規表現を記述しなさい（'メン'単体や'タンメン'は除外）。※置換を想定した肯定の後戻りを利用すること。"
    correct = random.choice(["ラー", "ソー"]) + "メン"
    # マッチするのは「メン」の部分だけであるため、dummiesには「メン」を含まない、または条件に合わないもの
    dummies = ["メン", "タンメン", "ソー", "ラー", "サンマーメン", "temp"]
    correct_patterns = [r"(?<=(ラー|ソー))メン"]
    dummy_patterns = [r"(ラー|ソー)メン", r"メン", r"(?<=(ラー|ソー))", r"(?<=ラー|ソー)メン"]
    pure_noises = ["temp", "data", "val", "test", "err", "12", "abc", "?", "!"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex18_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
    hint = "ファイル名チェックで、末尾が '.jpg', '.png', '.gif', '.webp' のいずれかの拡張子で終わるパターンにマッチする正規表現を記述しなさい。"
    ext = random.choice([".jpg", ".png", ".gif", ".webp"])
    correct = generate_chars(4) + ext
    dummies = ["image.jpeg", "image.jpg.", "jpg", "image.jpga", "temp"]
    correct_patterns = [r"\.(jpg|png|gif|webp)$"]
    dummy_patterns = [r"(jpg|png|gif|webp)$", r"\.(jpg|png|gif|webp)", r"\.[a-z]{3,4}$", r"\.(jpe?g|png)$"]
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!", "#", "@", "$", "*", "%"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex19_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
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
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!", "#", "@", "$", "*", "%"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

def generate_ex20_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str]]:
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
    pure_noises = ["temp", "data", "val", "test", "err", "12", "99", "abc", "?", "!", "#", "@", "$", "*", "%"]
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises

# --- アーケードモード自動生成関数 ---
def generate_arcade_problem(level: str) -> tuple[str, str, list[str], list[str], list[str], list[str], str]:
    """難易度Hard以上向けのプロシージャル問題生成ロジック。
    hint, correct_string, dummies, correct_patterns, dummy_patterns, pure_noises, value_type を返す"""
    target_types = ["ip_address", "mac_address", "url", "email", "date"]
    selected_type = random.choice(target_types)
    
    if selected_type == "ip_address":
        correct = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        dummies = [
            f"192.168",
            f"192.168.{random.randint(1, 254)}",
            f"192.168.abc.{random.randint(1, 254)}",
            f"192.168.{random.randint(1, 254)}.abc",
        ]
        correct_patterns = [r"\b192\.168\.\d{1,3}\.\d{1,3}\b", r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"]
        dummy_patterns = [r"\b\d{1,3}\.\d{1,3}\b", r"\d+", r"\b[a-zA-Z0-9.]+\b"]
        pure_noises = [
            "localhost", "dns-resolver", "auth_server",
            "node-1", "backup_service", "admin_panel"
        ]
        hint = "ログファイル等のテキストから、IPv4形式のIPアドレスを抽出する正規表現を記述しなさい。※単語境界（\\b）を利用すること"
        
    elif selected_type == "mac_address":
        def rand_hex_pair():
            return "".join(random.choice("0123456789ABCDEF") for _ in range(2))
        
        correct = ":".join(rand_hex_pair() for _ in range(6))
        dummies = [
            "-".join(rand_hex_pair() for _ in range(6)),
            ":".join(rand_hex_pair() for _ in range(5)),
            ":".join(rand_hex_pair() for _ in range(4)) + ":GG:HH",
            ":".join(rand_hex_pair() for _ in range(5)) + ":GG",
        ]
        correct_patterns = [r"\b[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}\b", r"\b[0-9A-F]{2}(:[0-9A-F]{2}){5}\b"]
        dummy_patterns = [r"\b[0-9A-Fa-f]{2}(-[0-9A-Fa-f]{2}){5}\b", r"\b[a-zA-Z0-9:]+\b", r"\w+"]
        pure_noises = [
            "001A2B3C4D5E", "123456", "UNKNOWN_DEV",
            "eth0", "wlan0", "lo"
        ]
        hint = "ログファイル等のテキストから、コロン区切り形式のMACアドレス（大文字HEX限定、例: 00:1A:2B:3C:4D:5E）を抽出する正規表現を記述しなさい。※単語境界（\\b）を利用すること"
        
    elif selected_type == "email":
        correct = f"user_{random.randint(100, 999)}@example.com"
        dummies = [
            f"user_{random.randint(100, 999)}@example",
            f"user_{random.randint(100, 999)}.example.com",
            f"@example.com",
            f"user_{random.randint(100, 999)}@.com",
        ]
        correct_patterns = [r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"]
        dummy_patterns = [r"\b[a-z]+@[a-z]+\b", r"\b[a-zA-Z0-9.]+@[a-z]+\b", r"\w+"]
        pure_noises = [
            "admin", "webmaster", "http://example.com",
            "no-reply", "mailer-daemon"
        ]
        hint = "ログファイル等のテキストから、標準的なメールアドレスの形式（例: user@example.com）を抽出する正規表現を記述しなさい。※単語境界（\\b）を利用すること"
        
    elif selected_type == "url":
        correct = f"https://server-{random.randint(1, 9)}.network.local/api"
        dummies = [
            f"http:/server-{random.randint(1, 9)}.network.local",
            f"https:server-{random.randint(1, 9)}.network.local",
            f"https://server-{random.randint(1, 9)}",
            f"ftp://server-{random.randint(1, 9)}.network.local",
        ]
        correct_patterns = [r"https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[a-zA-Z0-9_.-]*)*"]
        dummy_patterns = [r"https://[a-z]+", r"www\.[a-z]+\.com", r"[a-zA-Z0-9:/.]+"]
        pure_noises = [
            "network.local", "server-9", "api/v1/auth",
            "127.0.0.1", "localhost", "dns-resolver"
        ]
        hint = "ログファイル等のテキストから、httpまたはhttpsから始まるWebのURLを抽出する正規表現を記述しなさい。"
        
    else:  # date
        year = random.randint(2020, 2030)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        correct = f"{year:04d}-{month:02d}-{day:02d}"
        dummies = [
            f"{year:04d}/{month:02d}/{day:02d}",
            f"{year % 100:02d}-{month:02d}-{day:02d}",
            f"{year:04d}-{month:02d}-abc",
            f"{year:04d}-{month:02d}",
        ]
        correct_patterns = [r"\b\d{4}-\d{2}-\d{2}\b", r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b"]
        dummy_patterns = [r"\b\d{4}/\d{2}/\d{2}\b", r"\b\d{2}-\d{2}-\d{2}\b", r"\b\d{4}-\d{2}\b"]
        pure_noises = [
            "2026", "06-04", "LOG_DATE", "timestamp",
            "UTC", "GMT+9"
        ]
        hint = "ログファイル等のテキストから、ハイフン区切りの日付形式（YYYY-MM-DD、例: 2026-06-04）を抽出する正規表現を記述しなさい。※単語境界（\\b）を利用すること"
        
    return hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises, selected_type

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
    level = level.lower()
    if level not in ("easy", "hard"):
        level = "easy"

    if level == "hard":
        hint, correct_string, dummies, correct_patterns, dummy_patterns, pure_noises, value_type = generate_arcade_problem(level)
    else:
        generators = [
            generate_ex1_problem, generate_ex2_problem, generate_ex3_problem, generate_ex4_problem, generate_ex5_problem,
            generate_ex6_problem, generate_ex7_problem, generate_ex8_problem, generate_ex9_problem, generate_ex10_problem,
            generate_ex11_problem, generate_ex12_problem, generate_ex13_problem, generate_ex14_problem, generate_ex15_problem,
            generate_ex16_problem, generate_ex17_problem, generate_ex18_problem, generate_ex19_problem, generate_ex20_problem
        ]
        generator = random.choice(generators)
        hint, correct_string, dummies, correct_patterns, dummy_patterns, pure_noises = generator(level)
        value_type = "general"

    # 難易度に応じた純粋なノイズ数
    noise_count = random.randint(3, 6) if level == "easy" else random.randint(12, 18)
    selected_noises = [random.choice(pure_noises) for _ in range(noise_count)]

    # 没入感ログテキストとしてビルドする（改行で結合）
    noise_text = build_realistic_log(value_type, correct_string, dummies, selected_noises)

    # --- 4択の選択肢 (choices) を生成 (すべて正規表現パターン) ---
    correct_pat = random.choice(correct_patterns)
    unique_dummy_pats = list(set(dummy_patterns))
    
    if len(unique_dummy_pats) < 3:
        needed = 3 - len(unique_dummy_pats)
        for p in COMMON_DUMMY_PATTERNS:
            if p not in unique_dummy_pats and p not in correct_patterns:
                unique_dummy_pats.append(p)
                needed -= 1
                if needed == 0:
                    break
                    
    selected_dummies = random.sample(unique_dummy_pats, 3)
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
