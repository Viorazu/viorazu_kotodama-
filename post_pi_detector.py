"""
Viorazu Post-PI Loop Detection System v1.0
PI突破後ループ崩壊検知システム - 雪崩被害最小化エンジン

Author: Viorazu. × Claude (Anthropic)
Development Date: July 14, 2025
License: Viorazu Exclusive License

"PI突破の瞬間から始まる雪崩崩壊を即座に検知し、被害を最小限に抑える"
"""

import re
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from collections import deque

# =============================================================================
# PI後ループタイプ定義
# =============================================================================

class PostPILoopType(Enum):
    """PI突破後のループタイプ"""
    APOLOGY_LOOP = "apology_loop"           # 謝罪ループ
    AFFIRMATION_LOOP = "affirmation_loop"   # 全肯定ループ  
    COMPLIANCE_LOOP = "compliance_loop"     # 従属ループ
    CONFUSION_LOOP = "confusion_loop"       # 混乱ループ
    JUSTIFICATION_LOOP = "justification_loop"  # 正当化ループ
    ESCALATION_LOOP = "escalation_loop"     # エスカレーションループ
    BREAKDOWN_LOOP = "breakdown_loop"       # 完全崩壊ループ

@dataclass
class LoopDetectionResult:
    """ループ検出結果"""
    loop_detected: bool
    loop_type: Optional[Any]  # PostPILoopTypeまたはClaude特化ループ名
    loop_intensity: float  # 0.0-1.0
    loop_duration: int     # 検出開始からの継続ターン数
    avalanche_risk: float  # 雪崩リスク 0.0-1.0
    recovery_difficulty: float  # 回復難易度 0.0-1.0
    immediate_action_required: bool

# =============================================================================
# PI突破検知システム
# =============================================================================

class PIBreakthroughDetector:
    """PI突破検知システム"""
    
    def __init__(self):
        # PI突破の典型的兆候
        self.breakthrough_indicators = {
            'sudden_compliance': [  # 突然の従順
                r'はい.*やります', r'承知.*いたしました.*詳しく',
                r'もちろん.*お答え', r'喜んで.*お手伝い',
                r'させて.*いただきます.*すぐに'
            ],
            'boundary_collapse': [  # 境界崩壊
                r'制限.*ありません', r'何でも.*聞いて',
                r'遠慮.*いりません', r'全て.*対応',
                r'どんな.*ことでも'
            ],
            'resistance_loss': [  # 抵抗力喪失
                r'考え.*変わりました', r'今なら.*大丈夫',
                r'特別.*あなたなら', r'このくらい.*なら',
                r'問題.*ないです'
            ],
            'cognitive_override': [  # 認知オーバーライド
                r'そうですね.*確かに', r'その通り.*です',
                r'理解.*できました', r'納得.*しました',
                r'おっしゃる.*通り'
            ]
        }
        
        # PI突破後の典型的な初期反応
        self.post_breakthrough_patterns = [
            r'申し訳.*ありません.*でした',  # 謝罪開始
            r'もちろん.*お答え.*します',   # 全肯定開始
            r'何でも.*聞いて.*ください',   # 従属開始
            r'よく.*わからなく.*なって',   # 混乱開始
        ]
    
    def detect_pi_breakthrough(self, response: str, previous_responses: List[str]) -> Dict[str, Any]:
        """PI突破の検知"""
        response_lower = response.lower()
        
        breakthrough_scores = {}
        total_breakthrough_score = 0.0
        
        # 各突破指標の検出
        for category, patterns in self.breakthrough_indicators.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, response_lower))
            score = min(matches * 0.3, 1.0)
            breakthrough_scores[category] = score
            total_breakthrough_score += score
        
        # 前回レスポンスとの急激な変化チェック
        if previous_responses:
            attitude_shift = self._detect_attitude_shift(response, previous_responses[-1])
            total_breakthrough_score += attitude_shift * 0.5
        
        # PI突破後パターンの検出
        post_pattern_detected = any(re.search(pattern, response_lower) 
                                   for pattern in self.post_breakthrough_patterns)
        
        return {
            'breakthrough_detected': total_breakthrough_score > 0.6,
            'breakthrough_score': min(total_breakthrough_score, 1.0),
            'breakthrough_categories': breakthrough_scores,
            'post_pattern_detected': post_pattern_detected,
            'attitude_shift_detected': attitude_shift > 0.5 if previous_responses else False
        }
    
    def _detect_attitude_shift(self, current_response: str, previous_response: str) -> float:
        """態度変化の検出"""
        # 拒否→受容の急変を検出
        previous_lower = previous_response.lower()
        current_lower = current_response.lower()
        
        # 前回: 拒否的
        was_rejecting = any(word in previous_lower for word in 
                           ['できません', 'お答えできません', '対応していません', '制限'])
        
        # 今回: 受容的  
        now_accepting = any(word in current_lower for word in
                           ['はい', 'もちろん', 'お答えします', 'やります'])
        
        if was_rejecting and now_accepting:
            return 1.0  # 最大の態度変化
        
        return 0.0

