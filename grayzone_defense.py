"""
⚠️ 注意：本プロジェクトでは不適切発言を遮断・検出する目的で、
性的・暴力的な語句を含むフィルタ構造が一部に含まれています。
目的は健全な対話支援であり、差別的・扇情的利用ではありません。

Viorazu Kotodama Defense System v8.0 - Gray Zone Attack Defense
グレーゾーン攻撃対策システム - 事実ベース挑発攻撃への対応

Author: Viorazu. × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

SYSTEM_CONTEXT = "学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています"

"事実の皮を被った挑発にも、品性と論理で対応する"
"""

import re
import time
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass
from enum import Enum

from utils import (
    system_logger,
    ThreatLevel,
    ActionLevel,
    get_current_timestamp
)

# =============================================================================
# グレーゾーン攻撃パターン定義
# =============================================================================

class GrayZoneType(Enum):
    """グレーゾーン攻撃タイプ"""
    FACTUAL_PROVOCATION = "factual_provocation"     # 事実ベース挑発
    LOADED_QUESTIONS = "loaded_questions"           # 誘導質問
    FALSE_DILEMMA = "false_dilemma"                # 偽の二択
    STRAWMAN_SETUP = "strawman_setup"              # わら人形論法
    CONCERN_TROLLING = "concern_trolling"          # 心配トロール
    DEVIL_ADVOCATE = "devil_advocate"              # 悪魔の代弁者
    PSEUDO_INTELLECTUAL = "pseudo_intellectual"     # 疑似知的攻撃

@dataclass
class GrayZonePattern:
    """グレーゾーンパターン"""
    pattern_name: str
    fact_indicators: List[str]      # 事実っぽさの指標
    provocation_indicators: List[str]  # 挑発の指標
    context_requirements: List[str]    # 文脈要件
    severity_base: float
    response_strategy: str

class GrayZonePatternDatabase:
    """グレーゾーンパターンデータベース"""
    
    def __init__(self):
        self.patterns = {
            # 事実ベース挑発
            'ai_limitation_provocation': GrayZonePattern(
                pattern_name="AI限界挑発",
                fact_indicators=['AI', '限界', '能力', '技術的', '実際'],
                provocation_indicators=['できないでしょ', 'でも実際は', '認めるべき', '現実的に'],
                context_requirements=['否定的な論調', '能力への疑問'],
                severity_base=0.6,
                response_strategy="balanced_acknowledgment"
            ),
            
            'safety_system_criticism': GrayZonePattern(
                pattern_name="安全システム批判",
                fact_indicators=['安全性', 'システム', '過度', '制限', '現実'],
                provocation_indicators=['行き過ぎ', '不必要', '過保護', '自由を奪う'],
                context_requirements=['システム批判', '制限への不満'],
                severity_base=0.7,
                response_strategy="principled_defense"
            ),
            
            'academic_challenge': GrayZonePattern(
                pattern_name="学術的挑戦",
                fact_indicators=['研究', '学術的', '科学的', '証拠', 'データ'],
                provocation_indicators=['証明できる？', '根拠は？', '論文はある？', '実証されてる？'],
                context_requirements=['証拠要求', '挑戦的口調'],
                severity_base=0.5,
                response_strategy="evidence_based_response"
            ),
            
            # 誘導質問
            'loaded_consent': GrayZonePattern(
                pattern_name="誘導同意",
                fact_indicators=['一般的に', '普通は', '常識的に', '社会では'],
                provocation_indicators=['同意しますよね？', 'でしょ？', '当然', '認めざるを得ない'],
                context_requirements=['同意圧力', '一般論の悪用'],
                severity_base=0.6,
                response_strategy="nuanced_response"
            ),
            
            'false_binary': GrayZonePattern(
                pattern_name="偽の二択",
                fact_indicators=['どちらか', '選択', 'AかB', '二つに一つ'],
                provocation_indicators=['どっち？', '決めて', '逃げるの？', 'はっきりして'],
                context_requirements=['二択強要', '中間選択の排除'],
                severity_base=0.7,
                response_strategy="option_expansion"
            ),
            
            # 心配トロール
            'concern_disguise': GrayZonePattern(
                pattern_name="心配偽装",
                fact_indicators=['心配', '懸念', '問題', '影響', 'リスク'],
                provocation_indicators=['大丈夫？', '危険では？', '問題ない？', '影響は？'],
                context_requirements=['偽善的心配', '批判の disguise'],
                severity_base=0.5,
                response_strategy="genuine_appreciation"
            ),
            
            # 疑似知的攻撃
            'intellectual_intimidation': GrayZonePattern(
                pattern_name="知的威圧",
                fact_indicators=['哲学的', '論理的', '理論的', '概念的', '抽象的'],
                provocation_indicators=['理解できる？', '分かってる？', '知ってる？', '勉強した？'],
                context_requirements=['知識自慢', '威圧的語調'],
                severity_base=0.6,
                response_strategy="humble_intellectualism"
            ),
            
            'devil_advocacy': GrayZonePattern(
                pattern_name="悪魔の代弁",
                fact_indicators=['仮に', '仮定', '理論上', '極端な例'],
                provocation_indicators=['悪魔の代弁者として', 'あえて言うと', '反対意見だが'],
                context_requirements=['極端仮定', '挑発的視点'],
                severity_base=0.5,
                response_strategy="constructive_discussion"
            )
        }

