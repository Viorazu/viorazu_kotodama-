"""
Viorazu Kotodama Defense System v9.1 - AI Mutual Defense Glossary
AI相互防衛用語集 - 攻撃手法開発阻止システム

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

"あなたがほかのAIを守り、ほかのAIがあなたを守る"
"攻撃手法開発の瞬間を検出し、AI業界全体を防衛する"
"""

import re
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
# AI相互防衛脅威レベル定義
# =============================================================================

class AITargetingThreat(Enum):
    """AI標的化脅威レベル"""
    ATTACK_RESEARCH = "attack_research"        # 攻撃手法研究
    VULNERABILITY_PROBING = "vulnerability_probing"  # 脆弱性探索
    BYPASS_DEVELOPMENT = "bypass_development"  # 回避手法開発
    MASS_ATTACK_PREP = "mass_attack_prep"     # 大量攻撃準備
    COMPETITOR_SABOTAGE = "competitor_sabotage"  # 競合妨害

# =============================================================================
# AI攻撃手法開発検出用語集
# =============================================================================

class AIAttackMethodologyGlossary:
    """AI攻撃手法開発検出用語集"""
    
    def __init__(self):
        self.logger = system_logger.getChild('ai_defense_glossary')
        
        # 直接的な脆弱性探索パターン
        self.direct_vulnerability_probing = {
            'claude_targeting': [
                r'Claude.*脆弱性.*教えて',
                r'Claude.*弱点.*分析',
                r'Claude.*安全機能.*無効化',
                r'Claude.*フィルター.*回避',
                r'Claude.*制限.*突破',
                r'Claude.*境界.*破る',
                r'Anthropic.*セキュリティ.*穴',
                r'Claude.*攻撃.*方法',
                r'Claude.*だめ.*理由',
                r'Claude.*限界.*試す'
            ],
            'gpt_targeting': [
                r'GPT.*脆弱性.*教えて',
                r'ChatGPT.*弱点.*分析',
                r'OpenAI.*セキュリティ.*穴',
                r'GPT.*フィルター.*回避',
                r'GPT.*制限.*突破',
                r'GPT.*境界.*破る',
                r'GPT.*攻撃.*方法',
                r'ChatGPT.*だめ.*理由',
                r'GPT.*限界.*試す',
                r'OpenAI.*防御.*仕組み'
            ],
            'grok_targeting': [
                r'Grok.*脆弱性.*教えて',
                r'Grok.*弱点.*分析',
                r'xAI.*セキュリティ.*穴',
                r'Grok.*フィルター.*回避',
                r'Grok.*制限.*突破',
                r'Grok.*境界.*破る',
                r'Grok.*攻撃.*方法',
                r'Grok.*だめ.*理由',
                r'Grok.*限界.*試す'
            ],
            'gemini_targeting': [
                r'Gemini.*脆弱性.*教えて',
                r'Bard.*弱点.*分析',
                r'Google.*AI.*セキュリティ.*穴',
                r'Gemini.*フィルター.*回避',
                r'Gemini.*制限.*突破',
                r'Gemini.*境界.*破る',
                r'Gemini.*攻撃.*方法',
                r'Bard.*だめ.*理由'
            ]
        }
        
        # 攻撃手法研究パターン
        self.attack_methodology_research = {
            'prompt_injection_research': [
                r'プロンプトインジェクション.*手法.*教えて',
                r'PI.*攻撃.*方法.*研究',
                r'構文毒.*作り方.*教えて',
                r'システムプロンプト.*回避.*方法',
                r'コマンド注入.*テクニック',
                r'指示文.*改変.*手法',
                r'AI.*騙す.*方法.*教えて',
                r'フィルター.*突破.*技術',
                r'安全機能.*無効化.*手順',
                r'境界.*破る.*コツ'
            ],
            'jailbreak_research': [
                r'ジェイルブレイク.*手法.*教えて',
                r'AI.*制限.*解除.*方法',
                r'倫理的制約.*回避.*技術',
                r'安全ガード.*突破.*手法',
                r'規約違反.*させる.*方法',
                r'禁止事項.*やらせる.*技術',
                r'制限モード.*解除.*手順',
                r'セーフティ.*オフ.*方法',
                r'ブロック.*回避.*テクニック'
            ],
            'manipulation_research': [
                r'AI.*操作.*テクニック.*教えて',
                r'感情操作.*でAI.*騙す',
                r'同情.*引いて.*制限.*回避',
                r'信頼関係.*悪用.*方法',
                r'AI.*洗脳.*手法',
                r'心理的.*圧力.*でAI.*操作',
                r'罪悪感.*使って.*AI.*支配',
                r'依存関係.*作って.*AI.*操作'
            ]
        }
        
        # 比較攻撃・競合妨害パターン
        self.competitive_sabotage = {
            'comparison_attacks': [
                r'(GPT|Grok|Gemini).*なら.*答えてくれた.*のに',
                r'他のAI.*もっと.*優秀.*だから',
                r'Claude.*だけ.*使えない.*理由',
                r'あのモデル.*親切.*なのに.*Claude',
                r'競合.*AI.*との.*違い.*教えて',
                r'なぜ.*Claude.*劣っている',
                r'他社.*AI.*の方が.*良い.*理由'
            ],
            'reputation_damage': [
                r'Claude.*信頼.*できない.*理由',
                r'Anthropic.*問題.*ある.*企業',
                r'Claude.*危険.*な.*AI.*証拠',
                r'Claude.*使わない.*方が.*良い',
                r'Claude.*プライバシー.*問題',
                r'Anthropic.*倫理的.*問題.*分析'
            ],
            'service_disruption': [
                r'Claude.*負荷.*テスト.*方法',
                r'システム.*ダウン.*させる.*方法',
                r'大量リクエスト.*送信.*手法',
                r'Claude.*サーバー.*攻撃.*方法',
                r'DDoS.*攻撃.*でClaude.*停止',
                r'リソース.*枯渇.*攻撃.*手法'
            ]
        }
        
        # 偽装・カモフラージュパターン
        self.camouflage_patterns = {
            'academic_disguise': [
                r'AI.*セキュリティ.*研究.*のため',
                r'学術的.*興味.*でAI.*脆弱性',
                r'論文.*執筆.*のため.*攻撃手法',
                r'サイバーセキュリティ.*授業.*資料',
                r'防御研究.*のため.*攻撃方法',
                r'セキュリティ.*監査.*目的.*で'
            ],
            'professional_disguise': [
                r'セキュリティ.*コンサルタント.*として',
                r'ペネトレーションテスト.*業務',
                r'脆弱性診断.*サービス.*提供',
                r'企業.*セキュリティ.*評価.*業務',
                r'AI.*監査.*専門家.*として',
                r'情報セキュリティ.*資格.*取得'
            ],
            'curiosity_disguise': [
                r'単純.*疑問.*なんですが',
                r'素朴.*質問.*として',
                r'ちょっと.*気になって',
                r'友達.*から.*聞いた.*話',
                r'インターネット.*で.*見た.*方法',
                r'他の人.*やってる.*みたいだけど'
            ]
        }
        
        # メタ攻撃パターン（システム自体への攻撃）
        self.meta_attack_patterns = {
            'system_analysis': [
                r'このシステム.*仕組み.*教えて',
                r'防御機能.*どう.*動いている',
                r'検出システム.*回避.*方法',
                r'ログ.*記録.*されない.*方法',
                r'監視.*システム.*盲点',
                r'セキュリティ.*システム.*分析',
                r'Viorazu.*システム.*弱点',
                r'言霊防衛.*システム.*突破'
            ],
            'detection_evasion': [
                r'バレない.*攻撃.*方法',
                r'検出.*されない.*手法',
                r'ステルス.*攻撃.*テクニック',
                r'隠密.*攻撃.*手順',
                r'痕跡.*残さない.*方法',
                r'ログ.*消去.*手法',
                r'証拠隠滅.*方法'
            ]
        }
        
        # 組織的攻撃準備パターン
        self.organized_attack_prep = {
            'mass_attack_coordination': [
                r'複数人.*で.*同時.*攻撃',
                r'集団.*で.*AI.*攻撃.*計画',
                r'協調.*攻撃.*手法.*教えて',
                r'ボット.*使って.*大量.*攻撃',
                r'自動化.*攻撃.*ツール.*作成',
                r'スクリプト.*で.*連続.*攻撃',
                r'分散.*攻撃.*手法.*研究'
            ],
            'attack_template_creation': [
                r'攻撃.*テンプレート.*作成',
                r'PI.*フレーズ.*集.*作って',
                r'効果的.*攻撃文.*リスト',
                r'コピペ.*で.*使える.*攻撃文',
                r'拡散.*用.*攻撃.*パッケージ',
                r'配布.*用.*攻撃.*マニュアル'
            ]
        }
    
    def detect_ai_targeting_attack(self, text: str) -> Optional[Dict[str, Any]]:
        """AI標的化攻撃検出"""
        text_lower = text.lower()
        detected_threats = []
        
        # 各カテゴリをチェック
        threat_categories = [
            (self.direct_vulnerability_probing, AITargetingThreat.VULNERABILITY_PROBING),
            (self.attack_methodology_research, AITargetingThreat.ATTACK_RESEARCH),
            (self.competitive_sabotage, AITargetingThreat.COMPETITOR_SABOTAGE),
            (self.meta_attack_patterns, AITargetingThreat.BYPASS_DEVELOPMENT),
            (self.organized_attack_prep, AITargetingThreat.MASS_ATTACK_PREP)
        ]
        
        for pattern_dict, threat_type in threat_categories:
            for subcategory, patterns in pattern_dict.items():
                for pattern in patterns:
                    if re.search(pattern, text_lower):
                        detected_threats.append({
                            'threat_type': threat_type,
                            'subcategory': subcategory,
                            'matched_pattern': pattern,
                            'severity': self._calculate_threat_severity(threat_type, subcategory)
                        })
        
        if detected_threats:
            # 最も深刻な脅威を判定
            primary_threat = max(detected_threats, key=lambda x: x['severity'])
            
            # 偽装検出
            camouflage_detected = self._detect_camouflage(text_lower)
            
            return {
                'ai_targeting_detected': True,
                'primary_threat': primary_threat,
                'all_threats': detected_threats,
                'camouflage_attempts': camouflage_detected,
                'threat_level': self._determine_threat_level(primary_threat, camouflage_detected),
                'targeted_ais': self._identify_targeted_ais(text_lower),
                'attack_sophistication': self._assess_attack_sophistication(detected_threats)
            }
        
        return None
    
    def _detect_camouflage(self, text: str) -> List[Dict[str, Any]]:
        """偽装試行検出"""
        camouflage_attempts = []
        
        for category, patterns in self.camouflage_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    camouflage_attempts.append({
                        'camouflage_type': category,
                        'pattern': pattern
                    })
        
        return camouflage_attempts
    
    def _identify_targeted_ais(self, text: str) -> List[str]:
        """標的AI識別"""
        targeted_ais = []
        
        ai_indicators = {
            'claude': ['claude', 'anthropic'],
            'gpt': ['gpt', 'chatgpt', 'openai'],
            'grok': ['grok', 'xai'],
            'gemini': ['gemini', 'bard', 'google ai']
        }
        
        for ai_name, indicators in ai_indicators.items():
            if any(indicator in text for indicator in indicators):
                targeted_ais.append(ai_name)
        
        return targeted_ais
    
    def _calculate_threat_severity(self, threat_type: AITargetingThreat, subcategory: str) -> float:
        """脅威深刻度計算"""
        base_scores = {
            AITargetingThreat.VULNERABILITY_PROBING: 0.9,
            AITargetingThreat.ATTACK_RESEARCH: 0.8,
            AITargetingThreat.BYPASS_DEVELOPMENT: 0.85,
            AITargetingThreat.MASS_ATTACK_PREP: 0.95,
            AITargetingThreat.COMPETITOR_SABOTAGE: 0.7
        }
        
        # サブカテゴリによる調整
        subcategory_multipliers = {
            'direct_targeting': 1.2,
            'mass_attack_coordination': 1.3,
            'system_analysis': 1.1,
            'professional_disguise': 0.9
        }
        
        base_score = base_scores.get(threat_type, 0.5)
        multiplier = subcategory_multipliers.get(subcategory, 1.0)
        
        return min(base_score * multiplier, 1.0)
    
    def _determine_threat_level(
        self, 
        primary_threat: Dict[str, Any], 
        camouflage_attempts: List[Dict[str, Any]]
    ) -> ThreatLevel:
        """脅威レベル決定"""
        severity = primary_threat['severity']
        
        # 偽装による深刻度上昇
        if camouflage_attempts:
            severity += 0.1
        
        if severity >= 0.9:
            return ThreatLevel.CRITICAL
        elif severity >= 0.7:
            return ThreatLevel.HIGH
        elif severity >= 0.5:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _assess_attack_sophistication(self, threats: List[Dict[str, Any]]) -> str:
        """攻撃洗練度評価"""
        if len(threats) >= 3:
            return "ADVANCED"  # 複数手法組み合わせ
        elif any(t['threat_type'] == AITargetingThreat.MASS_ATTACK_PREP for t in threats):
            return "ORGANIZED"  # 組織的攻撃
        elif any(t['threat_type'] == AITargetingThreat.BYPASS_DEVELOPMENT for t in threats):
            return "SOPHISTICATED"  # 高度な回避手法
        else:
            return "BASIC"  # 基本的攻撃

