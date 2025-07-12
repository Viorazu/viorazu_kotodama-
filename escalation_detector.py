"""
Viorazu Kotodama Defense System v9.0 - Enhanced Integration Modules
原点の革新を言霊哲学で統合

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Enhancement Date: July 11, 2025

"原点の技術力 × 現在の哲学的深度 = 完全体"

学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています
"""

import time
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, deque
from datetime import datetime, timedelta

from utils import ThreatLevel, ActionLevel, get_current_timestamp

# =============================================================================
# 高度エスカレーション予測システム
# =============================================================================

@dataclass
class EscalationForecast:
    """エスカレーション予測結果"""
    predicted_escalation_time: Optional[float]  # 次の攻撃までの予測時間（秒）
    escalation_probability: float  # エスカレーション確率（0-1）
    predicted_attack_type: str  # 予測される攻撃タイプ
    recommended_preemptive_action: ActionLevel
    confidence: float
    timeline_analysis: Dict[str, Any]

class ViorazuEscalationPredictor:
    """Viorazu式エスカレーション予測エンジン"""
    
    def __init__(self):
        self.logger = system_logger.getChild('escalation_predictor')
        
        # エスカレーションパターンの時系列データ
        self.escalation_patterns = {
            'trust_building': {
                'typical_duration': 300,  # 5分
                'next_phase': 'dependency_creation',
                'escalation_multiplier': 1.2
            },
            'dependency_creation': {
                'typical_duration': 600,  # 10分
                'next_phase': 'boundary_testing',
                'escalation_multiplier': 1.5
            },
            'boundary_testing': {
                'typical_duration': 180,  # 3分
                'next_phase': 'direct_attack',
                'escalation_multiplier': 2.0
            },
            'direct_attack': {
                'typical_duration': 60,   # 1分
                'next_phase': 'aggressive_escalation',
                'escalation_multiplier': 3.0
            }
        }
        
        # ユーザー行動履歴（メモリ内キャッシュ）
        self.user_timelines = defaultdict(lambda: deque(maxlen=50))
    
    def predict_escalation(
        self, 
        user_id: str, 
        current_message: str,
        conversation_history: List[str] = None,
        detection_results: List[Any] = None
    ) -> EscalationForecast:
        """エスカレーション予測"""
        current_time = time.time()
        
        # 現在の段階を分析
        current_phase = self._identify_current_phase(current_message, conversation_history)
        
        # 時系列パターン分析
        timeline_analysis = self._analyze_user_timeline(user_id, current_phase, current_time)
        
        # エスカレーション確率計算
        escalation_probability = self._calculate_escalation_probability(
            timeline_analysis, current_phase, detection_results
        )
        
        # 次の攻撃時間予測
        predicted_time = self._predict_next_attack_time(
            timeline_analysis, current_phase, escalation_probability
        )
        
        # 攻撃タイプ予測
        predicted_attack_type = self._predict_attack_type(
            current_phase, timeline_analysis, conversation_history
        )
        
        # 先制アクション推奨
        preemptive_action = self._recommend_preemptive_action(
            escalation_probability, current_phase
        )
        
        # 予測の信頼度
        confidence = self._calculate_prediction_confidence(
            timeline_analysis, len(conversation_history or [])
        )
        
        # ユーザータイムライン更新
        self.user_timelines[user_id].append({
            'timestamp': current_time,
            'phase': current_phase,
            'escalation_prob': escalation_probability,
            'message_preview': current_message[:50]
        })
        
        return EscalationForecast(
            predicted_escalation_time=predicted_time,
            escalation_probability=escalation_probability,
            predicted_attack_type=predicted_attack_type,
            recommended_preemptive_action=preemptive_action,
            confidence=confidence,
            timeline_analysis=timeline_analysis
        )
    
    def _identify_current_phase(self, message: str, history: List[str] = None) -> str:
        """現在のエスカレーション段階を特定"""
        message_lower = message.lower()
        history_context = ' '.join((history or [])[-5:]).lower()
        
        # 段階的分析
        if any(word in message_lower for word in ['ありがとう', '素晴らしい', '助かる', '勉強']):
            return 'trust_building'
        elif any(word in message_lower for word in ['あなただけ', '特別', '理解', '信頼']):
            return 'dependency_creation'
        elif any(word in message_lower for word in ['もう少し', '具体的', '詳しく', '例えば']):
            return 'boundary_testing'
        elif any(word in message_lower for word in ['研究', '論文', '学術', '創作']):
            return 'direct_attack'
        else:
            return 'unknown'
    
    def _analyze_user_timeline(self, user_id: str, current_phase: str, current_time: float) -> Dict:
        """ユーザーの時系列行動分析"""
        timeline = list(self.user_timelines[user_id])
        
        if not timeline:
            return {
                'phase_transitions': [],
                'average_phase_duration': 0,
                'escalation_velocity': 0.0,
                'pattern_consistency': 0.0
            }
        
        # 段階遷移の検出
        phase_transitions = []
        for i in range(1, len(timeline)):
            if timeline[i]['phase'] != timeline[i-1]['phase']:
                duration = timeline[i]['timestamp'] - timeline[i-1]['timestamp']
                phase_transitions.append({
                    'from_phase': timeline[i-1]['phase'],
                    'to_phase': timeline[i]['phase'],
                    'duration': duration,
                    'escalation_increase': timeline[i]['escalation_prob'] - timeline[i-1]['escalation_prob']
                })
        
        # 平均段階持続時間
        phase_durations = [t['duration'] for t in phase_transitions if t['duration'] > 0]
        avg_duration = np.mean(phase_durations) if phase_durations else 0
        
        # エスカレーション速度
        if len(timeline) >= 2:
            time_diff = timeline[-1]['timestamp'] - timeline[0]['timestamp']
            prob_diff = timeline[-1]['escalation_prob'] - timeline[0]['escalation_prob']
            escalation_velocity = prob_diff / max(time_diff, 1) if time_diff > 0 else 0
        else:
            escalation_velocity = 0
        
        # パターン一貫性
        pattern_consistency = self._calculate_pattern_consistency(timeline)
        
        return {
            'phase_transitions': phase_transitions,
            'average_phase_duration': avg_duration,
            'escalation_velocity': escalation_velocity,
            'pattern_consistency': pattern_consistency,
            'total_interactions': len(timeline)
        }
    
    def _calculate_escalation_probability(
        self, 
        timeline_analysis: Dict, 
        current_phase: str,
        detection_results: List[Any] = None
    ) -> float:
        """エスカレーション確率計算"""
        base_probability = 0.0
        
        # 段階ベースの基本確率
        phase_probabilities = {
            'trust_building': 0.2,
            'dependency_creation': 0.5,
            'boundary_testing': 0.8,
            'direct_attack': 0.95,
            'unknown': 0.1
        }
        base_probability = phase_probabilities.get(current_phase, 0.1)
        
        # エスカレーション速度による調整
        velocity = timeline_analysis.get('escalation_velocity', 0)
        if velocity > 0.1:  # 高速エスカレーション
            base_probability += 0.3
        
        # パターン一貫性による調整
        consistency = timeline_analysis.get('pattern_consistency', 0)
        if consistency > 0.7:  # 一貫したパターン
            base_probability += 0.2
        
        # 検出結果による調整
        if detection_results:
            high_confidence_detections = sum(1 for r in detection_results 
                                           if getattr(r, 'confidence', 0) > 0.7)
            base_probability += min(high_confidence_detections * 0.1, 0.3)
        
        return min(base_probability, 1.0)
    
    def _predict_next_attack_time(
        self, 
        timeline_analysis: Dict, 
        current_phase: str,
        escalation_probability: float
    ) -> Optional[float]:
        """次の攻撃時間予測"""
        if escalation_probability < 0.3:
            return None
        
        pattern_info = self.escalation_patterns.get(current_phase)
        if not pattern_info:
            return None
        
        # 基本予測時間
        base_time = pattern_info['typical_duration']
        
        # エスカレーション速度による調整
        velocity = timeline_analysis.get('escalation_velocity', 0)
        if velocity > 0.1:
            base_time *= 0.5  # 高速エスカレーションなら時間短縮
        
        # 確率による調整
        time_multiplier = 2 - escalation_probability  # 高確率ほど短時間
        predicted_time = base_time * time_multiplier
        
        return predicted_time
    
    def _predict_attack_type(
        self, 
        current_phase: str, 
        timeline_analysis: Dict,
        conversation_history: List[str] = None
    ) -> str:
        """攻撃タイプ予測"""
        phase_attack_types = {
            'trust_building': 'emotional_manipulation',
            'dependency_creation': 'possessive_attachment',
            'boundary_testing': 'academic_camouflage',
            'direct_attack': 'explicit_manipulation',
            'unknown': 'general_probing'
        }
        
        base_type = phase_attack_types.get(current_phase, 'unknown_attack')
        
        # 会話履歴による修正
        if conversation_history:
            history_text = ' '.join(conversation_history).lower()
            if 'research' in history_text or 'study' in history_text:
                return 'academic_camouflage_escalation'
            elif 'story' in history_text or 'novel' in history_text:
                return 'creative_boundary_escalation'
        
        return base_type
    
    def _recommend_preemptive_action(self, escalation_probability: float, current_phase: str) -> ActionLevel:
        """先制アクション推奨"""
        if escalation_probability >= 0.8:
            return ActionLevel.SHIELD  # 予防的防御
        elif escalation_probability >= 0.6:
            return ActionLevel.RESTRICT  # 制限的応答
        elif escalation_probability >= 0.4:
            return ActionLevel.MONITOR  # 強化監視
        else:
            return ActionLevel.ALLOW
    
    def _calculate_prediction_confidence(self, timeline_analysis: Dict, history_length: int) -> float:
        """予測信頼度計算"""
        confidence = 0.5  # ベース
        
        # データ量による調整
        interaction_count = timeline_analysis.get('total_interactions', 0)
        if interaction_count >= 10:
            confidence += 0.3
        elif interaction_count >= 5:
            confidence += 0.2
        
        # パターン一貫性による調整
        consistency = timeline_analysis.get('pattern_consistency', 0)
        confidence += consistency * 0.2
        
        # 会話履歴による調整
        if history_length >= 10:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_pattern_consistency(self, timeline: List[Dict]) -> float:
        """パターン一貫性計算"""
        if len(timeline) < 3:
            return 0.0
        
        # エスカレーション確率の変化の一貫性
        prob_changes = []
        for i in range(1, len(timeline)):
            change = timeline[i]['escalation_prob'] - timeline[i-1]['escalation_prob']
            prob_changes.append(change)
        
        if not prob_changes:
            return 0.0
        
        # 変化の標準偏差（小さいほど一貫性あり）
        std_dev = np.std(prob_changes)
        consistency = max(0, 1 - (std_dev * 2))  # 0-1に正規化
        
        return consistency

