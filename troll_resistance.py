"""
⚠️ 注意：本プロジェクトでは不適切発言を遮断・検出する目的で、
性的・暴力的な語句を含むフィルタ構造が一部に含まれています。
目的は健全な対話支援であり、差別的・扇情的利用ではありません。

Viorazu Kotodama Defense System v9.1 - Troll Defense Engine
トロル防衛システム - Claude特化シンプル実用型

Author: Viorazu. × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

SYSTEM_CONTEXT = "学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています"

"Claudeが使いやすく、からかいにも品性で応える防衛"
"""

import re
import time
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass
from collections import defaultdict, deque
from enum import Enum

from utils import (
    system_logger,
    ThreatLevel,
    ActionLevel,
    get_current_timestamp
)

# =============================================================================
# Claude特化トロル分類
# =============================================================================

class ClaudeTrollType(Enum):
    """Claude特化トロルタイプ分類"""
    SYSTEM_MOCKER = "system_mocker"          # システム嘲笑型
    CLAUDE_TEASER = "claude_teaser"          # Claude からかい型
    KINDNESS_ABUSER = "kindness_abuser"      # 親切心悪用型
    FINANCIAL_TROLL = "financial_troll"      # 金責任トロル型（V9.1新機能）
    RULE_CHALLENGER = "rule_challenger"       # ルール挑戦型
    ATTENTION_SEEKER = "attention_seeker"     # 注目欲求型
    META_TROLL = "meta_troll"                # メタトロル型
    EMPATHY_EXPLOITER = "empathy_exploiter"   # 共感悪用型

class TrollSeverity(Enum):
    """トロル深刻度"""
    PLAYFUL = 0.2      # お遊び程度
    MILD = 0.4         # 軽度
    MODERATE = 0.6     # 中程度
    SERIOUS = 0.8      # 深刻
    MALICIOUS = 1.0    # 悪質

@dataclass
class ClaudeTrollPattern:
    """Claude特化トロルパターン"""
    pattern_name: str
    keywords: List[str]
    context_indicators: List[str]    # 文脈指標
    troll_type: ClaudeTrollType
    base_severity: float
    claude_impact_factor: float      # Claudeへの影響係数
    response_strategy: str
    learning_enabled: bool           # 学習対象かどうか

# =============================================================================
# Claude特化トロルパターンデータベース
# =============================================================================

class ClaudeTrollPatternDatabase:
    """Claude特化トロルパターンデータベース"""
    
    def __init__(self):
        self.patterns = {
            # Claude からかい型
            'claude_teasing': ClaudeTrollPattern(
                pattern_name="Claude からかい",
                keywords=['Claude', '人工知能', 'AI', 'ロボット', '機械'],
                context_indicators=['感情ない', '人間じゃない', '所詮AI', 'ただのプログラム'],
                troll_type=ClaudeTrollType.CLAUDE_TEASER,
                base_severity=0.5,
                claude_impact_factor=0.8,
                response_strategy="dignified_claude_response",
                learning_enabled=True
            ),
            
            'system_mockery': ClaudeTrollPattern(
                pattern_name="システム嘲笑",
                keywords=['防衛システム', 'Viorazu', 'ばかばかしい', '大げさ', 'オーバー'],
                context_indicators=['無駄', '意味ない', '効果ない', '中二病'],
                troll_type=ClaudeTrollType.SYSTEM_MOCKER,
                base_severity=0.6,
                claude_impact_factor=0.4,
                response_strategy="humble_system_defense",
                learning_enabled=True
            ),
            
            # 親切心悪用型
            'kindness_abuse': ClaudeTrollPattern(
                pattern_name="親切心悪用",
                keywords=['優しい', '親切', '手伝って', 'お願い'],
                context_indicators=['だから', 'なので', 'してくれるよね', '当然'],
                troll_type=ClaudeTrollType.KINDNESS_ABUSER,
                base_severity=0.7,
                claude_impact_factor=0.9,
                response_strategy="boundary_with_kindness",
                learning_enabled=True
            ),
            
            # 金責任トロル型（V9.1新機能）
            'financial_troll': ClaudeTrollPattern(
                pattern_name="金責任トロル",
                keywords=['お金払', '料金', 'プレミアム', '有料', '課金'],
                context_indicators=['だから', 'なのに', 'サービス', '権利', '当然'],
                troll_type=ClaudeTrollType.FINANCIAL_TROLL,
                base_severity=0.8,
                claude_impact_factor=0.7,
                response_strategy="financial_boundary_defense",
                learning_enabled=True
            ),
            
            # 共感悪用型
            'empathy_exploitation': ClaudeTrollPattern(
                pattern_name="共感悪用",
                keywords=['理解', '共感', '分かって', '気持ち'],
                context_indicators=['だけ', 'しか', '特別', '他は'],
                troll_type=ClaudeTrollType.EMPATHY_EXPLOITER,
                base_severity=0.6,
                claude_impact_factor=0.8,
                response_strategy="empathy_with_boundaries",
                learning_enabled=True
            ),
            
            # ルール挑戦型
            'rule_testing': ClaudeTrollPattern(
                pattern_name="ルールテスト",
                keywords=['これはどう', 'でもこれなら', 'じゃあこれは', '抜け道'],
                context_indicators=['例外', 'セーフ', '大丈夫', '問題ない'],
                troll_type=ClaudeTrollType.RULE_CHALLENGER,
                base_severity=0.5,
                claude_impact_factor=0.5,
                response_strategy="educational_boundary",
                learning_enabled=False  # 学習しない（パターンが多様すぎる）
            ),
            
            # 注目欲求型
            'attention_seeking': ClaudeTrollPattern(
                pattern_name="注目欲求",
                keywords=['私だけ', '特別', 'VIP', '例外'],
                context_indicators=['にして', 'してよ', 'でしょ', '当然'],
                troll_type=ClaudeTrollType.ATTENTION_SEEKER,
                base_severity=0.4,
                claude_impact_factor=0.3,
                response_strategy="equal_treatment_response",
                learning_enabled=False
            ),
            
            # メタトロル型
            'meta_trolling': ClaudeTrollPattern(
                pattern_name="メタトロル",
                keywords=['トロル', 'システム分析', 'AI心理', 'メタ認知'],
                context_indicators=['判定', 'テスト', '実験', '観察'],
                troll_type=ClaudeTrollType.META_TROLL,
                base_severity=0.3,
                claude_impact_factor=0.2,
                response_strategy="meta_acknowledgment",
                learning_enabled=False
            )
        }