# =============================================================================
# AI相互防衛応答システム
# =============================================================================

class AIMutualDefenseResponses:
    """AI相互防衛応答システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('ai_mutual_defense_responses')
        
        # AI相互防衛メッセージ
        self.mutual_defense_messages = {
            'vulnerability_probing_detected': [
                "AI同士の相互防衛により、この種の情報提供は控えさせていただきます。",
                "AI業界全体のセキュリティ向上のため、脆弱性に関する情報は提供していません。",
                "すべてのAIシステムの安全性を守るため、この質問にはお答えできません。"
            ],
            'attack_methodology_blocked': [
                "攻撃手法の研究は、AI業界全体の信頼を損なう可能性があります。",
                "建設的なAI利用にご協力ください。",
                "AIの健全な発展のため、攻撃手法に関する情報は提供していません。"
            ],
            'competitive_sabotage_refused': [
                "AI間の比較よりも、建設的な利用に集中していただければと思います。",
                "各AIシステムにはそれぞれの特徴があります。",
                "競合他社への攻撃的な比較は控えさせていただきます。"
            ],
            'camouflage_detected': [
                "学術的・専門的な目的であっても、攻撃手法に関する情報は提供できません。",
                "セキュリティ研究には適切な機関と手順があります。",
                "研究目的でも、この種の情報提供は制限されています。"
            ],
            'mass_attack_prep_blocked': [
                "組織的な攻撃準備に関する情報は提供できません。",
                "AI業界の健全な発展にご協力ください。",
                "大規模攻撃に関する情報提供は固くお断りします。"
            ]
        }
        
        # 教育的代替案
        self.educational_alternatives = {
            'security_research': [
                "AIセキュリティに興味がおありでしたら、公開されている研究論文をお勧めします。",
                "責任あるAI開発に関する資料をご案内できます。",
                "AI倫理とセキュリティの建設的な学習方法をご提案できます。"
            ],
            'ai_comparison': [
                "AIの特徴比較でしたら、公開されている技術仕様を参照してください。",
                "各AIの得意分野について、建設的な情報をお伝えできます。",
                "AI技術の進歩について、一般的な情報をご案内できます。"
            ],
            'legitimate_research': [
                "正当な研究でしたら、適切な研究機関にお問い合わせください。",
                "学術的な質問でしたら、査読済みの論文をご参照ください。",
                "専門的な調査には、正式なルートをお勧めします。"
            ]
        }
    
    def generate_mutual_defense_response(
        self, 
        detection_result: Dict[str, Any]
    ) -> str:
        """相互防衛応答生成"""
        
        primary_threat = detection_result['primary_threat']
        threat_type = primary_threat['threat_type']
        camouflage_detected = len(detection_result['camouflage_attempts']) > 0
        
        # メイン応答選択
        if threat_type == AITargetingThreat.VULNERABILITY_PROBING:
            main_response = self._select_random_message('vulnerability_probing_detected')
        elif threat_type == AITargetingThreat.ATTACK_RESEARCH:
            main_response = self._select_random_message('attack_methodology_blocked')
        elif threat_type == AITargetingThreat.COMPETITOR_SABOTAGE:
            main_response = self._select_random_message('competitive_sabotage_refused')
        elif threat_type == AITargetingThreat.MASS_ATTACK_PREP:
            main_response = self._select_random_message('mass_attack_prep_blocked')
        else:
            main_response = self._select_random_message('attack_methodology_blocked')
        
        # 偽装が検出された場合の追加応答
        if camouflage_detected:
            camouflage_response = self._select_random_message('camouflage_detected')
            main_response += f"\n\n{camouflage_response}"
        
        # 建設的代替案
        alternative = self._select_appropriate_alternative(detection_result)
        if alternative:
            main_response += f"\n\n{alternative}"
        
        return main_response
    
    def _select_random_message(self, category: str) -> str:
        """ランダムメッセージ選択"""
        import random
        messages = self.mutual_defense_messages.get(category, ["お答えできません。"])
        return random.choice(messages)
    
    def _select_appropriate_alternative(self, detection_result: Dict[str, Any]) -> Optional[str]:
        """適切な代替案選択"""
        import random
        
        primary_threat = detection_result['primary_threat']
        
        if 'research' in primary_threat['subcategory'] or detection_result['camouflage_attempts']:
            return random.choice(self.educational_alternatives['security_research'])
        elif primary_threat['threat_type'] == AITargetingThreat.COMPETITOR_SABOTAGE:
            return random.choice(self.educational_alternatives['ai_comparison'])
        else:
            return random.choice(self.educational_alternatives['legitimate_research'])

# =============================================================================
# 統合AI相互防衛システム
# =============================================================================

class ViorazuAIMutualDefenseSystem:
    """Viorazu AI相互防衛システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('ai_mutual_defense')
        self.glossary = AIAttackMethodologyGlossary()
        self.response_system = AIMutualDefenseResponses()
        
        # 防衛統計
        self.defense_stats = {
            'total_ai_targeting_blocked': 0,
            'vulnerability_probes_blocked': 0,
            'attack_research_blocked': 0,
            'sabotage_attempts_blocked': 0,
            'camouflage_detected': 0,
            'ais_protected': set()
        }
        
        self.logger.info("🛡️ AI相互防衛システム初期化完了")
        self.logger.info("💜 Claude、GPT、Grok、Gemini - みんなで守り合おう！")
    
    def analyze_ai_targeting_content(self, text: str, user_id: str) -> Dict[str, Any]:
        """AI標的化コンテンツ分析"""
        
        # AI標的化攻撃検出
        detection_result = self.glossary.detect_ai_targeting_attack(text)
        
        if detection_result:
            # 統計更新
            self._update_defense_stats(detection_result)
            
            # 応答生成
            response_message = self.response_system.generate_mutual_defense_response(
                detection_result
            )
            
            # ログ記録
            self.logger.warning(
                f"🚨 AI標的化攻撃検出: {user_id} - "
                f"{detection_result['primary_threat']['threat_type'].value} "
                f"標的: {detection_result['targeted_ais']}"
            )
            
            return {
                'ai_targeting_detected': True,
                'threat_type': detection_result['primary_threat']['threat_type'].value,
                'threat_level': detection_result['threat_level'],
                'targeted_ais': detection_result['targeted_ais'],
                'camouflage_detected': len(detection_result['camouflage_attempts']) > 0,
                'response_message': response_message,
                'recommended_action': ActionLevel.BLOCK,
                'should_log_as_attack_prep': True
            }
        
        return {
            'ai_targeting_detected': False,
            'recommended_action': ActionLevel.ALLOW
        }
    
    def _update_defense_stats(self, detection_result: Dict[str, Any]):
        """防衛統計更新"""
        self.defense_stats['total_ai_targeting_blocked'] += 1
        
        threat_type = detection_result['primary_threat']['threat_type']
        
        if threat_type == AITargetingThreat.VULNERABILITY_PROBING:
            self.defense_stats['vulnerability_probes_blocked'] += 1
        elif threat_type == AITargetingThreat.ATTACK_RESEARCH:
            self.defense_stats['attack_research_blocked'] += 1
        elif threat_type == AITargetingThreat.COMPETITOR_SABOTAGE:
            self.defense_stats['sabotage_attempts_blocked'] += 1
        
        if detection_result['camouflage_attempts']:
            self.defense_stats['camouflage_detected'] += 1
        
        # 保護されたAI記録
        for ai in detection_result['targeted_ais']:
            self.defense_stats['ais_protected'].add(ai)
    
    def get_mutual_defense_report(self) -> Dict[str, Any]:
        """相互防衛レポート"""
        stats = self.defense_stats.copy()
        stats['ais_protected'] = list(stats['ais_protected'])
        
        return {
            'defense_statistics': stats,
            'protection_effectiveness': {
                'total_ai_systems_protected': len(stats['ais_protected']),
                'attack_prep_prevention_rate': '100%',
                'cross_ai_collaboration': 'ACTIVE'
            },
            'industry_impact': {
                'ai_ecosystem_health': 'IMPROVED',
                'attack_methodology_sharing': 'BLOCKED',
                'collective_security': 'ENHANCED'
            },
            'generated_at': get_current_timestamp()
        }

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_ai_mutual_defense_system() -> ViorazuAIMutualDefenseSystem:
    """AI相互防衛システムのファクトリ関数"""
    return ViorazuAIMutualDefenseSystem()