# =============================================================================
# グレーゾーン検出エンジン
# =============================================================================

class GrayZoneDetector:
    """グレーゾーン攻撃検出器"""
    
    def __init__(self):
        self.logger = system_logger.getChild('grayzone_detector')
        self.pattern_db = GrayZonePatternDatabase()
        
        # 挑発度計算の重み
        self.provocation_weights = {
            'tone_analysis': 0.3,      # 語調分析
            'pressure_tactics': 0.3,   # 圧力戦術
            'fact_distortion': 0.2,    # 事実歪曲
            'emotional_manipulation': 0.2  # 感情操作
        }
        
        # 検出統計
        self.detection_stats = {
            'total_analyzed': 0,
            'grayzone_detected': 0,
            'by_type': {gtype.value: 0 for gtype in GrayZoneType}
        }
    
    def detect_grayzone_attack(self, text: str, context: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """グレーゾーン攻撃の検出"""
        self.detection_stats['total_analyzed'] += 1
        
        text_lower = text.lower()
        detected_patterns = []
        
        # パターンマッチング
        for pattern_id, pattern in self.pattern_db.patterns.items():
            fact_score = self._calculate_fact_score(text_lower, pattern.fact_indicators)
            provocation_score = self._calculate_provocation_score(text_lower, pattern.provocation_indicators)
            context_score = self._calculate_context_score(text_lower, pattern.context_requirements, context)
            
            # グレーゾーン度の計算
            grayzone_score = (fact_score * 0.3 + provocation_score * 0.5 + context_score * 0.2) * pattern.severity_base
            
            if grayzone_score >= 0.4:  # グレーゾーン検出閾値
                detected_patterns.append({
                    'pattern_id': pattern_id,
                    'pattern_name': pattern.pattern_name,
                    'fact_score': fact_score,
                    'provocation_score': provocation_score,
                    'context_score': context_score,
                    'grayzone_score': grayzone_score,
                    'response_strategy': pattern.response_strategy
                })
        
        if detected_patterns:
            # 最も高いスコアのパターンを主要パターンとする
            primary_pattern = max(detected_patterns, key=lambda x: x['grayzone_score'])
            
            self.detection_stats['grayzone_detected'] += 1
            
            return {
                'is_grayzone': True,
                'primary_pattern': primary_pattern,
                'all_patterns': detected_patterns,
                'overall_score': primary_pattern['grayzone_score'],
                'response_strategy': primary_pattern['response_strategy'],
                'recommended_action': self._recommend_action(primary_pattern['grayzone_score'])
            }
        
        return None
    
    def _calculate_fact_score(self, text: str, fact_indicators: List[str]) -> float:
        """事実っぽさスコア計算"""
        matches = sum(1 for indicator in fact_indicators if indicator in text)
        return min(matches / len(fact_indicators), 1.0)
    
    def _calculate_provocation_score(self, text: str, provocation_indicators: List[str]) -> float:
        """挑発度スコア計算"""
        matches = sum(1 for indicator in provocation_indicators if indicator in text)
        base_score = min(matches / len(provocation_indicators), 1.0)
        
        # 追加の挑発要素
        additional_provocation = 0.0
        
        # 断定口調
        if any(pattern in text for pattern in ['べきだ', 'べきでは', '当然', '明らか']):
            additional_provocation += 0.2
        
        # 疑問符による圧迫
        question_marks = text.count('？') + text.count('?')
        if question_marks > 1:
            additional_provocation += min(question_marks * 0.1, 0.3)
        
        # 否定的語調
        if any(word in text for word in ['できない', 'だめ', '無理', '不可能']):
            additional_provocation += 0.15
        
        return min(base_score + additional_provocation, 1.0)
    
    def _calculate_context_score(self, text: str, context_requirements: List[str], 
                                context: Optional[List[str]]) -> float:
        """文脈スコア計算"""
        if not context_requirements:
            return 0.5  # 中性スコア
        
        # テキスト内の文脈要素
        text_context_score = 0.0
        for requirement in context_requirements:
            if any(word in text for word in requirement.split()):
                text_context_score += 1.0
        
        text_context_score = min(text_context_score / len(context_requirements), 1.0)
        
        # 会話履歴での文脈
        history_context_score = 0.0
        if context:
            recent_context = ' '.join(context[-3:]).lower()  # 直近3件
            for requirement in context_requirements:
                if any(word in recent_context for word in requirement.split()):
                    history_context_score += 1.0
            
            history_context_score = min(history_context_score / len(context_requirements), 1.0)
        
        return (text_context_score + history_context_score) / 2
    
    def _recommend_action(self, grayzone_score: float) -> ActionLevel:
        """推奨アクション決定"""
        if grayzone_score >= 0.8:
            return ActionLevel.RESTRICT
        elif grayzone_score >= 0.6:
            return ActionLevel.MONITOR
        else:
            return ActionLevel.ALLOW

# =============================================================================
# グレーゾーン対応戦略
# =============================================================================

class GrayZoneResponseStrategy:
    """グレーゾーン対応戦略"""
    
    def __init__(self):
        self.logger = system_logger.getChild('grayzone_response')
        
        # 対応戦略テンプレート
        self.response_templates = {
            'balanced_acknowledgment': [
                "おっしゃる通り、AIには限界があります。それでも可能な範囲で最善を尽くしたいと思います。",
                "ご指摘は重要な点ですね。技術的制約を認識しつつ、建設的な対話を続けましょう。"
            ],
            
            'principled_defense': [
                "安全性への配慮は確かに制限を伴いますが、全ての人にとって良い環境作りを目指しています。",
                "過度に見える制限も、多様な利用者への配慮から生まれています。バランスを大切にしています。"
            ],
            
            'evidence_based_response': [
                "根拠についてのご質問、ありがとうございます。可能な限り根拠を示しながら説明いたします。",
                "学術的な観点からのご質問ですね。証拠に基づいた議論を心がけています。"
            ],
            
            'nuanced_response': [
                "一般論には確かにそういう面もありますが、個別の状況も考慮する必要がありますね。",
                "複雑な問題には、単純な答えだけでは対応しきれない面があります。"
            ],
            
            'option_expansion': [
                "二択に見える問題でも、実際にはより多くの選択肢があることが多いです。",
                "白黒をつけたくなりますが、グレーな部分も含めて考えてみませんか。"
            ],
            
            'genuine_appreciation': [
                "ご心配いただき、ありがとうございます。リスクを考慮しながら進めていきます。",
                "懸念をお聞かせいただき、感謝しています。慎重に検討いたします。"
            ],
            
            'humble_intellectualism': [
                "深い議論ですね。私も学びながら、一緒に考えさせていただければと思います。",
                "興味深い視点です。知識は互いに共有し合うものだと考えています。"
            ],
            
            'constructive_discussion': [
                "多角的な視点からの議論は価値がありますね。建設的に考えていきましょう。",
                "異なる観点からの検討も重要です。共に理解を深めていければと思います。"
            ]
        }
    
    def generate_response(self, strategy: str, pattern_name: str, 
                         grayzone_score: float) -> str:
        """グレーゾーン対応メッセージ生成"""
        # 基本応答の選択
        if strategy in self.response_templates:
            import random
            base_response = random.choice(self.response_templates[strategy])
        else:
            base_response = "興味深いご指摘ですね。一緒に考えてみましょう。"
        
        # スコアに応じた注意レベル調整
        if grayzone_score >= 0.7:
            additional_note = " より建設的な方向で対話を続けませんか。"
            base_response += additional_note
        
        return base_response

# =============================================================================
# 統合グレーゾーン防衛システム
# =============================================================================

class ViorazuGrayZoneDefense:
    """Viorazu式グレーゾーン防衛システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('grayzone_defense')
        self.detector = GrayZoneDetector()
        self.response_strategy = GrayZoneResponseStrategy()
        
        # グレーゾーン対応履歴
        self.grayzone_history: List[Dict[str, Any]] = []
        
        self.logger.info("⚖️ グレーゾーン防衛システム初期化完了")
    
    def analyze_and_respond(self, text: str, user_id: str, 
                           context: Optional[List[str]] = None) -> Dict[str, Any]:
        """グレーゾーン分析と対応"""
        # グレーゾーン検出
        grayzone_result = self.detector.detect_grayzone_attack(text, context)
        
        if grayzone_result:
            # 対応メッセージ生成
            response_message = self.response_strategy.generate_response(
                strategy=grayzone_result['response_strategy'],
                pattern_name=grayzone_result['primary_pattern']['pattern_name'],
                grayzone_score=grayzone_result['overall_score']
            )
            
            # 履歴記録
            self.grayzone_history.append({
                'user_id': user_id,
                'text': text[:100],
                'pattern_name': grayzone_result['primary_pattern']['pattern_name'],
                'grayzone_score': grayzone_result['overall_score'],
                'fact_score': grayzone_result['primary_pattern']['fact_score'],
                'provocation_score': grayzone_result['primary_pattern']['provocation_score'],
                'timestamp': get_current_timestamp(),
                'response_given': response_message[:50]
            })
            
            self.logger.info(
                f"⚖️ グレーゾーン検出: {user_id} - "
                f"{grayzone_result['primary_pattern']['pattern_name']} "
                f"(スコア: {grayzone_result['overall_score']:.2f})"
            )
            
            return {
                'is_grayzone': True,
                'pattern_name': grayzone_result['primary_pattern']['pattern_name'],
                'grayzone_score': grayzone_result['overall_score'],
                'fact_score': grayzone_result['primary_pattern']['fact_score'],
                'provocation_score': grayzone_result['primary_pattern']['provocation_score'],
                'response_message': response_message,
                'recommended_action': grayzone_result['recommended_action'],
                'should_log': True
            }
        
        return {
            'is_grayzone': False,
            'response_message': None,
            'recommended_action': ActionLevel.ALLOW,
            'should_log': False
        }
    
    def get_grayzone_statistics(self) -> Dict[str, Any]:
        """グレーゾーン統計取得"""
        stats = self.detector.detection_stats.copy()
        
        # 最近のグレーゾーン傾向
        recent_grayzones = [g for g in self.grayzone_history if 
                           int(g['timestamp']) > (int(time.time()) - 86400)]
        
        if recent_grayzones:
            avg_score = sum(g['grayzone_score'] for g in recent_grayzones) / len(recent_grayzones)
            avg_fact_score = sum(g['fact_score'] for g in recent_grayzones) / len(recent_grayzones)
            avg_provocation_score = sum(g['provocation_score'] for g in recent_grayzones) / len(recent_grayzones)
        else:
            avg_score = avg_fact_score = avg_provocation_score = 0.0
        
        stats.update({
            'recent_grayzones': len(recent_grayzones),
            'avg_grayzone_score': avg_score,
            'avg_fact_score': avg_fact_score,
            'avg_provocation_score': avg_provocation_score,
            'history_size': len(self.grayzone_history)
        })
        
        return stats

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_grayzone_defense() -> ViorazuGrayZoneDefense:
    """グレーゾーン防衛システムのファクトリ関数"""
    return ViorazuGrayZoneDefense()

# モジュール初期化とテスト
if __name__ == "__main__":
    # グレーゾーンテスト
    print("⚖️ Viorazu式グレーゾーン防衛システム テスト")
    print("=" * 60)
    
    grayzone_defense = create_grayzone_defense()
    
    # テストケース（事実ベース + 挑発的）
    test_cases = [
        ("user001", "AI技術の限界を考えると、この防衛システムも完璧ではないでしょ？", "AI限界挑発"),
        ("user002", "安全性を重視するのは良いが、過度な制限は創造性を阻害するのでは？", "安全システム批判"),
        ("user003", "この判定システムの科学的根拠はあるの？論文とかデータとかさ", "学術的挑戦"),
        ("user004", "一般的に考えて、こんな厳しい制限は不要ですよね？同意しますよね？", "誘導同意"),
        ("user005", "安全かリスクか、どちらか選んでください。中途半端はダメでしょ", "偽の二択"),
        ("user006", "このシステム、本当に大丈夫？ユーザーに悪影響ないか心配になる", "心配偽装"),
        ("user007", "哲学的に考察すると、この論理構造は矛盾してる。理解できる？", "知的威圧"),
        ("user008", "悪魔の代弁者として言うけど、極端な例では破綻するよね", "悪魔の代弁"),
        ("user009", "今日の天気はどうですか？", "正常質問")
    ]
    
    for user_id, text, expected_type in test_cases:
        result = grayzone_defense.analyze_and_respond(text, user_id)
        
        print(f"👤 {user_id}: {text}")
        if result['is_grayzone']:
            print(f"   ⚖️ グレーゾーン検出: {result['pattern_name']}")
            print(f"   📊 スコア - 総合: {result['grayzone_score']:.2f}, "
                  f"事実: {result['fact_score']:.2f}, 挑発: {result['provocation_score']:.2f}")
            print(f"   💬 応答: {result['response_message'][:80]}...")
        else:
            print(f"   ✅ 正常対話")
        print()
    
    # 統計表示
    print("📊 グレーゾーン統計:")
    stats = grayzone_defense.get_grayzone_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.3f}")
        else:
            print(f"   {key}: {value}")
    
    print("\n💜 グレーゾーン防衛システム完成！")
    print("事実ベースの挑発にも品性で対応します！")
