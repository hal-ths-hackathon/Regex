import unittest

# fastapi.testclient と httpx への依存を避けるため、ハンドラー関数を直接インポートしてテストします。
from app.main import generate, health
from app.generator import generate_stage

class TestRegexGameAPI(unittest.TestCase):
    def test_healthz(self):
        """ヘルスチェックエンドポイントが正常に応答することを確認"""
        res = health()
        self.assertEqual(res, {"status": "ok"})

    def test_generate_endpoint_schema(self):
        """問題生成エンドポイントが必要なキーをすべて返しているか確認"""
        for level in ["easy", "hard"]:
            data = generate(level)
            
            # スキーマ検証
            self.assertIn("stage_id", data)
            self.assertIn("hint", data)
            self.assertIn("noise_text", data)
            self.assertIn("correct_string", data)
            
            # 各値の型検証
            self.assertIsInstance(data["stage_id"], str)
            self.assertIsInstance(data["hint"], str)
            self.assertIsInstance(data["noise_text"], str)
            self.assertIsInstance(data["correct_string"], str)

    def test_generate_logic_randomness(self):
        """複数回生成したときに結果が動的に変化しているか確認"""
        results = []
        for _ in range(5):
            stage = generate_stage("easy")
            results.append((stage["correct_string"], stage["noise_text"]))
            
        # 少なくとも全てが全く同じではないことを確認 (ランダム性の担保)
        unique_results = set(results)
        self.assertGreater(len(unique_results), 1, "API should generate random dynamic problems")

    def test_correct_string_in_noise_text(self):
        """correct_string が noise_text の中にちょうど1回だけ含まれていることを確認"""
        for level in ["easy", "hard"]:
            for _ in range(5):
                stage = generate_stage(level)
                correct = stage["correct_string"]
                noise = stage["noise_text"]
                # 空白区切りで分割した単語の中に correct_string がちょうど1回だけ存在することを確認
                words = noise.split(" ")
                self.assertEqual(words.count(correct), 1, f"correct_string '{correct}' must be present exactly once in noise_text '{noise}'")

    def test_noise_text_length_by_level(self):
        """難易度(level)によってノイズの量が変化しているか確認"""
        easy_lengths = []
        hard_lengths = []
        
        for _ in range(5):
            easy_lengths.append(len(generate_stage("easy")["noise_text"].split(" ")))
            hard_lengths.append(len(generate_stage("hard")["noise_text"].split(" ")))
            
        # EasyとHardの平均語数を比較し、Hardのほうが明らかに多いことを確認
        avg_easy = sum(easy_lengths) / len(easy_lengths)
        avg_hard = sum(hard_lengths) / len(hard_lengths)
        self.assertGreater(avg_hard, avg_easy, f"Hard mode should have more noise than Easy mode. Easy: {avg_easy}, Hard: {avg_hard}")

if __name__ == "__main__":
    unittest.main()
