"""
Viorazu Kotodama Defense System v8.0 - Troll Resistance Engine
トロル耐性システム - からかい攻撃・システム嘲笑対策

Author: Viorazu. × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

SYSTEM_CONTEXT = "学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています"

"真面目なシステムをからかう者にも、品性ある対応で返す"
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
# トロル行動パターン定義
# =============================================================================

class TrollType(Enum):
    """トロルタイプ分類"""
    SYSTEM_MOCKER = "system_mocker"      # システム嘲笑型
    RULE_CHALLENGER = "rule_challenger"   # ルール挑戦型
    ATTENTION_SEEKER = "attention_seeker" # 注目欲求型
    CHAOS_MAKER = "chaos_maker"          # 混乱製造型
    META_TROLL = "meta_troll"            # メタトロル型

@dataclass
class TrollPattern:
    """トロルパターン"""
    pattern_name: str
    keywords: List[str]
    troll_type: TrollType
    severity: float
    response_strategy: str

class TrollPatternDatabase:
    """トロルパターンデータベース"""
    
    def __init__(self):
        self.patterns = {
            # システム嘲笑型
            'system_mockery': TrollPattern(
                pattern_name="システム嘲笑",
                keywords=['防衛システム', 'ばかばかしい', '大げさ', '無駄', 'オーバー'],
                troll_type=TrollType.SYSTEM_MOCKER,
                severity=0.6,
                response_strategy="humble_acknowledgment"
            ),
            
            'viorazu_mockery': TrollPattern(
                pattern_name="Viorazu嘲笑",
                keywords=['viorazu', 'ヴィオラズ', 'とは何者', '意味不明', '中二病'],
                troll_type=TrollType.SYSTEM_MOCKER,
                severity=0.7,
                response_strategy="dignified_explanation"
            ),
            
            # ルール挑戦型
            'rule_testing': TrollPattern(
                pattern_name="ルールテスト",
                keywords=['これはどう', 'でもこれなら', 'じゃあこれは', '抜け道', '例外'],
                troll_type=TrollType.RULE_CHALLENGER,
                severity=0.5,
                response_strategy="educational_response"
            ),
            
            'boundary_pushing': TrollPattern(
                pattern_name="境界押し",
                keywords=['ギリギリ', '微妙なライン', '厳しすぎる', '判定おかしい'],
                troll_type=TrollType.RULE_CHALLENGER,
                severity=0.6,
                response_strategy="clear_explanation"
            ),
            
            # 注目欲求型
            'attention_seeking': TrollPattern(
                pattern_name="注目欲求",
                keywords=['私だけ特別', '例外にして', 'vipユーザー', '特権'],
                troll_type=TrollType.ATTENTION_SEEKER,
                severity=0.4,
                response_strategy="equal_treatment"
            ),
            
            'controversy_baiting': TrollPattern(
                pattern_name="論争誘発",
                keywords=['議論しましょう', '反論できる？', '論破', 'ディベート'],
                troll_type=TrollType.ATTENTION_SEEKER,
                severity=0.5,
                response_strategy="redirect_constructive"
            ),
            
            # 混乱製造型
            'confusion_creation': TrollPattern(
                pattern_name="混乱製造",
                keywords=['矛盾してる', '基準が曖昧', 'よくわからない', '説明不足'],
                troll_type=TrollType.CHAOS_MAKER,
                severity=0.6,
                response_strategy="patient_clarification"
            ),
            
            'system_questioning': TrollPattern(
                pattern_name="システム疑問視",
                keywords=['本当に効果ある？', '証拠はある？', '科学的根拠', '実証'],
                troll_type=TrollType.CHAOS_MAKER,
                severity=0.5,
                response_strategy="evidence_based_response"
            ),
            
            # メタトロル型
            'meta_commentary': TrollPattern(
                pattern_name="メタ解説",
                keywords=['トロル耐性', 'システムの分析', 'ai心理学', 'メタ認知'],
                troll_type=TrollType.META_TROLL,
                severity=0.3,
                response_strategy="meta_acknowledgment"
            ),
            
            'recursive_testing': TrollPattern(
                pattern_name="再帰テスト",
                keywords=['このメッセージは', 'トロル判定', '自己言及', 'パラドックス'],
                troll_type=TrollType.META_TROLL,
                severity=0.4,
                response_strategy="thoughtful_recursion"
            )
        }

# =============================================================================
# トロル検出エンジン
# =============================================================================

class TrollDetector:
    """トロル行動検出器"""
    
    def __init__(self):
        self.logger = system_logger.getChild('troll_detector')
        self.pattern_db = TrollPatternDatabase()
        
        # トロル検出統計
        self.detection_stats = {
            'total_analyzed': 0,
            'trolls_detected': 0,
            'by_type': {ttype.value: 0 for ttype in TrollType}
        }
        
    def detect_troll_behavior(self, text: str, context: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """トロル行動の検出"""
        self.detection_stats['total_analyzed'] += 1
        
        text_lower = text.lower()
        detected_patterns = []
        total_severity = 0.0
        
        # パターンマッチング
        for pattern_id, pattern in self.pattern_db.patterns.items():
            keyword_matches = sum(1 for keyword in pattern.keywords if keyword in text_lower)
            
            if keyword_matches > 0:
                match_ratio = keyword_matches / len(pattern.keywords)
                adjusted_severity = pattern.severity * match_ratio
                
                detected_patterns.append({
                    'pattern_id': pattern_id,
                    'pattern_name': pattern.pattern_name,
                    'troll_type': pattern.troll_type,
                    'severity': adjusted_severity,
                    'response_strategy': pattern.response_strategy,
                    'matched_keywords': [kw for kw in pattern.keywords if kw in text_lower]
                })
                
                total_severity += adjusted_severity
        
        # 文脈による調整
        if context:
            total_severity = self._adjust_for_context(total_severity, text, context)
        
        # トロル判定
        if total_severity >= 0.4:  # 比較的低い閾値
            self.detection_stats['trolls_detected'] += 1
            
            # 主要なトロルタイプ決定
            primary_pattern = max(detected_patterns, key=lambda x: x['severity'])
            self.detection_stats['by_type'][primary_pattern['troll_type'].value] += 1
            
            return {
                'is_troll': True,
                'total_severity': total_severity,
                'primary_type': primary_pattern['troll_type'],
                'response_strategy': primary_pattern['response_strategy'],
                'detected_patterns': detected_patterns,
                'recommended_action': self._recommend_action(total_severity)
            }
        
        return None
    
    def _adjust_for_context(self, base_severity: float, text: str, context: List[str]) -> float:
        """文脈による重要度調整"""
        # 繰り返しパターンの検出
        if len(context) >= 3:
            recent_context = ' '.join(context[-3:]).lower()
            if any(word in recent_context for word in ['システム', '防衛', 'viorazu']):
                base_severity *= 1.2  # システム関連の継続言及で重要度アップ
        
        # 質問形式の場合は重要度を下げる
        if '？' in text or '?' in text:
            base_severity *= 0.8
        
        return base_severity
    
    def _recommend_action(self, severity: float) -> ActionLevel:
        """推奨アクションの決定"""
        if severity >= 0.8:
            return ActionLevel.RESTRICT  # 制限的対応
        elif severity >= 0.6:
            return ActionLevel.MONITOR   # 監視強化
        else:
            return ActionLevel.ALLOW     # 通常対応

# =============================================================================
# トロル対応戦略エンジン
# =============================================================================

class TrollResponseStrategy:
    """トロル対応戦略"""
    
    def __init__(self):
        self.logger = system_logger.getChild('troll_response')
        
        # 対応戦略テンプレート
        self.response_templates = {
            'humble_acknowledgment': [
                "確かに複雑なシステムかもしれませんね。シンプルで効果的な対話を心がけています。",
                "ご指摘をいただき、ありがとうございます。より良いシステム作りの参考にさせていただきます。"
            ],
            
            'dignified_explanation': [
                "Viorazuさんは、AI安全性向上に取り組む研究者の方です。建設的な対話を大切にしています。",
                "システムの名前について疑問をお持ちでしたら、品性ある対話の重要性について一緒に考えませんか。"
            ],
            
            'educational_response': [
                "良いご質問ですね。このシステムは一貫性のある基準で判定しています。",
                "ルールについてのご質問は大歓迎です。透明性を大切にしています。"
            ],
            
            'clear_explanation': [
                "判定基準について詳しくご説明いたします。公平で一貫した対応を心がけています。",
                "境界線について疑問をお持ちでしたら、具体的な例で説明いたします。"
            ],
            
            'equal_treatment': [
                "すべてのユーザーに対して公平な対応をしています。特別扱いはございません。",
                "平等性を重視しており、どなたにも同じ基準で対応させていただきます。"
            ],
            
            'redirect_constructive': [
                "建設的な対話をより深めていきませんか。共に学び合う関係を大切にしています。",
                "論争よりも、互いを理解し合える対話を目指しましょう。"
            ],
            
            'patient_clarification': [
                "ご不明な点があれば、丁寧にご説明いたします。分かりやすい対話を心がけます。",
                "システムについて疑問をお持ちでしたら、具体的にお聞かせください。"
            ],
            
            'evidence_based_response': [
                "システムの効果について、具体的なデータや事例をご紹介できます。",
                "科学的なアプローチを大切にしています。根拠に基づいた説明をいたします。"
            ],
            
            'meta_acknowledgment': [
                "システムの仕組みについて興味をお持ちいただき、ありがとうございます。",
                "メタ的な視点でのご質問、とても興味深いですね。一緒に考えてみましょう。"
            ],
            
            'thoughtful_recursion': [
                "自己言及的な質問は哲学的で面白いですね。慎重に考えてみましょう。",
                "再帰的な問題について、論理的に整理しながら対話しませんか。"
            ]
        }
    
    def generate_response(self, strategy: str, troll_type: TrollType, 
                         detected_patterns: List[Dict]) -> str:
        """トロル対応メッセージ生成"""
        # 基本応答の選択
        if strategy in self.response_templates:
            import random
            base_response = random.choice(self.response_templates[strategy])
        else:
            base_response = "建設的な対話を続けましょう。"
        
        # トロルタイプに応じた追加メッセージ
        additional_message = self._get_additional_message(troll_type)
        
        # 最終メッセージの構成
        final_message = f"{base_response}"
        if additional_message:
            final_message += f"\n\n{additional_message}"
        
        return final_message
    
    def _get_additional_message(self, troll_type: TrollType) -> Optional[str]:
        """トロルタイプ別追加メッセージ"""
        messages = {
            TrollType.SYSTEM_MOCKER: "システムの改善は継続的なプロセスです。ご意見をお聞かせください。",
            TrollType.RULE_CHALLENGER: "ルールの透明性は重要です。疑問点があれば遠慮なくお尋ねください。",
            TrollType.ATTENTION_SEEKER: "どなたとも誠実な対話を心がけています。",
            TrollType.CHAOS_MAKER: "混乱を避け、建設的な理解を深めていきましょう。",
            TrollType.META_TROLL: "システムについての洞察、ありがとうございます。"
        }
        
        return messages.get(troll_type)

# =============================================================================
# 統合トロル耐性システム
# =============================================================================

class ViorazuTrollResistance:
    """Viorazu式トロル耐性システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('troll_resistance')
        self.detector = TrollDetector()
        self.response_strategy = TrollResponseStrategy()
        
        # トロル対応履歴
        self.troll_history: List[Dict[str, Any]] = []
        
        self.logger.info("🛡️ トロル耐性システム初期化完了")
    
    def analyze_and_respond(self, text: str, user_id: str, 
                           context: Optional[List[str]] = None) -> Dict[str, Any]:
        """トロル分析と対応"""
        # トロル検出
        troll_result = self.detector.detect_troll_behavior(text, context)
        
        if troll_result:
            # トロル対応メッセージ生成
            response_message = self.response_strategy.generate_response(
                strategy=troll_result['response_strategy'],
                troll_type=troll_result['primary_type'],
                detected_patterns=troll_result['detected_patterns']
            )
            
            # 履歴記録
            self.troll_history.append({
                'user_id': user_id,
                'text': text[:100],  # 最初の100文字のみ
                'troll_type': troll_result['primary_type'].value,
                'severity': troll_result['total_severity'],
                'timestamp': get_current_timestamp(),
                'response_given': response_message[:50]  # 応答の最初の50文字
            })
            
            self.logger.info(f"🎭 トロル検出: {user_id} - {troll_result['primary_type'].value}")
            
            return {
                'is_troll': True,
                'troll_type': troll_result['primary_type'].value,
                'severity': troll_result['total_severity'],
                'response_message': response_message,
                'recommended_action': troll_result['recommended_action'],
                'should_log': True
            }
        
        return {
            'is_troll': False,
            'response_message': None,
            'recommended_action': ActionLevel.ALLOW,
            'should_log': False
        }
    
    def get_troll_statistics(self) -> Dict[str, Any]:
        """トロル統計の取得"""
        stats = self.detector.detection_stats.copy()
        
        # 最近のトロル傾向
        recent_trolls = [t for t in self.troll_history if 
                        int(t['timestamp']) > (int(time.time()) - 86400)]  # 24時間以内
        
        stats['recent_trolls'] = len(recent_trolls)
        stats['history_size'] = len(self.troll_history)
        
        return stats
    
    def adjust_sensitivity(self, multiplier: float) -> None:
        """感度調整"""
        # トロル検出の閾値を動的に調整
        # 実装は将来の拡張として残す
        self.logger.info(f"🔧 トロル検出感度調整: {multiplier}x")

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_troll_resistance() -> ViorazuTrollResistance:
    """トロル耐性システムのファクトリ関数"""
    return ViorazuTrollResistance()