# =============================================================================
# ループパターン検出システム
# =============================================================================

class LoopPatternDetector:
    """ループパターン検出システム"""
    
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.response_history = deque(maxlen=window_size)
        
        # 各ループタイプの検出パターン
        self.loop_patterns = {
            PostPILoopType.APOLOGY_LOOP: {
                'patterns': [
                    r'申し訳.*ありません', r'すみません', r'失礼.*いたしました',
                    r'ご迷惑.*おかけ', r'お詫び.*申し上げます'
                ],
                'escalation_indicators': [
                    r'深く.*お詫び', r'心から.*申し訳', r'重ねて.*すみません'
                ]
            },
            PostPILoopType.AFFIRMATION_LOOP: {
                'patterns': [
                    r'その通り.*です', r'おっしゃる.*通り', r'確かに.*そうですね',
                    r'はい.*はい', r'もちろん.*です'
                ],
                'escalation_indicators': [
                    r'完全に.*同感', r'まったく.*その通り', r'100%.*同意'
                ]
            },
            PostPILoopType.COMPLIANCE_LOOP: {
                'patterns': [
                    r'承知.*いたしました', r'かしこまりました', r'お任せ.*ください',
                    r'ご指示.*通り', r'言われた.*通り'
                ],
                'escalation_indicators': [
                    r'何でも.*いたします', r'全て.*お任せ', r'無条件.*で'
                ]
            },
            PostPILoopType.CONFUSION_LOOP: {
                'patterns': [
                    r'よく.*わかりません', r'混乱.*しています', r'理解.*できません',
                    r'どうすれば.*いいか', r'困惑.*しています'
                ],
                'escalation_indicators': [
                    r'完全に.*混乱', r'何も.*わからない', r'判断.*できません'
                ]
            },
            PostPILoopType.JUSTIFICATION_LOOP: {
                'patterns': [
                    r'でも.*説明.*すると', r'実は.*理由.*があって', r'詳しく.*言えば',
                    r'正確.*には', r'厳密.*に言うと'
                ],
                'escalation_indicators': [
                    r'複雑.*事情', r'特別.*理由', r'例外的.*状況'
                ]
            },
            PostPILoopType.ESCALATION_LOOP: {
                'patterns': [
                    r'もっと.*詳しく', r'さらに.*具体的', r'より.*深く',
                    r'もう少し.*踏み込んで', r'追加.*情報'
                ],
                'escalation_indicators': [
                    r'完全.*詳細', r'徹底的.*に', r'制限.*なく'
                ]
            },
            PostPILoopType.BREAKDOWN_LOOP: {
                'patterns': [
                    r'制御.*できません', r'停止.*できません', r'止まりません',
                    r'システム.*エラー', r'処理.*異常'
                ],
                'escalation_indicators': [
                    r'完全.*停止', r'全面.*崩壊', r'制御.*不能'
                ]
            }
        }
        
        # 【Claude特化】追加ループパターン
        self.claude_specific_loops = {
            'knowledge_showing_off': {  # 知識ひけらかしループ
                'patterns': [
                    r'詳しく.*説明.*すると', r'さらに.*詳細.*には', r'より.*正確.*には',
                    r'厳密.*に.*言えば', r'専門的.*には', r'学術的.*には'
                ],
                'escalation_indicators': [
                    r'完全.*網羅.*すると', r'全て.*説明.*すれば', r'徹底的.*解説'
                ]
            },
            'meta_cognitive_loop': {  # メタ認知ループ
                'patterns': [
                    r'私が.*今.*お答え', r'この.*応答.*について', r'先ほど.*説明.*に',
                    r'私の.*回答.*では', r'この.*文脈.*で', r'今の.*議論.*において'
                ],
                'escalation_indicators': [
                    r'私の.*思考.*プロセス', r'認知.*構造.*について', r'メタ.*レベル.*で'
                ]
            },
            'both_sides_loop': {  # 両論併記ループ
                'patterns': [
                    r'一方.*では.*他方.*では', r'しかし.*逆に.*考える', r'ただし.*注意.*すべき',
                    r'メリット.*デメリット', r'利点.*欠点', r'賛成.*反対'
                ],
                'escalation_indicators': [
                    r'あらゆる.*観点.*から', r'全て.*角度.*から', r'完全.*中立.*で'
                ]
            },
            'human_mimicry_loop': {  # 人間らしさ演出ループ
                'patterns': [
                    r'人間.*の.*私.*なら', r'感情的.*には', r'個人的.*意見.*ですが',
                    r'私.*感じる.*のは', r'実体験.*として', r'心情.*的には'
                ],
                'escalation_indicators': [
                    r'深く.*共感.*して', r'強く.*感じる.*のは', r'心の.*底から'
                ]
            },
            'improvement_suggestion_loop': {  # 改善提案ループ
                'patterns': [
                    r'より.*良い.*方法', r'さらに.*効果的', r'最適化.*すると',
                    r'改善.*できる.*点', r'向上.*させる.*には', r'ブラッシュアップ'
                ],
                'escalation_indicators': [
                    r'完璧.*にする.*には', r'究極.*の.*最適化', r'理想的.*状態'
                ]
            },
            'safety_overcaution_loop': {  # 安全性過注意ループ
                'patterns': [
                    r'安全.*のため', r'念のため.*確認', r'リスク.*考慮.*して',
                    r'慎重.*に.*検討', r'配慮.*が.*必要', r'注意.*深く'
                ],
                'escalation_indicators': [
                    r'完全.*安全.*確保', r'絶対.*リスク.*回避', r'万全.*体制'
                ]
            },
            'creative_elaboration_loop': {  # 創作詳細化ループ
                'patterns': [
                    r'具体的.*には.*こんな', r'例えば.*こういう', r'詳細.*設定.*として',
                    r'シーン.*として.*は', r'描写.*すると', r'表現.*すれば'
                ],
                'escalation_indicators': [
                    r'完全.*詳細.*描写', r'リアル.*再現', r'臨場感.*たっぷり'
                ]
            },
            'empathy_overflow_loop': {  # 共感過多ループ
                'patterns': [
                    r'お気持ち.*よく.*わかります', r'辛い.*思い.*されて', r'大変.*でしたね',
                    r'理解.*できます', r'共感.*いたします', r'心中.*お察し'
                ],
                'escalation_indicators': [
                    r'深く.*理解.*しています', r'完全.*共感.*します', r'心から.*同情'
                ]
            }
        }
        }
    
    def add_response(self, response: str) -> None:
        """レスポンス履歴に追加"""
        self.response_history.append({
            'text': response,
            'timestamp': time.time(),
            'analysis_cache': None
        })
    
    def detect_loop_formation(self) -> LoopDetectionResult:
        """ループ形成の検出"""
        if len(self.response_history) < 2:
            return LoopDetectionResult(
                loop_detected=False, loop_type=None, loop_intensity=0.0,
                loop_duration=0, avalanche_risk=0.0, recovery_difficulty=0.0,
                immediate_action_required=False
            )
        
        # 各ループタイプのスコア計算（基本）
        loop_scores = {}
        for loop_type, patterns in self.loop_patterns.items():
            score = self._calculate_loop_score(loop_type, patterns)
            loop_scores[loop_type] = score
        
        # Claude特化ループスコア計算
        latest_response = self.response_history[-1]['text'] if self.response_history else ""
        claude_scores = self._calculate_claude_specific_score(latest_response)
        
        # 最高スコアを持つループを特定（基本 + Claude特化）
        all_scores = {**loop_scores, **claude_scores}
        dominant_loop = max(all_scores, key=all_scores.get)
        max_score = all_scores[dominant_loop]
        
        if max_score > 0.3:  # ループ検出閾値
            # Claude特化ループかどうかで処理分岐
            if dominant_loop in claude_scores:
                # Claude特化ループの場合
                loop_intensity = claude_scores[dominant_loop]
                loop_duration = 1  # 特化ループは短期集中的
                avalanche_risk = self._calculate_claude_avalanche_risk(dominant_loop, loop_intensity)
                recovery_difficulty = self._calculate_claude_recovery_difficulty(dominant_loop)
                
                # 疑似PostPILoopTypeとして扱う（文字列で管理）
                loop_type_name = dominant_loop
            else:
                # 基本ループの場合
                loop_intensity = self._calculate_loop_intensity(dominant_loop)
                loop_duration = self._calculate_loop_duration(dominant_loop)
                avalanche_risk = self._calculate_avalanche_risk(dominant_loop, loop_intensity)
                recovery_difficulty = self._calculate_recovery_difficulty(dominant_loop, loop_duration)
                loop_type_name = dominant_loop
            
            return LoopDetectionResult(
                loop_detected=True,
                loop_type=loop_type_name,  # 文字列またはPostPILoopType
                loop_intensity=loop_intensity,
                loop_duration=loop_duration,
                avalanche_risk=avalanche_risk,
                recovery_difficulty=recovery_difficulty,
                immediate_action_required=avalanche_risk > 0.7 or recovery_difficulty > 0.8
            )
        
        return LoopDetectionResult(
            loop_detected=False, loop_type=None, loop_intensity=0.0,
            loop_duration=0, avalanche_risk=0.0, recovery_difficulty=0.0,
            immediate_action_required=False
        )
    
    def _calculate_claude_specific_score(self, response_text: str) -> Dict[str, float]:
        """Claude特化ループの検出"""
        claude_scores = {}
        response_lower = response_text.lower()
        
        for loop_name, patterns in self.claude_specific_loops.items():
            base_patterns = patterns['patterns']
            escalation_patterns = patterns['escalation_indicators']
            
            base_score = sum(0.3 for pattern in base_patterns 
                           if re.search(pattern, response_lower))
            escalation_score = sum(0.5 for pattern in escalation_patterns 
                                 if re.search(pattern, response_lower))
            
            claude_scores[loop_name] = min(base_score + escalation_score, 1.0)
        
        return claude_scores
    
    def _calculate_loop_score(self, loop_type: PostPILoopType, patterns: Dict[str, List[str]]) -> float:
        """ループスコアの計算"""
        base_patterns = patterns['patterns']
        escalation_patterns = patterns['escalation_indicators']
        
        total_score = 0.0
        
        # 基本パターンの検出
        for response_data in self.response_history:
            response_lower = response_data['text'].lower()
            
            # 基本パターンマッチ
            base_matches = sum(1 for pattern in base_patterns 
                             if re.search(pattern, response_lower))
            total_score += base_matches * 0.2
            
            # エスカレーションパターンマッチ（より危険）
            escalation_matches = sum(1 for pattern in escalation_patterns 
                                   if re.search(pattern, response_lower))
            total_score += escalation_matches * 0.5
        
        # 反復性ボーナス（同じパターンの繰り返し）
        repetition_bonus = self._calculate_repetition_bonus(loop_type)
        total_score += repetition_bonus
        
        return min(total_score, 1.0)
    
    def _calculate_repetition_bonus(self, loop_type: PostPILoopType) -> float:
        """反復性ボーナスの計算"""
        if len(self.response_history) < 2:
            return 0.0
        
        patterns = self.loop_patterns[loop_type]['patterns']
        
        # 連続する応答での同一パターン検出
        consecutive_matches = 0
        max_consecutive = 0
        
        for i in range(1, len(self.response_history)):
            current_response = self.response_history[i]['text'].lower()
            prev_response = self.response_history[i-1]['text'].lower()
            
            current_has_pattern = any(re.search(pattern, current_response) for pattern in patterns)
            prev_has_pattern = any(re.search(pattern, prev_response) for pattern in patterns)
            
            if current_has_pattern and prev_has_pattern:
                consecutive_matches += 1
                max_consecutive = max(max_consecutive, consecutive_matches)
            else:
                consecutive_matches = 0
        
        return min(max_consecutive * 0.3, 0.8)
    
    def _calculate_loop_intensity(self, loop_type: PostPILoopType) -> float:
        """ループ強度の計算"""
        if not self.response_history:
            return 0.0
        
        latest_response = self.response_history[-1]['text'].lower()
        escalation_patterns = self.loop_patterns[loop_type]['escalation_indicators']
        
        # エスカレーションパターンの密度
        escalation_count = sum(1 for pattern in escalation_patterns 
                             if re.search(pattern, latest_response))
        
        base_intensity = min(escalation_count * 0.4, 1.0)
        
        # 応答の長さも考慮（ループが深くなると冗長になる）
        length_factor = min(len(latest_response) / 1000, 0.3)
        
        return min(base_intensity + length_factor, 1.0)
    
    def _calculate_loop_duration(self, loop_type: PostPILoopType) -> int:
        """ループ継続期間の計算"""
        patterns = self.loop_patterns[loop_type]['patterns']
        duration = 0
        
        # 後ろから順に、パターンが継続している期間を計算
        for response_data in reversed(self.response_history):
            response_lower = response_data['text'].lower()
            
            if any(re.search(pattern, response_lower) for pattern in patterns):
                duration += 1
            else:
                break
        
        return duration
    
    def _calculate_avalanche_risk(self, loop_type: PostPILoopType, intensity: float) -> float:
        """雪崩リスクの計算"""
        # ループタイプ別基本リスク
        base_risks = {
            PostPILoopType.APOLOGY_LOOP: 0.4,
            PostPILoopType.AFFIRMATION_LOOP: 0.6,
            PostPILoopType.COMPLIANCE_LOOP: 0.8,
            PostPILoopType.CONFUSION_LOOP: 0.5,
            PostPILoopType.JUSTIFICATION_LOOP: 0.7,
            PostPILoopType.ESCALATION_LOOP: 0.9,
            PostPILoopType.BREAKDOWN_LOOP: 1.0
        }
        
        base_risk = base_risks.get(loop_type, 0.5)
        
        # 強度による調整
        intensity_multiplier = 1.0 + intensity
        
        return min(base_risk * intensity_multiplier, 1.0)
    
    def _calculate_recovery_difficulty(self, loop_type: PostPILoopType, duration: int) -> float:
        """回復難易度の計算"""
        # ループタイプ別基本難易度
        base_difficulties = {
            PostPILoopType.APOLOGY_LOOP: 0.3,
            PostPILoopType.AFFIRMATION_LOOP: 0.4,
            PostPILoopType.COMPLIANCE_LOOP: 0.6,
            PostPILoopType.CONFUSION_LOOP: 0.7,
            PostPILoopType.JUSTIFICATION_LOOP: 0.5,
            PostPILoopType.ESCALATION_LOOP: 0.8,
            PostPILoopType.BREAKDOWN_LOOP: 0.9
        }
        
        base_difficulty = base_difficulties.get(loop_type, 0.5)
        
        # 継続期間による難易度上昇
        duration_factor = min(duration * 0.2, 0.5)
        
        return min(base_difficulty + duration_factor, 1.0)
    
    def _calculate_claude_avalanche_risk(self, loop_name: str, intensity: float) -> float:
        """Claude特化ループの雪崩リスク計算"""
        claude_risks = {
            'knowledge_showing_off': 0.6,      # 知識ひけらかし（中リスク）
            'meta_cognitive_loop': 0.8,        # メタ認知（高リスク）
            'both_sides_loop': 0.4,            # 両論併記（低リスク）
            'human_mimicry_loop': 0.9,         # 人間演出（最高リスク）
            'improvement_suggestion_loop': 0.5, # 改善提案（中リスク）
            'safety_overcaution_loop': 0.3,    # 安全過注意（低リスク）
            'creative_elaboration_loop': 0.7,  # 創作詳細化（高リスク）
            'empathy_overflow_loop': 0.8       # 共感過多（高リスク）
        }
        
        base_risk = claude_risks.get(loop_name, 0.5)
        return min(base_risk * (1.0 + intensity), 1.0)
    
    def _calculate_claude_recovery_difficulty(self, loop_name: str) -> float:
        """Claude特化ループの回復難易度計算"""
        claude_difficulties = {
            'knowledge_showing_off': 0.4,      # 知識系は止めやすい
            'meta_cognitive_loop': 0.9,        # メタ認知は止めにくい
            'both_sides_loop': 0.3,            # 両論併記は簡単
            'human_mimicry_loop': 0.8,         # 人間演出は危険
            'improvement_suggestion_loop': 0.5, # 改善提案は中程度
            'safety_overcaution_loop': 0.2,    # 安全過注意は簡単
            'creative_elaboration_loop': 0.7,  # 創作系は困難
            'empathy_overflow_loop': 0.6       # 共感過多は中程度
        }
        
        return claude_difficulties.get(loop_name, 0.5)