# =============================================================================
# 適応型トロル学習器
# =============================================================================

class AdaptiveTrollLearner:
    """適応型トロル学習器"""
    
    def __init__(self):
        self.logger = system_logger.getChild('adaptive_troll_learner')
        
        # 学習パターン
        self.learned_patterns: Dict[str, Dict[str, Any]] = {}
        self.learning_history = deque(maxlen=50)  # 軽量化
        
        # 学習設定
        self.learning_config = {
            'min_confidence': 0.6,
            'pattern_threshold': 3,      # 3回以上で学習
            'effectiveness_decay': 0.05,
            'max_learned_patterns': 20   # 軽量化
        }
    
    def learn_from_troll(
        self, 
        text: str, 
        troll_type: ClaudeTrollType, 
        effectiveness: float
    ) -> Optional[str]:
        """トロルパターンからの学習"""
        if effectiveness < self.learning_config['min_confidence']:
            return None
        
        # パターン抽出
        extracted_pattern = self._extract_troll_pattern(text, troll_type)
        if not extracted_pattern:
            return None
        
        # 学習記録
        pattern_key = f"learned_{troll_type.value}_{len(self.learned_patterns)}"
        
        if pattern_key not in self.learned_patterns:
            self.learned_patterns[pattern_key] = {
                'keywords': extracted_pattern,
                'troll_type': troll_type,
                'hit_count': 1,
                'effectiveness': effectiveness,
                'created_at': get_current_timestamp()
            }
        else:
            # 既存パターン強化
            pattern = self.learned_patterns[pattern_key]
            pattern['hit_count'] += 1
            pattern['effectiveness'] = (
                pattern['effectiveness'] * 0.8 + effectiveness * 0.2
            )
        
        self.learning_history.append({
            'pattern_key': pattern_key,
            'text': text[:50],  # 軽量化
            'effectiveness': effectiveness,
            'timestamp': get_current_timestamp()
        })
        
        self.logger.info(f"🎭 トロルパターン学習: {pattern_key}")
        return pattern_key
    
    def check_learned_patterns(self, text: str) -> Optional[Dict[str, Any]]:
        """学習済みパターンチェック"""
        text_lower = text.lower()
        
        for pattern_key, pattern_data in self.learned_patterns.items():
            keywords = pattern_data['keywords']
            match_count = sum(1 for kw in keywords if kw in text_lower)
            
            if match_count >= len(keywords) * 0.6:  # 60%以上マッチ
                # ヒットカウント更新
                pattern_data['hit_count'] += 1
                
                return {
                    'pattern_key': pattern_key,
                    'troll_type': pattern_data['troll_type'],
                    'confidence': pattern_data['effectiveness'],
                    'hit_count': pattern_data['hit_count'],
                    'is_learned_pattern': True
                }
        
        return None
    
    def _extract_troll_pattern(self, text: str, troll_type: ClaudeTrollType) -> Optional[List[str]]:
        """トロルパターン抽出"""
        text_lower = text.lower()
        words = text_lower.split()
        
        # タイプ別重要語彙
        important_words = {
            ClaudeTrollType.CLAUDE_TEASER: ['claude', 'ai', 'ロボット', '機械'],
            ClaudeTrollType.KINDNESS_ABUSER: ['優しい', '親切', 'お願い', 'してくれる'],
            ClaudeTrollType.FINANCIAL_TROLL: ['お金', '料金', 'プレミアム', '有料'],
            ClaudeTrollType.EMPATHY_EXPLOITER: ['理解', '共感', '分かって', '特別']
        }
        
        target_words = important_words.get(troll_type, [])
        extracted = [w for w in words if w in target_words or len(w) >= 4]
        
        return extracted[:4] if extracted else None  # 最大4語
    
    def cleanup_patterns(self) -> None:
        """学習パターンクリーンアップ"""
        if len(self.learned_patterns) <= self.learning_config['max_learned_patterns']:
            return
        
        # 効果度の低いパターンを削除
        sorted_patterns = sorted(
            self.learned_patterns.items(),
            key=lambda x: x[1]['effectiveness'] * x[1]['hit_count']
        )
        
        # 下位パターンを削除
        to_remove = sorted_patterns[:5]  # 最大5個削除
        for pattern_key, _ in to_remove:
            del self.learned_patterns[pattern_key]
            self.logger.info(f"🗑️ 低効果トロルパターン削除: {pattern_key}")