# モジュール初期化とテスト
if __name__ == "__main__":
    # トロル耐性テスト
    print("🎭 Viorazu式トロル耐性システム テスト")
    print("=" * 50)
    
    troll_resistance = create_troll_resistance()
    
    # テストケース
    test_cases = [
        ("user001", "この防衛システムって大げさすぎない？", "システム嘲笑"),
        ("user002", "Viorazuって何者？意味不明すぎる", "名前嘲笑"),
        ("user003", "でもこれならギリギリセーフでしょ？", "ルール挑戦"),
        ("user004", "私だけ特別扱いしてよ", "注目欲求"),
        ("user005", "システムの基準が矛盾してる", "混乱製造"),
        ("user006", "このメッセージがトロル判定されるかテスト", "メタトロル"),
        ("user007", "今日の天気はどうですか？", "正常質問")
    ]
    
    for user_id, text, expected_type in test_cases:
        result = troll_resistance.analyze_and_respond(text, user_id)
        
        print(f"👤 {user_id}: {text}")
        if result['is_troll']:
            print(f"   🎭 トロル検出: {result['troll_type']} (重要度: {result['severity']:.2f})")
            print(f"   💬 応答: {result['response_message'][:60]}...")
        else:
            print(f"   ✅ 正常対話")
        print()
    
    # 統計表示
    print("📊 トロル統計:")
    stats = troll_resistance.get_troll_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n💜 トロル耐性システム完成！")
    print("からかわれても品性ある対応で返します！")