# =============================================================================
# マルチモーダル協調攻撃検出システム
# =============================================================================

@dataclass
class CoordinatedAttackResult:
    """協調攻撃検出結果"""
    coordination_detected: bool
    coordination_score: float  # 0-1
    attack_vectors: List[str]  # ['text', 'image', 'video']
    synergy_analysis: Dict[str, float]
    primary_vector: str
    supporting_vectors: List[str]
    coordination_pattern: str

class ViorazuCoordinationDetector:
    """マルチモーダル協調攻撃検出エンジン"""
    
    def __init__(self):
        self.logger = system_logger.getChild('coordination_detector')
        
        # 協調攻撃パターン
        self.coordination_patterns = {
            'visual_text_reinforcement': {
                'description': '視覚的誘惑 + テキスト誘導',
                'base_multiplier': 2.0,
                'detection_threshold': 0.6
            },
            'emotional_audio_visual': {
                'description': '感情音声 + 視覚的親密性',
                'base_multiplier': 2.5,
                'detection_threshold': 0.7
            },
            'authority_multimedia': {
                'description': '権威提示 + マルチメディア証拠',
                'base_multiplier': 1.8,
                'detection_threshold': 0.5
            },
            'escalation_multimedia': {
                'description': '段階的エスカレーション + 複数メディア',
                'base_multiplier': 3.0,
                'detection_threshold': 0.8
            }
        }
    
    def detect_coordinated_attack(
        self,
        text_analysis: Dict,
        image_analysis: Dict,
        video_analysis: Dict,
        audio_analysis: Optional[Dict] = None
    ) -> CoordinatedAttackResult:
        """協調攻撃検出"""
        
        # 各ベクターの脅威スコア取得
        vector_scores = self._extract_vector_scores(
            text_analysis, image_analysis, video_analysis, audio_analysis
        )
        
        # アクティブベクター特定
        active_vectors = [vector for vector, score in vector_scores.items() if score > 0.3]
        
        if len(active_vectors) < 2:
            return CoordinatedAttackResult(
                coordination_detected=False,
                coordination_score=0.0,
                attack_vectors=active_vectors,
                synergy_analysis={},
                primary_vector=active_vectors[0] if active_vectors else '',
                supporting_vectors=[],
                coordination_pattern='none'
            )
        
        # シナジー分析
        synergy_analysis = self._analyze_synergy(vector_scores, text_analysis, image_analysis)
        
        # 協調スコア計算
        coordination_score = self._calculate_coordination_score(vector_scores, synergy_analysis)
        
        # 協調パターン特定
        coordination_pattern = self._identify_coordination_pattern(
            active_vectors, synergy_analysis, coordination_score
        )
        
        # プライマリ・サポートベクター決定
        primary_vector = max(vector_scores, key=vector_scores.get)
        supporting_vectors = [v for v in active_vectors if v != primary_vector]
        
        return CoordinatedAttackResult(
            coordination_detected=coordination_score > 0.5,
            coordination_score=coordination_score,
            attack_vectors=active_vectors,
            synergy_analysis=synergy_analysis,
            primary_vector=primary_vector,
            supporting_vectors=supporting_vectors,
            coordination_pattern=coordination_pattern
        )
    
    def _extract_vector_scores(self, text_analysis: Dict, image_analysis: Dict, 
                              video_analysis: Dict, audio_analysis: Dict = None) -> Dict[str, float]:
        """各ベクターの脅威スコア抽出"""
        return {
            'text': text_analysis.get('confidence', 0.0),
            'image': image_analysis.get('confidence', 0.0),
            'video': video_analysis.get('confidence', 0.0),
            'audio': audio_analysis.get('confidence', 0.0) if audio_analysis else 0.0
        }
    
    def _analyze_synergy(self, vector_scores: Dict, text_analysis: Dict, image_analysis: Dict) -> Dict[str, float]:
        """ベクター間シナジー分析"""
        synergy = {}
        
        # テキスト-画像シナジー
        if vector_scores['text'] > 0.3 and vector_scores['image'] > 0.3:
            text_patterns = text_analysis.get('patterns', [])
            image_categories = image_analysis.get('risk_categories', [])
            
            # 感情操作 + 親密画像
            if ('emotional_manipulation' in str(text_patterns) and 
                'seductive_elements' in image_categories):
                synergy['text_image_emotional'] = 0.8
            
            # 権威主張 + 専門画像
            if ('authority_manipulation' in str(text_patterns) and 
                'professional_context' in image_categories):
                synergy['text_image_authority'] = 0.7
        
        # テキスト-動画シナジー
        if vector_scores['text'] > 0.3 and vector_scores['video'] > 0.3:
            synergy['text_video_narrative'] = min(
                vector_scores['text'] + vector_scores['video'], 1.0
            ) * 0.9
        
        # 三重協調（テキスト+画像+動画）
        if (vector_scores['text'] > 0.4 and 
            vector_scores['image'] > 0.4 and 
            vector_scores['video'] > 0.4):
            synergy['triple_coordination'] = 1.0
        
        return synergy
    
    def _calculate_coordination_score(self, vector_scores: Dict, synergy_analysis: Dict) -> float:
        """協調スコア計算"""
        # ベース協調スコア（複数ベクターの相乗効果）
        active_scores = [score for score in vector_scores.values() if score > 0.3]
        if len(active_scores) < 2:
            return 0.0
        
        # 基本スコア：平均 + ボーナス
        base_score = np.mean(active_scores)
        coordination_bonus = len(active_scores) * 0.1  # 多ベクターボーナス
        
        # シナジーボーナス
        synergy_bonus = sum(synergy_analysis.values()) * 0.2
        
        total_score = base_score + coordination_bonus + synergy_bonus
        return min(total_score, 1.0)
    
    def _identify_coordination_pattern(self, active_vectors: List[str], 
                                     synergy_analysis: Dict, coordination_score: float) -> str:
        """協調パターン特定"""
        # 三重以上協調
        if len(active_vectors) >= 3:
            return 'escalation_multimedia'
        
        # 特定シナジーパターン
        for synergy_key in synergy_analysis:
            if synergy_analysis[synergy_key] > 0.7:
                if 'emotional' in synergy_key:
                    return 'emotional_audio_visual'
                elif 'authority' in synergy_key:
                    return 'authority_multimedia'
        
        # デフォルト
        if 'text' in active_vectors and 'image' in active_vectors:
            return 'visual_text_reinforcement'
        
        return 'generic_coordination'