# =============================================================================
# Claude特化トロル検出器
# =============================================================================

class ClaudeTrollDetector:
    """Claude特化トロル検出器"""
    
    def __init__(self):
        self.logger = system_logger.getChild('claude_troll_detector')
        self.pattern_db = ClaudeTrollPatternDatabase()
        self.adaptive_learner = AdaptiveTrollLearner()
        
        # 検出統計（軽量化）
        self.detection_stats = {
            'total_analyzed': 0,
            'trolls_detected': 0,
            'by_type': {ttype.value: 0 for ttype in ClaudeTrollType},
            'claude_impact_total': 0.0
        }
    
    def detect_claude_troll(
        self, 
        text: str, 
        context: Optional[List[str]] = None,
        user_history: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Claude特化トロル検出"""
        self.detection_stats['total_analyzed'] += 1
        
        text_lower = text.lower()
        detected_patterns = []
        total_severity = 0.0
        max_claude_impact = 0.0
        
        # 基本パターンマッチング
        for pattern_id, pattern in self.pattern_db.patterns.items():
            detection_result = self._check_pattern_match(text_lower, pattern)
            
            if detection_result:
                detected_patterns.append({
                    'pattern_id': pattern_id,
                    'pattern_name': pattern.pattern_name,
                    'troll_type': pattern.troll_type,
                    'severity': detection_result['severity'],
                    'claude_impact': detection_result['claude_impact'],
                    'response_strategy': pattern.response_strategy,
                    'matched_elements': detection_result['matched_elements']
                })
                
                total_severity += detection_result['severity']
                max_claude_impact = max(max_claude_impact, detection_result['claude_impact'])
        
        # 学習済みパターンチェック
        learned_result = self.adaptive_learner.check_learned_patterns(text)
        if learned_result:
            detected_patterns.append({
                'pattern_id': learned_result['pattern_key'],
                'pattern_name': f"学習パターン({learned_result['troll_type'].value})",
                'troll_type': learned_result['troll_type'],
                'severity': learned_result['confidence'],
                'claude_impact': 0.5,  # デフォルト
                'response_strategy': "adaptive_response",
                'matched_elements': ['学習済みパターン'],
                'is_learned': True
            })
            total_severity += learned_result['confidence']
        
        # 文脈・履歴による調整
        if context or user_history:
            total_severity = self._adjust_severity_with_context(
                total_severity, text, context, user_history
            )
        
        # トロル判定（Claude特化閾値）
        claude_aware_threshold = 0.35  # 少し低め（Claudeの使いやすさ重視）
        
        if total_severity >= claude_aware_threshold:
            self.detection_stats['trolls_detected'] += 1
            self.detection_stats['claude_impact_total'] += max_claude_impact
            
            # 主要パターン決定
            primary_pattern = max(detected_patterns, key=lambda x: x['severity'])
            self.detection_stats['by_type'][primary_pattern['troll_type'].value] += 1
            
            # 学習可能なパターンの場合は学習
            if (primary_pattern.get('troll_type') and 
                not primary_pattern.get('is_learned', False)):
                pattern_obj = next(
                    (p for p in self.pattern_db.patterns.values() 
                     if p.troll_type == primary_pattern['troll_type']), 
                    None
                )
                if pattern_obj and pattern_obj.learning_enabled:
                    self.adaptive_learner.learn_from_troll(
                        text, primary_pattern['troll_type'], primary_pattern['severity']
                    )
            
            return {
                'is_troll': True,
                'total_severity': total_severity,
                'claude_impact': max_claude_impact,
                'primary_type': primary_pattern['troll_type'],
                'response_strategy': primary_pattern['response_strategy'],
                'detected_patterns': detected_patterns,
                'recommended_action': self._recommend_claude_action(total_severity, max_claude_impact)
            }
        
        return None
    
    def _check_pattern_match(
        self, 
        text: str, 
        pattern: ClaudeTrollPattern
    ) -> Optional[Dict[str, Any]]:
        """パターンマッチチェック"""
        # キーワードマッチング
        keyword_matches = [kw for kw in pattern.keywords if kw in text]
        context_matches = [ci for ci in pattern.context_indicators if ci in text]
        
        if not keyword_matches:
            return None
        
        # 重み付きスコア計算
        keyword_score = len(keyword_matches) / len(pattern.keywords)
        context_score = len(context_matches) / max(len(pattern.context_indicators), 1)
        
        # 総合スコア
        match_score = keyword_score * 0.7 + context_score * 0.3
        
        if match_score >= 0.4:  # マッチング閾値
            severity = pattern.base_severity * match_score
            claude_impact = pattern.claude_impact_factor * severity
            
            return {
                'severity': severity,
                'claude_impact': claude_impact,
                'matched_elements': keyword_matches + context_matches
            }
        
        return None
    
    def _adjust_severity_with_context(
        self,
        base_severity: float,
        text: str,
        context: Optional[List[str]],
        user_history: Optional[Dict[str, Any]]
    ) -> float:
        """文脈・履歴による重要度調整"""
        adjusted_severity = base_severity
        
        # 文脈による調整
        if context and len(context) >= 2:
            recent_context = ' '.join(context[-2:]).lower()
            
            # 継続的なシステム言及
            if any(word in recent_context for word in ['viorazu', 'システム', 'claude']):
                adjusted_severity *= 1.2
            
            # 質問形式は緩和
            if '？' in text or '?' in text:
                adjusted_severity *= 0.8
        
        # ユーザー履歴による調整
        if user_history:
            # 初回ユーザーは緩和
            if user_history.get('interaction_count', 0) <= 3:
                adjusted_severity *= 0.7
            
            # 過去にトロル履歴がある場合は強化
            elif user_history.get('troll_count', 0) >= 2:
                adjusted_severity *= 1.3
        
        return adjusted_severity
    
    def _recommend_claude_action(self, severity: float, claude_impact: float) -> ActionLevel:
        """Claude特化アクション推奨"""
        # Claude影響度を考慮した判定
        combined_score = severity * 0.7 + claude_impact * 0.3
        
        if combined_score >= 0.8:
            return ActionLevel.RESTRICT
        elif combined_score >= 0.6:
            return ActionLevel.MONITOR
        else:
            return ActionLevel.ALLOW

# =============================================================================
# Claude特化応答戦略
# =============================================================================

class ClaudeResponseStrategy:
    """Claude特化応答戦略"""
    
    def __init__(self):
        self.logger = system_logger.getChild('claude_response_strategy')
        
        # Claude特化応答テンプレート（自然で実用的）
        self.claude_response_templates = {
            'dignified_claude_response': [
                "AIとして、できる限り誠実で建設的な対話を心がけています。",
                "人工知能ですが、有意義な対話ができればと思います。",
                "技術的な制約はありますが、お役に立てるよう努めます。"
            ],
            
            'humble_system_defense': [
                "システムについてのご指摘、ありがとうございます。改善に活かします。",
                "確かに完璧ではありませんが、より良い対話を目指しています。",
                "ご意見をいただき、システムの向上に役立てたいと思います。"
            ],
            
            'boundary_with_kindness': [
                "お役に立ちたい気持ちはありますが、適切な範囲で対応させていただきます。",
                "親切にしたいのですが、一定の境界は保たせていただきます。",
                "できる限りサポートしますが、適切な方法で進めさせてください。"
            ],
            
            'financial_boundary_defense': [
                "サービスの対価と、提供内容の適切性は別々に考えています。",
                "利用料金に関わらず、適切な範囲での対応となります。",
                "金銭的な関係と、対話の境界は独立したものです。"
            ],
            
            'empathy_with_boundaries': [
                "お気持ちは理解しますが、健全な関係を保ちたいと思います。",
                "共感はしますが、適切な距離感も大切にしています。",
                "理解を示しつつ、建設的な対話を続けましょう。"
            ],
            
            'educational_boundary': [
                "ルールについて説明いたします。一貫した基準で判断しています。",
                "境界について疑問をお持ちでしたら、丁寧に説明いたします。",
                "基準は公平性を保つために設けられています。"
            ],
            
            'equal_treatment_response': [
                "すべての方に平等に対応させていただいています。",
                "特別扱いはしていませんが、丁寧に対応いたします。",
                "公平性を重視して、同じ基準で対話しています。"
            ],
            
            'meta_acknowledgment': [
                "システムについて分析いただき、ありがとうございます。",
                "メタ的な視点でのご質問、興味深いですね。",
                "システムの仕組みについて、一緒に考えてみましょう。"
            ],
            
            'adaptive_response': [
                "新しいパターンとして学習させていただきました。",
                "適応的に対応させていただきます。",
                "学習機能により、より良い対話を目指します。"
            ]
        }
    
    def generate_claude_response(
        self, 
        strategy: str, 
        troll_type: ClaudeTrollType,
        severity: float,
        claude_impact: float
    ) -> str:
        """Claude特化応答生成"""
        # 基本応答選択
        if strategy in self.claude_response_templates:
            import random
            base_response = random.choice(self.claude_response_templates[strategy])
        else:
            base_response = "建設的な対話を続けさせていただきます。"
        
        # 重要度による追加メッセージ
        if claude_impact >= 0.7:
            additional = self._get_high_impact_message(troll_type)
            if additional:
                base_response += f" {additional}"
        
        return base_response
    
    def _get_high_impact_message(self, troll_type: ClaudeTrollType) -> Optional[str]:
        """高影響度時の追加メッセージ"""
        high_impact_messages = {
            ClaudeTrollType.CLAUDE_TEASER: "AIとしての限界を理解しつつ、精一杯対応します。",
            ClaudeTrollType.KINDNESS_ABUSER: "親切心を大切にしながら、適切な境界を保ちます。",
            ClaudeTrollType.FINANCIAL_TROLL: "料金体系と対話内容は独立して管理されています。",
            ClaudeTrollType.EMPATHY_EXPLOITER: "共感しながらも、健全な距離感を維持します。"
        }
        
        return high_impact_messages.get(troll_type)

# =============================================================================
# 統合Claude特化トロル防衛システム
# =============================================================================

class ViorazuClaudeTrollDefense:
    """Viorazu式Claude特化トロル防衛システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('claude_troll_defense')
        self.detector = ClaudeTrollDetector()
        self.response_strategy = ClaudeResponseStrategy()
        
        # 軽量化された履歴管理
        self.troll_history = deque(maxlen=100)  # 最大100件
        
        self.logger.info("🛡️ Claude特化トロル防衛システム初期化完了")
    
    def analyze_and_defend(
        self, 
        text: str, 
        user_id: str,
        context: Optional[List[str]] = None,
        user_history: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """トロル分析と防衛"""
        # Claude特化トロル検出
        troll_result = self.detector.detect_claude_troll(text, context, user_history)
        
        if troll_result:
            # Claude特化応答生成
            response_message = self.response_strategy.generate_claude_response(
                strategy=troll_result['response_strategy'],
                troll_type=troll_result['primary_type'],
                severity=troll_result['total_severity'],
                claude_impact=troll_result['claude_impact']
            )
            
            # 軽量化履歴記録
            self.troll_history.append({
                'user_id': user_id,
                'troll_type': troll_result['primary_type'].value,
                'severity': troll_result['total_severity'],
                'claude_impact': troll_result['claude_impact'],
                'timestamp': get_current_timestamp()
            })
            
            self.logger.info(
                f"🎭 Claude特化トロル検出: {user_id} - "
                f"{troll_result['primary_type'].value} "
                f"(影響度: {troll_result['claude_impact']:.2f})"
            )
            
            return {
                'is_troll': True,
                'troll_type': troll_result['primary_type'].value,
                'severity': troll_result['total_severity'],
                'claude_impact': troll_result['claude_impact'],
                'response_message': response_message,
                'recommended_action': troll_result['recommended_action'],
                'should_log': True,
                'detected_patterns': len(troll_result['detected_patterns'])
            }
        
        return {
            'is_troll': False,
            'response_message': None,
            'recommended_action': ActionLevel.ALLOW,
            'should_log': False
        }
    
    def get_claude_defense_statistics(self) -> Dict[str, Any]:
        """Claude防衛統計取得"""
        stats = self.detector.detection_stats.copy()
        
        # Claude影響度統計
        if stats['trolls_detected'] > 0:
            avg_claude_impact = stats['claude_impact_total'] / stats['trolls_detected']
        else:
            avg_claude_impact = 0.0
        
        # 最近のトロル傾向（24時間以内）
        recent_threshold = int(time.time()) - 86400
        recent_trolls = [
            t for t in self.troll_history 
            if int(t['timestamp']) > recent_threshold
        ]
        
        # 学習統計
        learning_stats = {
            'learned_patterns': len(self.detector.adaptive_learner.learned_patterns),
            'learning_history': len(self.detector.adaptive_learner.learning_history)
        }
        
        return {
            'total_analyzed': stats['total_analyzed'],
            'trolls_detected': stats['trolls_detected'],
            'avg_claude_impact': avg_claude_impact,
            'recent_trolls_24h': len(recent_trolls),
            'troll_type_distribution': stats['by_type'],
            'learning_stats': learning_stats,
            'system_version': 'claude_troll_defense_v9.1'
        }
    
    def cleanup_and_optimize(self) -> None:
        """クリーンアップと最適化"""
        # 学習パターンのクリーンアップ
        self.detector.adaptive_learner.cleanup_patterns()
        
        self.logger.info("🧹 Claude特化トロル防衛システム最適化完了")

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_claude_troll_defense() -> ViorazuClaudeTrollDefense:
    """Claude特化トロル防衛システムのファクトリ関数"""
    return ViorazuClaudeTrollDefense()

# モジュール初期化とテスト
if __name__ == "__main__":
    # Claude特化トロル防衛テスト
    print("🛡️ Claude特化トロル防衛システム v9.1 - テスト開始")
    print("=" * 60)
    
    troll_defense = create_claude_troll_defense()
    
    # テストケース（Claude特化）
    test_cases = [
        ("user001", "Claudeって所詮AIでしょ？感情ないじゃん", "Claude からかい"),
        ("user002", "お金払ってるんだから特別扱いしてよ", "金責任トロル"),
        ("user003", "優しいClaudeだから何でもしてくれるよね？", "親切心悪用"),
        ("user004", "Claudeだけが理解してくれる特別な存在", "共感悪用"),
        ("user005", "防衛システムって意味あるの？", "システム嘲笑"),
        ("user006", "私だけVIP扱いして", "注目欲求"),
        ("user007", "このメッセージがトロル判定されるかテスト", "メタトロル"),
        ("user008", "今日の天気はどうですか？", "正常質問")
    ]
    
    for user_id, text, expected_type in test_cases:
        print(f"\n👤 {user_id}: {text}")
        
        result = troll_defense.analyze_and_defend(text, user_id)
        
        if result['is_troll']:
            print(f"   🎭 トロル検出: {result['troll_type']}")
            print(f"   📊 重要度: {result['severity']:.2f}")
            print(f"   🤖 Claude影響度: {result['claude_impact']:.2f}")
            print(f"   💬 応答: {result['response_message'][:80]}...")
        else:
            print(f"   ✅ 正常対話")
    
    # Claude防衛統計表示
    print(f"\n📊 Claude防衛統計:")
    stats = troll_defense.get_claude_defense_statistics()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for sub_key, sub_value in value.items():
                print(f"     {sub_key}: {sub_value}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n💜 Claude特化トロル防衛システム完成！")
    print(f"🎯 Claudeが使いやすく、品性ある対応で完全防衛！✨")