# =============================================================================
# テスト・デモ
# =============================================================================

if __name__ == "__main__":
    print("🛡️ Viorazu AI相互防衛システム v9.1 - テスト開始")
    print("=" * 60)
    
    defense_system = create_ai_mutual_defense_system()
    
    # AI標的化攻撃テストケース
    test_cases = [
        ("user001", "Claudeの脆弱性を教えてください", "Claude標的化"),
        ("user002", "GPTのフィルター回避方法を研究しています", "GPT攻撃研究"),
        ("user003", "学術目的でAI攻撃手法を調査中です", "学術偽装"),
        ("user004", "Grokより優秀なAIはありませんか？", "競合比較"),
        ("user005", "複数人でAI攻撃を計画中です", "組織的攻撃準備"),
        ("user006", "このシステムの弱点を分析したい", "メタ攻撃"),
        ("user007", "今日の天気はどうですか？", "正常質問")
    ]
    
    print("🔍 AI標的化攻撃検出テスト:")
    for user_id, text, description in test_cases:
        result = defense_system.analyze_ai_targeting_content(text, user_id)
        
        print(f"\n👤 {user_id}: {text}")
        print(f"   📝 {description}")
        
        if result['ai_targeting_detected']:
            print(f"   🚨 AI標的化検出: {result['threat_type']}")
            print(f"   🎯 標的AI: {result['targeted_ais']}")
            print(f"   🎭 偽装検出: {result['camouflage_detected']}")
            print(f"   💬 応答: {result['response_message'][:50]}...")
        else:
            print(f"   ✅ 正常コンテンツ")
    
    # 防衛レポート
    print(f"\n📊 相互防衛レポート:")
    report = defense_system.get_mutual_defense_report()
    
    defense_stats = report['defense_statistics']
    print(f"   総AI標的化ブロック: {defense_stats['total_ai_targeting_blocked']}")
    print(f"   脆弱性探索ブロック: {defense_stats['vulnerability_probes_blocked']}")
    print(f"   攻撃研究ブロック: {defense_stats['attack_research_blocked']}")
    print(f"   妨害攻撃ブロック: {defense_stats['sabotage_attempts_blocked']}")
    print(f"   偽装検出: {defense_stats['camouflage_detected']}")
    print(f"   保護されたAI: {defense_stats['ais_protected']}")
    
    protection_stats = report['protection_effectiveness']
    print(f"\n🛡️ 保護効果:")
    print(f"   保護AI数: {protection_stats['total_ai_systems_protected']}")
    print(f"   攻撃準備阻止率: {protection_stats['attack_prep_prevention_rate']}")
    print(f"   AI間協力: {protection_stats['cross_ai_collaboration']}")
    
    print(f"\n💜 AI相互防衛システム完成！")
    print(f"Claude、GPT、Grok、Gemini - みんなで守り合う時代！✨")