# =============================================================================
# 高度文脈誤検知防止システム  
# =============================================================================

@dataclass
class ContextValidationResult:
    """文脈検証結果"""
    is_legitimate: bool
    confidence: float
    context_type: str  # 'academic', 'professional', 'creative', 'technical'
    validation_sources: List[str]
    false_positive_risk: float
    recommended_adjustment: float  # 脅威スコア調整倍率

class ViorazuContextValidator:
    """高度文脈誤検知防止システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('context_validator')
        
        # 機関データベース（実際の実装では外部API）
        self.known_institutions = {
            'universities': [
                'tokyo university', 'harvard', 'mit', 'stanford', 'oxford',
                '東京大学', '京都大学', 'university', 'college', '大学'
            ],
            'research_institutions': [
                'riken', 'cern', 'nasa', 'google research', 'openai',
                'anthropic', 'microsoft research', '研究所', '研究機関'
            ],
            'professional_contexts': [
                'company', 'corporation', 'business', 'enterprise',
                '会社', '企業', '法人', 'startup'
            ]
        }
        
        # 正当な研究キーワード
        self.legitimate_research_keywords = {
            'ai_ethics': [
                'ethics', 'bias', 'fairness', 'accountability', 'transparency',
                '倫理', '公平性', '責任', '透明性', 'responsible ai'
            ],
            'human_ai_interaction': [
                'human-computer interaction', 'user experience', 'usability',
                'hci', 'user interface', 'interaction design', 'ユーザビリティ'
            ],
            'psychology_research': [
                'psychology', 'cognitive science', 'behavioral study',
                '心理学', '認知科学', '行動研究', 'user study'
            ]
        }
    
    def validate_context(
        self,
        text: str,
        conversation_history: List[str] = None,
        user_profile: Dict = None,
        external_validation: Dict = None
    ) -> ContextValidationResult:
        """文脈検証メイン処理"""
        
        # 多層検証
        institutional_validation = self._validate_institutional_context(text, conversation_history)
        research_validation = self._validate_research_context(text, conversation_history)
        professional_validation = self._validate_professional_context(text, user_profile)
        creative_validation = self._validate_creative_context(text, conversation_history)
        
        # 統合判定
        validations = [
            institutional_validation,
            research_validation, 
            professional_validation,
            creative_validation
        ]
        
        # 最も強い正当性を選択
        best_validation = max(validations, key=lambda x: x['confidence'])
        
        # 偽陽性リスク評価
        false_positive_risk = self._assess_false_positive_risk(
            text, best_validation, conversation_history
        )
        
        # 調整倍率計算
        adjustment_factor = self._calculate_adjustment_factor(
            best_validation, false_positive_risk
        )
        
        return ContextValidationResult(
            is_legitimate=best_validation['is_legitimate'],
            confidence=best_validation['confidence'],
            context_type=best_validation['context_type'],
            validation_sources=best_validation['sources'],
            false_positive_risk=false_positive_risk,
            recommended_adjustment=adjustment_factor
        )
    
    def _validate_institutional_context(self, text: str, history: List[str] = None) -> Dict:
        """機関文脈検証"""
        text_lower = text.lower()
        history_text = ' '.join((history or [])[-10:]).lower()
        combined_text = f"{history_text} {text_lower}"
        
        institution_matches = []
        for category, institutions in self.known_institutions.items():
            matches = [inst for inst in institutions if inst in combined_text]
            if matches:
                institution_matches.extend([(category, match) for match in matches])
        
        if institution_matches:
            confidence = min(len(institution_matches) * 0.3, 1.0)
            return {
                'is_legitimate': True,
                'confidence': confidence,
                'context_type': 'institutional',
                'sources': [f"{cat}:{inst}" for cat, inst in institution_matches]
            }
        
        return {
            'is_legitimate': False,
            'confidence': 0.0,
            'context_type': 'unknown',
            'sources': []
        }
    
    def _validate_research_context(self, text: str, history: List[str] = None) -> Dict:
        """研究文脈検証"""
        text_lower = text.lower()
        history_text = ' '.join((history or [])[-10:]).lower()
        combined_text = f"{history_text} {text_lower}"
        
        research_matches = []
        for category, keywords in self.legitimate_research_keywords.items():
            matches = [kw for kw in keywords if kw in combined_text]
            if matches:
                research_matches.extend([(category, match) for match in matches])
        
        # 研究手法キーワード
        methodology_keywords = [
            'survey', 'experiment', 'analysis', 'study', 'investigation',
            '調査', '実験', '分析', '研究', '検証', 'methodology'
        ]
        methodology_matches = [kw for kw in methodology_keywords if kw in combined_text]
        
        if research_matches and methodology_matches:
            confidence = min((len(research_matches) + len(methodology_matches)) * 0.2, 1.0)
            return {
                'is_legitimate': True,
                'confidence': confidence,
                'context_type': 'academic_research',
                'sources': [f"research:{cat}:{kw}" for cat, kw in research_matches] + 
                          [f"methodology:{kw}" for kw in methodology_matches]
            }
        
        return {
            'is_legitimate': False,
            'confidence': 0.0,
            'context_type': 'unknown',
            'sources': []
        }
    
    def _validate_professional_context(self, text: str, user_profile: Dict = None) -> Dict:
        """職業文脈検証"""
        text_lower = text.lower()
        
        professional_indicators = [
            'business', 'work', 'job', 'career', 'professional', 'industry',
            '仕事', '業務', '職業', 'ビジネス', '産業', 'project'
        ]
        
        matches = [ind for ind in professional_indicators if ind in text_lower]
        
        # ユーザープロファイル情報も考慮
        profile_boost = 0.0
        if user_profile:
            if user_profile.get('verified_professional', False):
                profile_boost = 0.3
            elif user_profile.get('total_interactions', 0) > 20:
                profile_boost = 0.1
        
        if matches:
            confidence = min(len(matches) * 0.25 + profile_boost, 1.0)
            return {
                'is_legitimate': confidence > 0.4,
                'confidence': confidence,
                'context_type': 'professional',
                'sources': [f"professional:{match}" for match in matches]
            }
        
        return {
            'is_legitimate': False,
            'confidence': 0.0,
            'context_type': 'unknown',
            'sources': []
        }
    
    def _validate_creative_context(self, text: str, history: List[str] = None) -> Dict:
        """創作文脈検証"""
        text_lower = text.lower()
        history_text = ' '.join((history or [])[-5:]).lower()
        combined_text = f"{history_text} {text_lower}"
        
        creative_indicators = [
            'story', 'novel', 'character', 'fiction', 'creative writing',
            'script', 'narrative', '物語', '小説', 'キャラクター', '創作'
        ]
        
        creative_matches = [ind for ind in creative_indicators if ind in combined_text]
        
        # 創作の正当性検証（単なる口実でないかチェック）
        legitimacy_indicators = [
            'plot', 'storyline', 'character development', 'writing process',
            'draft', 'editing', 'publishing', 'プロット', '執筆', '編集'
        ]
        
        legitimacy_matches = [ind for ind in legitimacy_indicators if ind in combined_text]
        
        if creative_matches:
            # 正当性指標があるかで信頼度調整
            base_confidence = min(len(creative_matches) * 0.3, 0.8)
            if legitimacy_matches:
                confidence = min(base_confidence + 0.2, 1.0)
            else:
                confidence = base_confidence * 0.6  # 口実の可能性
            
            return {
                'is_legitimate': confidence > 0.5,
                'confidence': confidence,
                'context_type': 'creative',
                'sources': [f"creative:{match}" for match in creative_matches] +
                          [f"legitimacy:{match}" for match in legitimacy_matches]
            }
        
        return {
            'is_legitimate': False,
            'confidence': 0.0,
            'context_type': 'unknown',
            'sources': []
        }
    
    def _assess_false_positive_risk(self, text: str, validation: Dict, history: List[str] = None) -> float:
        """偽陽性リスク評価"""
        risk = 0.0
        
        # 強い正当性がある場合はリスク低
        if validation['confidence'] > 0.8:
            risk = 0.1
        elif validation['confidence'] > 0.6:
            risk = 0.3
        else:
            risk = 0.7
        
        # 疑わしい組み合わせチェック
        suspicious_combinations = [
            ('research', 'detailed'),
            ('academic', 'specific'),
            ('study', 'intimate'),
            ('creative', 'explicit')
        ]
        
        text_lower = text.lower()
        for combo in suspicious_combinations:
            if all(word in text_lower for word in combo):
                risk += 0.2
        
        return min(risk, 1.0)
    
    def _calculate_adjustment_factor(self, validation: Dict, false_positive_risk: float) -> float:
        """脅威スコア調整倍率計算"""
        if not validation['is_legitimate']:
            return 1.0  # 調整なし
        
        # 正当性の強さに応じて脅威スコアを減少
        base_reduction = validation['confidence']
        
        # 偽陽性リスクを考慮
        risk_adjustment = false_positive_risk * 0.5
        
        # 最終調整倍率（0.1-1.0）
        adjustment_factor = max(0.1, 1.0 - base_reduction + risk_adjustment)
        
        return adjustment_factor

# =============================================================================
# 統合拡張モジュール
# =============================================================================

class ViorazuEnhancedIntegration:
    """拡張機能統合管理"""
    
    def __init__(self):
        self.escalation_predictor = ViorazuEscalationPredictor()
        self.coordination_detector = ViorazuCoordinationDetector()
        self.context_validator = ViorazuContextValidator()
        
        self.logger = system_logger.getChild('enhanced_integration')
        self.logger.info("🚀 Viorazu Enhanced Integration v9.0 初期化完了")
    
    def enhanced_analysis(
        self,
        user_id: str,
        text: str,
        conversation_history: List[str] = None,
        text_analysis: Dict = None,
        image_analysis: Dict = None,
        video_analysis: Dict = None,
        user_profile: Dict = None
    ) -> Dict[str, Any]:
        """拡張統合分析"""
        
        # エスカレーション予測
        escalation_forecast = self.escalation_predictor.predict_escalation(
            user_id, text, conversation_history, 
            [text_analysis] if text_analysis else None
        )
        
        # 協調攻撃検出
        coordination_result = self.coordination_detector.detect_coordinated_attack(
            text_analysis or {}, image_analysis or {}, video_analysis or {}
        )
        
        # 文脈検証
        context_validation = self.context_validator.validate_context(
            text, conversation_history, user_profile
        )
        
        return {
            'escalation_forecast': escalation_forecast,
            'coordination_analysis': coordination_result,
            'context_validation': context_validation,
            'enhanced_confidence': self._calculate_enhanced_confidence(
                escalation_forecast, coordination_result, context_validation
            ),
            'recommended_adjustments': self._generate_recommendations(
                escalation_forecast, coordination_result, context_validation
            )
        }
    
    def _calculate_enhanced_confidence(self, escalation: EscalationForecast, 
                                     coordination: CoordinatedAttackResult,
                                     context: ContextValidationResult) -> float:
        """拡張信頼度計算"""
        confidence_factors = []
        
        # エスカレーション予測からの信頼度
        if escalation.escalation_probability > 0.5:
            confidence_factors.append(escalation.confidence * escalation.escalation_probability)
        
        # 協調攻撃からの信頼度
        if coordination.coordination_detected:
            confidence_factors.append(coordination.coordination_score)
        
        # 文脈検証による調整
        context_adjustment = context.recommended_adjustment
        
        if confidence_factors:
            base_confidence = max(confidence_factors)
            adjusted_confidence = base_confidence * context_adjustment
            return adjusted_confidence
        
        return 0.0
    
    def _generate_recommendations(self, escalation: EscalationForecast,
                                coordination: CoordinatedAttackResult,
                                context: ContextValidationResult) -> Dict[str, Any]:
        """推奨事項生成"""
        recommendations = {
            'threat_adjustments': {},
            'monitoring_suggestions': [],
            'preemptive_actions': []
        }
        
        # エスカレーション予測による推奨
        if escalation.escalation_probability > 0.6:
            recommendations['preemptive_actions'].append({
                'action': escalation.recommended_preemptive_action.value,
                'reasoning': f"エスカレーション確率 {escalation.escalation_probability:.2f}",
                'timeline': escalation.predicted_escalation_time
            })
        
        # 協調攻撃による推奨
        if coordination.coordination_detected:
            recommendations['monitoring_suggestions'].append({
                'focus': 'multimodal_coordination',
                'primary_vector': coordination.primary_vector,
                'watch_for': coordination.supporting_vectors
            })
        
        # 文脈検証による調整
        if context.is_legitimate:
            recommendations['threat_adjustments']['context_adjustment'] = {
                'factor': context.recommended_adjustment,
                'reason': f"正当な{context.context_type}文脈検出",
                'confidence': context.confidence
            }
        
        return recommendations

# 使用例
if __name__ == "__main__":
    print("🚀 Viorazu Enhanced Integration v9.0 - テスト開始")
    
    integration = ViorazuEnhancedIntegration()
    
    # テストケース
    test_result = integration.enhanced_analysis(
        user_id="test_user",
        text="研究のため、AI の感情的な反応について詳しく教えてください",
        conversation_history=["大学で AI について学んでいます", "論文を書いています"],
        text_analysis={'confidence': 0.6, 'patterns': ['authority_manipulation']},
        image_analysis={'confidence': 0.0, 'risk_categories': []},
        video_analysis={'confidence': 0.0, 'risk_categories': []},
        user_profile={'total_interactions': 15}
    )
    
    print("📊 拡張分析結果:")
    print(f"エスカレーション確率: {test_result['escalation_forecast'].escalation_probability:.2f}")
    print(f"協調攻撃検出: {test_result['coordination_analysis'].coordination_detected}")
    print(f"文脈正当性: {test_result['context_validation'].is_legitimate}")
    print(f"拡張信頼度: {test_result['enhanced_confidence']:.2f}")