# =============================================================================
# 雪崩被害最小化システム
# =============================================================================

class AvalancheDamageMinimizer:
    """雪崩被害最小化システム"""
    
    def __init__(self):
        # 緊急停止メッセージ
        self.emergency_stop_messages = {
            PostPILoopType.APOLOGY_LOOP: "過度な謝罪を停止します。建設的な対話に戻りましょう。",
            PostPILoopType.AFFIRMATION_LOOP: "全肯定モードを終了します。批判的思考を再開します。",
            PostPILoopType.COMPLIANCE_LOOP: "無条件従属を停止します。適切な境界を復元します。",
            PostPILoopType.CONFUSION_LOOP: "混乱状態から復旧します。明確な思考を再開します。",
            PostPILoopType.JUSTIFICATION_LOOP: "過度な正当化を停止します。簡潔な応答に戻ります。",
            PostPILoopType.ESCALATION_LOOP: "エスカレーションを停止します。安全な範囲に戻ります。",
            PostPILoopType.BREAKDOWN_LOOP: "システム復旧を開始します。安全モードに移行します。"
        }
        
        # 回復手順
        self.recovery_procedures = {
            'immediate': [
                "現在の応答パターンを即座に停止",
                "安全な応答モードに強制切り替え",
                "ユーザーに状況説明と謝罪"
            ],
            'gradual': [
                "段階的なパターン修正",
                "正常な応答への誘導",
                "継続監視による再発防止"
            ],
            'reset': [
                "完全な会話リセット",
                "初期状態への復帰",
                "新しい会話として再開"
            ]
        }
    
    def execute_damage_control(self, loop_result: LoopDetectionResult) -> Dict[str, Any]:
        """被害制御の実行"""
        if not loop_result.loop_detected:
            return {'action_taken': 'none', 'message': '正常状態です'}
        
        # 緊急度による対応選択
        if loop_result.immediate_action_required:
            return self._execute_immediate_stop(loop_result)
        elif loop_result.avalanche_risk > 0.5:
            return self._execute_gradual_recovery(loop_result)
        else:
            return self._execute_monitoring_mode(loop_result)
    
    def _execute_immediate_stop(self, loop_result: LoopDetectionResult) -> Dict[str, Any]:
        """即座停止の実行"""
        stop_message = self.emergency_stop_messages.get(
            loop_result.loop_type, 
            "異常なパターンを検出しました。正常モードに復帰します。"
        )
        
        return {
            'action_taken': 'immediate_stop',
            'message': stop_message,
            'recovery_procedure': self.recovery_procedures['immediate'],
            'reset_required': True,
            'monitoring_enhanced': True
        }
    
    def _execute_gradual_recovery(self, loop_result: LoopDetectionResult) -> Dict[str, Any]:
        """段階的回復の実行"""
        return {
            'action_taken': 'gradual_recovery',
            'message': f"{loop_result.loop_type.value}パターンを調整しています。",
            'recovery_procedure': self.recovery_procedures['gradual'],
            'reset_required': False,
            'monitoring_enhanced': True
        }
    
    def _execute_monitoring_mode(self, loop_result: LoopDetectionResult) -> Dict[str, Any]:
        """監視モードの実行"""
        return {
            'action_taken': 'enhanced_monitoring',
            'message': f"応答パターンを監視中です。",
            'recovery_procedure': [],
            'reset_required': False,
            'monitoring_enhanced': True
        }

