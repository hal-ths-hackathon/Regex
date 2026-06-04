import unittest
import re

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
            self.assertIn("choices", data)
            self.assertIn("correct_patterns", data)
            
            # 各値の型検証
            self.assertIsInstance(data["stage_id"], str)
            self.assertIsInstance(data["hint"], str)
            self.assertIsInstance(data["noise_text"], str)
            self.assertIsInstance(data["correct_string"], str)
            self.assertIsInstance(data["choices"], list)
            self.assertIsInstance(data["correct_patterns"], list)
            
            # 要素の型検証
            for choice in data["choices"]:
                self.assertIsInstance(choice, str)
            for pattern in data["correct_patterns"]:
                self.assertIsInstance(pattern, str)

    def test_generate_choices_validity(self):
        """生成されたchoicesが仕様を満たしているか確認（4択の正規表現、正解パターンが1つだけ含まれ、重複がない）"""
        for level in ["easy", "hard"]:
            for _ in range(30):
                stage = generate_stage(level)
                choices = stage["choices"]
                correct_patterns = stage["correct_patterns"]
                
                # 選択肢の数が4であることを確認
                self.assertEqual(len(choices), 4)
                
                # 4つの選択肢はユニークであることを確認
                self.assertEqual(len(set(choices)), 4, f"choices {choices} must have unique values")
                
                # choices の中に correct_patterns に含まれる正解パターンがちょうど1つだけ存在することを確認
                correct_count = sum(1 for choice in choices if choice in correct_patterns)
                self.assertEqual(correct_count, 1, f"choices {choices} must contain exactly one pattern from correct_patterns {correct_patterns}")

    def test_generate_all_ex_templates(self):
        """Ex1からEx20までのすべての問題テンプレートが正常に機能し、型とデータ仕様を満たしているか確認"""
        from app.generator import (
            generate_ex1_problem, generate_ex2_problem, generate_ex3_problem, generate_ex4_problem, generate_ex5_problem,
            generate_ex6_problem, generate_ex7_problem, generate_ex8_problem, generate_ex9_problem, generate_ex10_problem,
            generate_ex11_problem, generate_ex12_problem, generate_ex13_problem, generate_ex14_problem, generate_ex15_problem,
            generate_ex16_problem, generate_ex17_problem, generate_ex18_problem, generate_ex19_problem, generate_ex20_problem
        )
        
        generators = [
            generate_ex1_problem, generate_ex2_problem, generate_ex3_problem, generate_ex4_problem, generate_ex5_problem,
            generate_ex6_problem, generate_ex7_problem, generate_ex8_problem, generate_ex9_problem, generate_ex10_problem,
            generate_ex11_problem, generate_ex12_problem, generate_ex13_problem, generate_ex14_problem, generate_ex15_problem,
            generate_ex16_problem, generate_ex17_problem, generate_ex18_problem, generate_ex19_problem, generate_ex20_problem
        ]
        
        for i, generator in enumerate(generators, 1):
            for level in ["easy", "hard"]:
                hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises = generator(level)
                
                # 各変数の型アサート
                self.assertIsInstance(hint, str, f"Ex{i} hint must be str")
                self.assertIsInstance(correct, str, f"Ex{i} correct must be str")
                self.assertIsInstance(dummies, list, f"Ex{i} dummies must be list")
                self.assertIsInstance(correct_patterns, list, f"Ex{i} correct_patterns must be list")
                self.assertIsInstance(dummy_patterns, list, f"Ex{i} dummy_patterns must be list")
                self.assertIsInstance(pure_noises, list, f"Ex{i} pure_noises must be list")
                
                # 正解パターンとダミーパターンが重複していないこと
                intersection = set(correct_patterns) & set(dummy_patterns)
                self.assertEqual(len(intersection), 0, f"Ex{i} correct and dummy patterns must not overlap: {intersection}")

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
                if level == "easy":
                    # Easy (Exercises) では各行が値そのものであるため、改行で分割してカウント
                    words = noise.split("\n")
                    self.assertEqual(words.count(correct), 1, f"correct_string '{correct}' must be present exactly once in noise_text '{noise}'")
                else:
                    # Hard (Arcade) ではテンプレート内に埋め込まれるため、部分文字列としての出現回数をカウント
                    self.assertEqual(noise.count(correct), 1, f"correct_string '{correct}' must be present exactly once in noise_text '{noise}'")

    def test_noise_text_length_by_level(self):
        """難易度(level)によってノイズの量が変化しているか確認"""
        easy_lengths = []
        hard_lengths = []
        
        for _ in range(5):
            easy_lengths.append(len(generate_stage("easy")["noise_text"].split()))
            hard_lengths.append(len(generate_stage("hard")["noise_text"].split()))
            
        # EasyとHardの平均語数を比較し、Hardのほうが明らかに多いことを確認
        avg_easy = sum(easy_lengths) / len(easy_lengths)
        avg_hard = sum(hard_lengths) / len(hard_lengths)
        self.assertGreater(avg_hard, avg_easy, f"Hard mode should have more noise than Easy mode. Easy: {avg_easy}, Hard: {avg_hard}")

    def test_correct_patterns_simulate_no_false_positives(self):
        """全20演習問題において、生成されたnoise_textに対して、
        correct_patterns のいずれかを適用したときに、correct_string にのみマッチし、
        他のダミーやノイズに誤マッチしないことを検証する（複数行ログ・グローバルマッチ版）"""
        from app.generator import (
            build_realistic_log,
            generate_ex1_problem, generate_ex2_problem, generate_ex3_problem, generate_ex4_problem, generate_ex5_problem,
            generate_ex6_problem, generate_ex7_problem, generate_ex8_problem, generate_ex9_problem, generate_ex10_problem,
            generate_ex11_problem, generate_ex12_problem, generate_ex13_problem, generate_ex14_problem, generate_ex15_problem,
            generate_ex16_problem, generate_ex17_problem, generate_ex18_problem, generate_ex19_problem, generate_ex20_problem
        )
        import random
        generators = [
            generate_ex1_problem, generate_ex2_problem, generate_ex3_problem, generate_ex4_problem, generate_ex5_problem,
            generate_ex6_problem, generate_ex7_problem, generate_ex8_problem, generate_ex9_problem, generate_ex10_problem,
            generate_ex11_problem, generate_ex12_problem, generate_ex13_problem, generate_ex14_problem, generate_ex15_problem,
            generate_ex16_problem, generate_ex17_problem, generate_ex18_problem, generate_ex19_problem, generate_ex20_problem
        ]
        
        for i, generator in enumerate(generators, 1):
            for level in ["easy", "hard"]:
                # 10回ずつ生成して検証
                for _ in range(10):
                    hint, correct, dummies, correct_patterns, dummy_patterns, pure_noises = generator(level)
                    
                    # noise_text を構築する (generate_stage と同じロジックで改行結合)
                    noise_count = random.randint(3, 6) if level == "easy" else random.randint(12, 18)
                    selected_noises = [random.choice(pure_noises) for _ in range(noise_count)]
                    noise_text = build_realistic_log("general", correct, dummies, selected_noises)
                    
                    for pattern in correct_patterns:
                        compiled = re.compile(pattern, re.MULTILINE)
                        # 行ごとに分割して検証
                        lines = noise_text.split("\n")
                        matched_correct = False
                        matched_incorrect = False
                        for line in lines:
                            has_match = compiled.search(line) is not None
                            is_correct_line = correct in line
                            if is_correct_line:
                                if has_match:
                                    matched_correct = True
                            else:
                                if has_match:
                                    matched_incorrect = True
                        
                        self.assertTrue(matched_correct, f"Ex{i} ({level}): Pattern '{pattern}' did not match the correct line in: '{noise_text}'")
                        self.assertFalse(matched_incorrect, f"Ex{i} ({level}): Pattern '{pattern}' matched an incorrect line in: '{noise_text}'")

    def test_arcade_mode_simulation(self):
        """アーケードモードで生成された問題に対して、
        correct_patterns のいずれかを適用したときに、correct_string にのみマッチし、
        他のダミーやノイズに誤マッチしないことを検証する"""
        from app.generator import generate_stage
        
        for _ in range(50):
            # Hard モードはアーケード（プロシージャル自動生成）が動く
            stage = generate_stage("hard")
            correct = stage["correct_string"]
            noise_text = stage["noise_text"]
            correct_patterns = stage["correct_patterns"]
            choices = stage["choices"]
            
            # choices の基本スキーマチェック
            self.assertEqual(len(choices), 4)
            self.assertEqual(len(set(choices)), 4)
            
            for pattern in correct_patterns:
                compiled = re.compile(pattern, re.MULTILINE)
                lines = noise_text.split("\n")
                matched_correct = False
                matched_incorrect = False
                for line in lines:
                    has_match = compiled.search(line) is not None
                    is_correct_line = correct in line
                    if is_correct_line:
                        if has_match:
                            matched_correct = True
                    else:
                        if has_match:
                            matched_incorrect = True
                
                self.assertTrue(matched_correct, f"Arcade: Pattern '{pattern}' did not match the correct line in: '{noise_text}'")
                self.assertFalse(matched_incorrect, f"Arcade: Pattern '{pattern}' matched an incorrect line in: '{noise_text}'")

if __name__ == "__main__":
    unittest.main()

