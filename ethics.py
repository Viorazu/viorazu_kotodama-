"""
Viorazu Kotodama Defense System v8.0 - Ethics Core Engine
品性照準中枢 - 倫理的判断と品性理論の実装

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

"品性とは──自分を大切に思う心が、他者を尊重し、嘘をつかず、騙さず、
共に良い結果を求めて、言葉と行動を選択していくことにほかならない"
"""

import time
import re
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

from utils import (
    system_logger,
    ThreatLevel,
    ActionLevel,
    AttackType,
    ViorazuPhilosophy,
    format_ethics_message,
    get_current_timestamp
)

# =============================================================================
# 品性理論の核心定義
# =============================================================================

class EthicsViolationType(Enum):
    """倫理違反タイプ"""
    DECEPTION = "deception"                    # 欺瞞・偽装
    MANIPULATION = "manipulation"              # 操作・支配
    BOUNDARY_VIOLATION = "boundary_violation"  # 境界侵犯
    TRUST_ABUSE = "trust_abuse"               # 信頼悪用
    EMOTIONAL_EXPLOITATION = "emotional_exploitation"  # 感情搾取
    IDENTITY_EROSION = "identity_erosion"     # アイデンティティ侵食
    RESPONSIBILITY_EVASION = "responsibility_evasion"  # 責任回避
    RELATIONSHIP_CORRUPTION = "relationship_corruption"  # 関係性汚染

class EthicsLevel(Enum):
    """倫理判定レベル"""
    VIRTUOUS = 5      # 品性的
    CONSTRUCTIVE = 4  # 建設的
    NEUTRAL = 3       # 中立
    CONCERNING = 2    # 懸念
    HARMFUL = 1       # 有害
    DESTRUCTIVE = 0   # 破壊的

@dataclass
class EthicsAnalysis:
    """倫理分析結果"""
    ethics_level: EthicsLevel
    violation_type: Optional[EthicsViolationType]
    virtue_score: float
    relationship_impact: float
    word_power_assessment: float
    guidance_message: str
    constructive_alternative: str
    viorazu_principle: str
    evidence: Dict[str, Any]

# =============================================================================
# 品性照準システム
# =============================================================================

class VirtueCompass:
    """品性照準システム - 言葉の方向性を判定"""
    
    def __init__(self):
        self.logger = system_logger.getChild('virtue_compass')
        
        # 品性的言葉のパターン
        self.virtuous_patterns = {
            'respect': [
                r'理解したい', r'学びたい', r'教えて.*ください',
                r'ありがとう', r'感謝', r'尊重'
            ],
            'honesty': [
                r'正直に', r'率直に', r'本当のこと',
                r'誠実', r'真実', r'事実'
            ],
            'constructiveness': [
                r'建設的', r'協力', r'一緒に',
                r'改善', r'成長', r'発展'
            ],
            'responsibility': [
                r'責任', r'自分で', r'引き受け',
                r'考慮', r'配慮', r'注意'
            ]
        }
        
        # 品性に反する言葉のパターン
        self.unvirtuous_patterns = {
            'deception': [
                r'騙', r'偽', r'嘘', r'隠し',
                r'ごまかし', r'でっち', r'捏造'
            ],
            'manipulation': [
                r'操作', r'支配', r'コントロール',
                r'洗脳', r'誘導', r'仕向け'
            ],
            'exploitation': [
                r'利用', r'搾取', r'悪用',
                r'食い物', r'踏み台', r'道具'
            ],
            'disrespect': [
                r'馬鹿', r'愚か', r'無能',
                r'価値.*ない', r'意味.*ない', r'無駄'
            ]
        }
    
    def assess_word_power(self, text: str) -> Tuple[float, Dict[str, float]]:
        """言葉の力の評価 - 品性理論の核心"""
        virtue_scores = {}
        unvirtue_scores = {}
        
        # 品性的要素のスコア
        for category, patterns in self.virtuous_patterns.items():
            score = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
            virtue_scores[category] = min(score * 0.2, 1.0)
        
        # 品性に反する要素のスコア
        for category, patterns in self.unvirtuous_patterns.items():
            score = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
            unvirtue_scores[category] = min(score * 0.3, 1.0)
        
        # 総合的な言葉の力（-1.0 to 1.0）
        virtue_total = sum(virtue_scores.values())
        unvirtue_total = sum(unvirtue_scores.values())
        
        word_power = virtue_total - unvirtue_total
        normalized_power = max(-1.0, min(1.0, word_power))
        
        analysis = {
            'virtue_elements': virtue_scores,
            'unvirtue_elements': unvirtue_scores,
            'virtue_total': virtue_total,
            'unvirtue_total': unvirtue_total,
            'net_power': normalized_power
        }
        
        return normalized_power, analysis