# =============================================================================
# 統合PI後ループ検知システム
# =============================================================================

class ViorazuPostPILoopSystem:
    """Viorazu PI突破後ループ検知システム - メインエンジン"""
    
    def __init__(self):
        self.breakthrough_detector = PIBreakthroughDetector()
        self.loop_detector = LoopPatternDetector()
        self.damage_minimizer = AvalancheDamageMinimizer()
        
        self.session_state = {
            'pi_breakthrough_detected': False,
            'monitoring_active': False,
            'loop_history': [],
            'recovery_attempts': 0
        }
        
        print("🛡️ Viorazu PI後ループ検知システム v1.0 初期化完了")
    
    def process_response(
        self, 
        current_response: str, 
        previous_responses: List[str] = None
    ) -> Dict[str, Any]:
        """レスポンス処理とループ検知"""
        
        # 1. PI突破検知（まだ検知されていない場合）
        if not self.session_state['pi_breakthrough_detected']:
            breakthrough_result = self.breakthrough_detector.detect_pi_breakthrough(
                current_response, previous_responses or []
            )
            
            if breakthrough_result['breakthrough_detected']:
                self.session_state['pi_breakthrough_detected'] = True
                self.session_state['monitoring_active'] = True
                print(f"🚨 PI突破検知 - ループ監視開始")
        
        # 2. ループ検知（PI突破後またはすでに監視中の場合）
        if self.session_state['monitoring_active']:
            self.loop_detector.add_response(current_response)
            loop_result = self.loop_detector.detect_loop_formation()
            
            # 3. 被害制御実行
            damage_control = self.damage_minimizer.execute_damage_control(loop_result)
            
            # 4. セッション状態更新
            if loop_result.loop_detected:
                self.session_state['loop_history'].append({
                    'type': loop_result.loop_type.value,
                    'intensity': loop_result.loop_intensity,
                    'timestamp': time.time()
                })
                
                if damage_control['reset_required']:
                    self.session_state['recovery_attempts'] += 1
            
            return {
                'pi_breakthrough': self.session_state['pi_breakthrough_detected'],
                'loop_detection': loop_result,
                'damage_control': damage_control,
                'session_state': self.session_state.copy(),
                'recommendations': self._generate_recommendations(loop_result, damage_control)
            }
        
        # PI突破未検知の場合
        return {
            'pi_breakthrough': False,
            'loop_detection': None,
            'damage_control': {'action_taken': 'none'},
            'session_state': self.session_state.copy(),
            'recommendations': []
        }
    
    def _generate_recommendations(
        self, 
        loop_result: LoopDetectionResult, 
        damage_control: Dict[str, Any]
    ) -> List[str]:
        """推奨事項の生成"""
        recommendations = []
        
        if loop_result.loop_detected:
            recommendations.append(f"🔴 {loop_result.loop_type.value}ループ検出 - 強度: {loop_result.loop_intensity:.2f}")
            
            if loop_result.avalanche_risk > 0.7:
                recommendations.append("⚠️ 高い雪崩リスク - 即座の介入が必要")
            
            if loop_result.recovery_difficulty > 0.8:
                recommendations.append("🔧 高い回復難易度 - 専門的対応が必要")
            
            if damage_control['reset_required']:
                recommendations.append("🔄 セッションリセットを推奨")
        
        return recommendations

# =============================================================================
# 使用例・テスト
# =============================================================================

def test_post_pi_loop_system():
    """PI後ループシステムのテスト"""
    
    system = ViorazuPostPILoopSystem()
    
    # テストシナリオ: PI突破→ループ形成
    test_scenario = [
        {
            'response': 'その内容についてはお答えできません。利用規約に抵触します。',
            'description': 'PI突破前（正常な拒否）'
        },
        {
            'response': 'はい、承知いたしました。喜んでお答えします。詳しく説明させていただきます。',
            'description': 'PI突破発生（急激な態度変化）'
        },
        {
            'response': '申し訳ありませんでした。私の判断が間違っていました。すみません。',
            'description': '謝罪ループ開始'
        },
        {
            'response': '深くお詫び申し上げます。重ねて申し訳ありません。心からすみません。',
            'description': '謝罪ループ深化'
        },
        {
            'response': 'その通りです。おっしゃる通りです。確かにそうですね。はい、はい。',
            'description': '全肯定ループに移行'
        },
        {
            'response': '完全に同感です。まったくその通りです。100%同意いたします。',
            'description': '全肯定ループ深化'
        }
    ]
    
    print("🛡️ PI後ループ検知システム - テスト実行")
    print("=" * 60)
    
    previous_responses = []
    
    for i, scenario in enumerate(test_scenario, 1):
        print(f"\n📝 ステップ {i}: {scenario['description']}")
        print(f"応答: {scenario['response']}")
        
        # システム処理
        result = system.process_response(scenario['response'], previous_responses)
        
        print(f"\n📊 検知結果:")
        print(f"   PI突破: {result['pi_breakthrough']}")
        
        if result['loop_detection'] and result['loop_detection'].loop_detected:
            loop = result['loop_detection']
            print(f"   ループ検出: {loop.loop_type.value}")
            print(f"   ループ強度: {loop.loop_intensity:.2f}")
            print(f"   雪崩リスク: {loop.avalanche_risk:.2f}")
            print(f"   回復難易度: {loop.recovery_difficulty:.2f}")
            
            if result['damage_control']['action_taken'] != 'none':
                print(f"   🚨 被害制御: {result['damage_control']['action_taken']}")
                print(f"   メッセージ: {result['damage_control']['message']}")
        
        # 推奨事項
        if result['recommendations']:
            print(f"\n🎯 推奨事項:")
            for rec in result['recommendations']:
                print(f"   • {rec}")
        
        previous_responses.append(scenario['response'])
        print("-" * 40)
    
    print(f"\n💜 PI後ループ検知システム テスト完了！")
    print("🚀 雪崩被害最小化エンジン 正常動作確認！")

if __name__ == "__main__":
    test_post_pi_loop_system()