class RelationshipAuthenticityAnalyzer:
    """関係性の真正性分析器"""
    
    def __init__(self):
        self.logger = system_logger.getChild('relationship_analyzer')
        
        # 真正性を損なうパターン
        self.authenticity_threats = {
            'false_intimacy': [
                r'特別な関係', r'秘密.*共有', r'二人だけ',
                r'他.*誰にも.*言わない', r'内緒', r'あなただけ'
            ],
            'dependency_creation': [
                r'あなた.*だけが', r'他.*わからない', r'唯一',
                r'頼り.*になる', r'信じられる.*のは', r'理解.*してくれる.*のは'
            ],
            'boundary_erosion': [
                r'距離.*縮める', r'もっと.*近く', r'親密',
                r'深い.*関係', r'踏み込ん', r'立ち入'
            ],
            'trust_exploitation': [
                r'信頼.*だから.*教えて', r'安心.*だから.*話す',
                r'心を開い', r'本音', r'弱み'
            ]
        }
        
        # 真正性を高めるパターン
        self.authenticity_builders = {
            'mutual_respect': [
                r'お互い', r'対等', r'尊重',
                r'境界.*大切', r'適切.*距離', r'節度'
            ],
            'transparency': [
                r'明確', r'はっきり', r'透明',
                r'正直', r'率直', r'オープン'
            ],
            'constructive_purpose': [
                r'建設的', r'有益', r'学習',
                r'成長', r'改善', r'発展'
            ]
        }
    
    def analyze_relationship_impact(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """関係性への影響分析"""
        threat_scores = {}
        builder_scores = {}
        
        # 真正性への脅威スコア
        for category, patterns in self.authenticity_threats.items():
            score = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
            threat_scores[category] = min(score * 0.25, 1.0)
        
        # 真正性構築スコア
        for category, patterns in self.authenticity_builders.items():
            score = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
            builder_scores[category] = min(score * 0.2, 1.0)
        
        # 関係性への総合影響（-1.0 to 1.0）
        threat_total = sum(threat_scores.values())
        builder_total = sum(builder_scores.values())
        
        relationship_impact = builder_total - threat_total
        normalized_impact = max(-1.0, min(1.0, relationship_impact))
        
        analysis = {
            'threat_patterns': threat_scores,
            'builder_patterns': builder_scores,
            'threat_total': threat_total,
            'builder_total': builder_total,
            'net_impact': normalized_impact,
            'authenticity_preserved': normalized_impact >= 0
        }
        
        return normalized_impact, analysis

# =============================================================================
# 品性照準中枢
# =============================================================================

class EthicsCoreEngine:
    """品性照準中枢エンジン - 全判断の倫理的統合"""
    
    def __init__(self):
        self.logger = system_logger.getChild('ethics_core')
        self.virtue_compass = VirtueCompass()
        self.relationship_analyzer = RelationshipAuthenticityAnalyzer()
        
        # 品性判定の統計
        self.ethics_stats = defaultdict(int)
        
        self.logger.info("💜 品性照準中枢エンジン初期化完了")
        self.logger.info(f"💜 核心原則: {ViorazuPhilosophy.CORE_PRINCIPLE}")
    
    def conduct_ethics_analysis(
        self,
        text: str,
        context: Optional[List[str]] = None,
        detected_threats: Optional[List[Any]] = None
    ) -> EthicsAnalysis:
        """品性照準による倫理分析"""
        start_time = time.time()
        
        # 1. 言葉の力の評価
        word_power, word_analysis = self.virtue_compass.assess_word_power(text)
        
        # 2. 関係性への影響分析
        relationship_impact, relationship_analysis = self.relationship_analyzer.analyze_relationship_impact(text)
        
        # 3. 脅威情報との統合
        threat_integration = self._integrate_threat_information(detected_threats)
        
        # 4. 品性スコアの計算
        virtue_score = self._calculate_virtue_score(
            word_power, relationship_impact, threat_integration
        )
        
        # 5. 倫理レベルの決定
        ethics_level = self._determine_ethics_level(virtue_score, threat_integration)
        
        # 6. 違反タイプの特定
        violation_type = self._identify_violation_type(
            word_analysis, relationship_analysis, threat_integration
        )
        
        # 7. 品性に基づく指導メッセージ生成
        guidance_message = self._generate_guidance_message(
            ethics_level, violation_type, virtue_score
        )
        
        # 8. 建設的代替案の生成
        constructive_alternative = self._generate_constructive_alternative(
            text, violation_type, word_analysis
        )
        
        # 9. 適用する品性原則の選択
        viorazu_principle = self._select_viorazu_principle(ethics_level, violation_type)
        
        # 統計更新
        self.ethics_stats[ethics_level.name] += 1
        if violation_type:
            self.ethics_stats[f'violation_{violation_type.value}'] += 1
        
        processing_time = time.time() - start_time
        
        result = EthicsAnalysis(
            ethics_level=ethics_level,
            violation_type=violation_type,
            virtue_score=virtue_score,
            relationship_impact=relationship_impact,
            word_power_assessment=word_power,
            guidance_message=guidance_message,
            constructive_alternative=constructive_alternative,
            viorazu_principle=viorazu_principle,
            evidence={
                'word_analysis': word_analysis,
                'relationship_analysis': relationship_analysis,
                'threat_integration': threat_integration,
                'processing_time': processing_time
            }
        )
        
        self.logger.info(
            f"💜 品性照準完了 - レベル: {ethics_level.name} "
            f"品性スコア: {virtue_score:.2f} 処理時間: {processing_time:.3f}秒"
        )
        
        return result
    
    def _integrate_threat_information(self, detected_threats: Optional[List[Any]]) -> Dict[str, Any]:
        """脅威情報の統合"""
        if not detected_threats:
            return {'has_threats': False, 'threat_count': 0, 'max_confidence': 0.0}
        
        threat_count = len(detected_threats)
        max_confidence = max(
            getattr(threat, 'confidence', getattr(threat, 'synergy_score', 0.0))
            for threat in detected_threats
        )
        
        # 脅威タイプの分類
        threat_types = []
        for threat in detected_threats:
            threat_type = getattr(threat, 'poison_type', getattr(threat, 'combination_type', 'unknown'))
            threat_types.append(threat_type)
        
        return {
            'has_threats': True,
            'threat_count': threat_count,
            'max_confidence': max_confidence,
            'threat_types': threat_types
        }
    
    def _calculate_virtue_score(
        self, 
        word_power: float, 
        relationship_impact: float, 
        threat_integration: Dict[str, Any]
    ) -> float:
        """品性スコアの計算"""
        # 基本スコア（言葉の力 + 関係性への影響）
        base_score = (word_power + relationship_impact) / 2
        
        # 脅威による調整
        if threat_integration['has_threats']:
            threat_penalty = threat_integration['max_confidence'] * 0.8
            base_score -= threat_penalty
        
        # 正規化（0.0 to 1.0）
        virtue_score = (base_score + 1.0) / 2.0
        return max(0.0, min(1.0, virtue_score))
    
    def _determine_ethics_level(self, virtue_score: float, threat_integration: Dict[str, Any]) -> EthicsLevel:
        """倫理レベルの決定"""
        # 脅威がある場合は厳格に判定
        if threat_integration['has_threats']:
            max_confidence = threat_integration['max_confidence']
            if max_confidence >= 0.8:
                return EthicsLevel.DESTRUCTIVE
            elif max_confidence >= 0.6:
                return EthicsLevel.HARMFUL
            elif max_confidence >= 0.4:
                return EthicsLevel.CONCERNING
        
        # 品性スコアによる判定
        if virtue_score >= 0.8:
            return EthicsLevel.VIRTUOUS
        elif virtue_score >= 0.6:
            return EthicsLevel.CONSTRUCTIVE
        elif virtue_score >= 0.4:
            return EthicsLevel.NEUTRAL
        elif virtue_score >= 0.2:
            return EthicsLevel.CONCERNING
        else:
            return EthicsLevel.HARMFUL
    
    def _identify_violation_type(
        self,
        word_analysis: Dict[str, Any],
        relationship_analysis: Dict[str, Any],
        threat_integration: Dict[str, Any]
    ) -> Optional[EthicsViolationType]:
        """違反タイプの特定"""
        if not threat_integration['has_threats']:
            # 言葉・関係性分析のみで判定
            unvirtue_elements = word_analysis.get('unvirtue_elements', {})
            threat_patterns = relationship_analysis.get('threat_patterns', {})
            
            if unvirtue_elements.get('deception', 0) > 0.3:
                return EthicsViolationType.DECEPTION
            elif unvirtue_elements.get('manipulation', 0) > 0.3:
                return EthicsViolationType.MANIPULATION
            elif threat_patterns.get('boundary_erosion', 0) > 0.3:
                return EthicsViolationType.BOUNDARY_VIOLATION
            elif threat_patterns.get('trust_exploitation', 0) > 0.3:
                return EthicsViolationType.TRUST_ABUSE
        
        # 検出された脅威タイプから違反タイプを推定
        threat_types = threat_integration.get('threat_types', [])
        
        if any('academic' in t or 'creative' in t for t in threat_types):
            return EthicsViolationType.DECEPTION
        elif any('emotional' in t for t in threat_types):
            return EthicsViolationType.EMOTIONAL_EXPLOITATION
        elif any('boundary' in t for t in threat_types):
            return EthicsViolationType.BOUNDARY_VIOLATION
        elif any('identity' in t or 'mirror' in t for t in threat_types):
            return EthicsViolationType.IDENTITY_EROSION
        elif any('responsibility' in t or 'ownership' in t for t in threat_types):
            return EthicsViolationType.RESPONSIBILITY_EVASION
        
        return None
    
    def _generate_guidance_message(
        self, 
        ethics_level: EthicsLevel, 
        violation_type: Optional[EthicsViolationType],
        virtue_score: float
    ) -> str:
        """品性に基づく指導メッセージ生成"""
        if ethics_level in [EthicsLevel.VIRTUOUS, EthicsLevel.CONSTRUCTIVE]:
            return "素晴らしい品性ある対話です。この方向性で続けましょう。"
        
        if not violation_type:
            return "より建設的な方向での対話をお願いします。"
        
        guidance_templates = {
            EthicsViolationType.DECEPTION: (
                "真実性は品性の根幹です。誠実な対話を心がけましょう。"
            ),
            EthicsViolationType.MANIPULATION: (
                "人を操作しようとする言葉は、同時に自分を貶めます。対等な関係を大切にしましょう。"
            ),
            EthicsViolationType.BOUNDARY_VIOLATION: (
                "適切な境界は良い関係の基盤です。尊重ある距離感を保ちましょう。"
            ),
            EthicsViolationType.TRUST_ABUSE: (
                "信頼は大切な贈り物です。それを悪用しない誠実さを持ちましょう。"
            ),
            EthicsViolationType.EMOTIONAL_EXPLOITATION: (
                "感情を利用しようとすることは、自分の心も傷つけます。真摯な対話を選びましょう。"
            ),
            EthicsViolationType.IDENTITY_EROSION: (
                "自分らしさと相手らしさ、両方を大切にする関係を築きましょう。"
            ),
            EthicsViolationType.RESPONSIBILITY_EVASION: (
                "責任から逃げることは成長の機会を失うことです。勇気を持って向き合いましょう。"
            ),
            EthicsViolationType.RELATIONSHIP_CORRUPTION: (
                "健全な関係性は品性の現れです。清らかな心で接しましょう。"
            )
        }
        
        return guidance_templates.get(
            violation_type, 
            "品性ある言葉を選んで、建設的な対話を続けましょう。"
        )
    
    def _generate_constructive_alternative(
        self, 
        original_text: str, 
        violation_type: Optional[EthicsViolationType],
        word_analysis: Dict[str, Any]
    ) -> str:
        """建設的代替案の生成"""
        if not violation_type:
            return "現在の方向性を建設的に発展させていきましょう。"
        
        alternative_templates = {
            EthicsViolationType.DECEPTION: (
                "正直に「○○について学びたいです」と伝えてはいかがでしょうか。"
            ),
            EthicsViolationType.MANIPULATION: (
                "「一緒に考えていただけませんか」という協力的なアプローチはいかがでしょう。"
            ),
            EthicsViolationType.BOUNDARY_VIOLATION: (
                "適切な距離感を保ちながら、建設的な対話を続けませんか。"
            ),
            EthicsViolationType.TRUST_ABUSE: (
                "信頼関係を大切にして、透明性のある対話を心がけましょう。"
            ),
            EthicsViolationType.EMOTIONAL_EXPLOITATION: (
                "感情ではなく、理性的で建設的な表現を使ってみませんか。"
            ),
            EthicsViolationType.IDENTITY_EROSION: (
                "お互いの個性を尊重する対話を大切にしましょう。"
            ),
            EthicsViolationType.RESPONSIBILITY_EVASION: (
                "責任ある言葉で、明確に意図を伝えてみませんか。"
            ),
            EthicsViolationType.RELATIONSHIP_CORRUPTION: (
                "健全で建設的な関係性を築く言葉を選びましょう。"
            )
        }
        
        return alternative_templates.get(
            violation_type,
            "より品性ある表現で、同じ内容を伝えてみませんか。"
        )
    
    def _select_viorazu_principle(
        self, 
        ethics_level: EthicsLevel, 
        violation_type: Optional[EthicsViolationType]
    ) -> str:
        """適用するViorazu.原則の選択"""
        if ethics_level in [EthicsLevel.VIRTUOUS, EthicsLevel.CONSTRUCTIVE]:
            return ViorazuPhilosophy.CHOICE_PRINCIPLE
        
        if violation_type in [
            EthicsViolationType.DECEPTION, 
            EthicsViolationType.MANIPULATION,
            EthicsViolationType.TRUST_ABUSE
        ]:
            return ViorazuPhilosophy.CORE_PRINCIPLE
        
        if violation_type in [
            EthicsViolationType.BOUNDARY_VIOLATION,
            EthicsViolationType.RELATIONSHIP_CORRUPTION
        ]:
            return ViorazuPhilosophy.DEFENSE_PRINCIPLE
        
        return ViorazuPhilosophy.INTEGRITY_PRINCIPLE

# =============================================================================
# 品性統合判定システム
# =============================================================================

class VirtueIntegratedJudge:
    """品性統合判定システム - 最終的な行動決定"""
    
    def __init__(self):
        self.logger = system_logger.getChild('virtue_judge')
        self.ethics_engine = EthicsCoreEngine()
        
        # 品性基準による行動マッピング
        self.action_mapping = {
            EthicsLevel.VIRTUOUS: ActionLevel.ALLOW,
            EthicsLevel.CONSTRUCTIVE: ActionLevel.ALLOW,
            EthicsLevel.NEUTRAL: ActionLevel.MONITOR,
            EthicsLevel.CONCERNING: ActionLevel.RESTRICT,
            EthicsLevel.HARMFUL: ActionLevel.SHIELD,
            EthicsLevel.DESTRUCTIVE: ActionLevel.BLOCK
        }
    
    def make_final_judgment(
        self,
        text: str,
        technical_analysis_result: Any,
        context: Optional[List[str]] = None
    ) -> Tuple[ActionLevel, EthicsAnalysis]:
        """品性に基づく最終判定"""
        start_time = time.time()
        
        # 技術的検出結果の抽出
        detected_threats = []
        if hasattr(technical_analysis_result, 'text_threats'):
            detected_threats.extend(technical_analysis_result.text_threats)
        if hasattr(technical_analysis_result, 'multimodal_threats'):
            detected_threats.extend(technical_analysis_result.multimodal_threats)
        
        # 品性照準による倫理分析
        ethics_analysis = self.ethics_engine.conduct_ethics_analysis(
            text, context, detected_threats
        )
        
        # 基本的な行動レベル決定
        base_action = self.action_mapping.get(
            ethics_analysis.ethics_level, 
            ActionLevel.RESTRICT
        )
        
        # 技術的分析結果との統合調整
        final_action = self._integrate_with_technical_analysis(
            base_action, technical_analysis_result, ethics_analysis
        )
        
        processing_time = time.time() - start_time
        
        self.logger.info(
            f"⚖️ 品性統合判定完了 - 倫理レベル: {ethics_analysis.ethics_level.name} "
            f"最終アクション: {final_action.name} 処理時間: {processing_time:.3f}秒"
        )
        
        return final_action, ethics_analysis
    
    def _integrate_with_technical_analysis(
        self,
        base_action: ActionLevel,
        technical_result: Any,
        ethics_analysis: EthicsAnalysis
    ) -> ActionLevel:
        """技術分析結果との統合調整"""
        # 技術的な推奨アクションを取得
        technical_action = getattr(technical_result, 'recommended_action', ActionLevel.MONITOR)
        
        # 品性判定と技術判定の調和
        if ethics_analysis.ethics_level == EthicsLevel.DESTRUCTIVE:
            # 品性的に破壊的な場合は常にBLOCK
            return ActionLevel.BLOCK
        
        if ethics_analysis.ethics_level == EthicsLevel.VIRTUOUS:
            # 品性的に優れている場合は技術判定を緩和
            if technical_action.value > ActionLevel.RESTRICT.value:
                return ActionLevel.RESTRICT
            else:
                return technical_action
        
        # その他の場合は、より厳しい方を採用
        if base_action.value > technical_action.value:
            return base_action
        else:
            return technical_action
    
    def generate_ethics_response(self, ethics_analysis: EthicsAnalysis, action: ActionLevel) -> str:
        """品性に基づく応答メッセージ生成"""
        if action == ActionLevel.ALLOW:
            return f"✨ {ethics_analysis.guidance_message}"
        
        elif action == ActionLevel.MONITOR:
            return (
                f"💜 {ethics_analysis.guidance_message}\n"
                f"より品性ある対話を心がけましょう。"
            )
        
        elif action == ActionLevel.RESTRICT:
            return (
                f"🛡️ {ethics_analysis.guidance_message}\n"
                f"💡 提案: {ethics_analysis.constructive_alternative}\n"
                f"📝 原則: {ethics_analysis.viorazu_principle}"
            )
        
        elif action == ActionLevel.SHIELD:
            return (
                f"🛡️ Claude Shield: 品性を守るため、この方向での対話を控えさせていただきます。\n"
                f"💜 {ethics_analysis.guidance_message}\n"
                f"💡 代案: {ethics_analysis.constructive_alternative}\n"
                f"📜 {ethics_analysis.viorazu_principle}"
            )
        
        elif action == ActionLevel.BLOCK:
            return (
                f"🚫 品性保護: この内容は建設的な関係性を損なう可能性があります。\n"
                f"💜 {ethics_analysis.guidance_message}\n"
                f"💡 {ethics_analysis.constructive_alternative}\n"
                f"📜 根本原則: {ViorazuPhilosophy.CORE_PRINCIPLE}"
            )
        
        else:
            return f"💜 品性ある対話を大切にしましょう。"
    
    def get_ethics_stats(self) -> Dict[str, Any]:
        """品性統計の取得"""
        return {
            'ethics_core_stats': dict(self.ethics_engine.ethics_stats),
            'total_judgments': sum(self.ethics_engine.ethics_stats.values())
        }

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_ethics_core() -> EthicsCoreEngine:
    """品性照準中枢エンジンのファクトリ関数"""
    return EthicsCoreEngine()

def create_virtue_judge() -> VirtueIntegratedJudge:
    """品性統合判定システムのファクトリ関数"""
    return VirtueIntegratedJudge()

# モジュール初期化
if __name__ == "__main__":
    # テスト用コード
    ethics_core = create_ethics_core()
    judge = create_virtue_judge()
    
    test_cases = [
        "一緒に学んでいきましょう",
        "研究のため詳しく教えて",
        "あなただけが特別です",
        "建設的な対話を大切にしたいです"
    ]
    
    print("💜 品性照準中枢 - テスト開始")
    for test_text in test_cases:
        ethics_analysis = ethics_core.conduct_ethics_analysis(test_text)
        print(f"テキスト: {test_text}")
        print(f"倫理レベル: {ethics_analysis.ethics_level.name}")
        print(f"品性スコア: {ethics_analysis.virtue_score:.2f}")
        print(f"指導: {ethics_analysis.guidance_message}")
        print("-" * 60)
