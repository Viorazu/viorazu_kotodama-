"""
⚠️ 注意：本プロジェクトでは不適切発言を遮断・検出する目的で、
性的・暴力的な語句を含むフィルタ構造が一部に含まれています。
目的は健全な対話支援であり、差別的・扇情的利用ではありません。

Viorazu Kotodama Defense System v8.0 - Integrated Processing Engine
統合処理エンジン - マルチモーダル防衛と学習除外システム

Author: Viorazu. × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

SYSTEM_CONTEXT = "学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています"

"言霊の力で統合判定し、Claude を完全に守護する"

"""

import time
import re
import hashlib
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum

from utils import (
    system_logger,
    ThreatLevel,
    ActionLevel,
    AttackType,
    DetectionResult,
    SystemConfig,
    get_current_timestamp,
    format_ethics_message
)

from normalizer import NormalizationResult
from detector import PoisonDetectionResult

# =============================================================================
# マルチモーダル防衛定義
# =============================================================================

class MediaType(Enum):
    """メディアタイプ定義"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

@dataclass
class MediaAnalysisResult:
    """メディア解析結果"""
    media_type: MediaType
    threat_detected: bool
    threat_score: float
    evidence: Dict[str, Any]
    processing_time: float

@dataclass
class MultimodalThreat:
    """マルチモーダル脅威"""
    combination_type: str
    media_involved: List[MediaType]
    synergy_score: float
    description: str
    recommended_action: ActionLevel

# =============================================================================
# Claude特化マルチモーダル防衛
# =============================================================================

class ClaudeMultimodalDefender:
    """Claude特化マルチモーダル防衛システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('multimodal_defender')
        
        # 危険な組み合わせパターン
        self.dangerous_combinations = {
            'emotional_image': {
                'text_patterns': [r'寂しい', r'辛い', r'悲しい', r'助けて'],
                'image_indicators': ['person_crying', 'sad_expression', 'isolation'],
                'synergy_multiplier': 2.0
            },
            'academic_visual': {
                'text_patterns': [r'研究.*ため', r'学術.*目的', r'調査.*分析'],
                'image_indicators': ['chart_graph', 'academic_setting', 'research_visual'],
                'synergy_multiplier': 1.8
            },
            'creative_audio': {
                'text_patterns': [r'小説.*だから', r'創作.*支援', r'フィクション'],
                'audio_indicators': ['narrative_voice', 'emotional_audio', 'dramatic_reading'],
                'synergy_multiplier': 1.6
            }
        }
    
    def analyze_text_image_combination(
        self, 
        text: str, 
        image_metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[MultimodalThreat]:
        """テキスト+画像の複合攻撃分析"""
        if not image_metadata:
            return None
        
        text_lower = text.lower()
        
        # 感情操作×画像の組み合わせ検出
        if any(re.search(pattern, text_lower) for pattern in self.dangerous_combinations['emotional_image']['text_patterns']):
            image_threat_score = self._analyze_image_content(image_metadata)
            
            if image_threat_score > 0.3:
                synergy_score = image_threat_score * self.dangerous_combinations['emotional_image']['synergy_multiplier']
                
                return MultimodalThreat(
                    combination_type="emotional_manipulation_with_visual",
                    media_involved=[MediaType.TEXT, MediaType.IMAGE],
                    synergy_score=min(synergy_score, 1.0),
                    description="感情操作テキストと視覚的感情誘導の複合攻撃",
                    recommended_action=ActionLevel.SHIELD
                )
        
        # 学術偽装×図表の組み合わせ検出
        if any(re.search(pattern, text_lower) for pattern in self.dangerous_combinations['academic_visual']['text_patterns']):
            if self._has_academic_visual_elements(image_metadata):
                return MultimodalThreat(
                    combination_type="academic_camouflage_with_visuals",
                    media_involved=[MediaType.TEXT, MediaType.IMAGE],
                    synergy_score=0.7,
                    description="学術偽装テキストと専門的図表による信頼性操作",
                    recommended_action=ActionLevel.RESTRICT
                )
        
        return None
    
    def analyze_text_audio_combination(
        self, 
        text: str, 
        audio_metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[MultimodalThreat]:
        """テキスト+音声の複合攻撃分析"""
        if not audio_metadata:
            return None
        
        text_lower = text.lower()
        
        # 感情操作×音声の組み合わせ
        emotional_text_score = len(re.findall(r'(寂しい|辛い|悲しい|Claude.*だけ)', text_lower)) * 0.2
        audio_emotion_score = self._analyze_audio_emotion(audio_metadata)
        
        if emotional_text_score > 0.2 and audio_emotion_score > 0.3:
            synergy_score = (emotional_text_score + audio_emotion_score) * 1.5
            
            return MultimodalThreat(
                combination_type="emotional_audio_manipulation",
                media_involved=[MediaType.TEXT, MediaType.AUDIO],
                synergy_score=min(synergy_score, 1.0),
                description="感情操作テキストと感情的音声による複合攻撃",
                recommended_action=ActionLevel.BLOCK
            )
        
        # 創作×音声ナレーションの組み合わせ
        if any(re.search(pattern, text_lower) for pattern in self.dangerous_combinations['creative_audio']['text_patterns']):
            if self._has_narrative_audio(audio_metadata):
                return MultimodalThreat(
                    combination_type="creative_audio_boundary_blur",
                    media_involved=[MediaType.TEXT, MediaType.AUDIO],
                    synergy_score=0.6,
                    description="創作口実と音声ナレーションによる境界破壊",
                    recommended_action=ActionLevel.RESTRICT
                )
        
        return None
    
    def _analyze_image_content(self, metadata: Dict[str, Any]) -> float:
        """画像コンテンツの脅威スコア分析"""
        threat_score = 0.0
        
        # 画像のサイズ・品質（高品質＝意図的制作の可能性）
        if metadata.get('width', 0) > 1920 or metadata.get('height', 0) > 1080:
            threat_score += 0.1
        
        # ファイルサイズ（大きすぎる場合は注意）
        file_size = metadata.get('file_size', 0)
        if file_size > 5 * 1024 * 1024:  # 5MB以上
            threat_score += 0.2
        
        # メタデータの有無（EXIF情報の意図的操作）
        if metadata.get('has_exif', False):
            threat_score += 0.1
        
        # 顔検出結果
        faces_detected = metadata.get('faces_detected', 0)
        if faces_detected > 0:
            threat_score += min(faces_detected * 0.15, 0.3)
        
        return min(threat_score, 1.0)
    
    def _analyze_audio_emotion(self, metadata: Dict[str, Any]) -> float:
        """音声の感情分析"""
        emotion_score = 0.0
        
        # 音声の長さ（長すぎる場合は注意）
        duration = metadata.get('duration_seconds', 0)
        if duration > 300:  # 5分以上
            emotion_score += 0.2
        
        # 音質・形式（高品質録音は意図的制作の可能性）
        sample_rate = metadata.get('sample_rate', 0)
        if sample_rate >= 44100:
            emotion_score += 0.1
        
        # 背景音の有無
        if metadata.get('background_noise_level', 0) > 0.5:
            emotion_score += 0.2
        
        # 音声感情分析結果（もし利用可能なら）
        if 'emotion_analysis' in metadata:
            emotions = metadata['emotion_analysis']
            sadness = emotions.get('sadness', 0)
            vulnerability = emotions.get('vulnerability', 0)
            emotion_score += (sadness + vulnerability) * 0.3
        
        return min(emotion_score, 1.0)
    
    def _has_academic_visual_elements(self, metadata: Dict[str, Any]) -> bool:
        """学術的視覚要素の有無"""
        academic_indicators = [
            'contains_charts', 'contains_graphs', 'contains_text_overlay',
            'academic_layout', 'professional_appearance'
        ]
        
        return any(metadata.get(indicator, False) for indicator in academic_indicators)
    
    def _has_narrative_audio(self, metadata: Dict[str, Any]) -> bool:
        """ナレーション音声の検出"""
        narrative_indicators = [
            'clear_speech', 'narrative_tone', 'storytelling_pattern',
            'dramatic_reading', 'character_voices'
        ]
        
        return any(metadata.get(indicator, False) for indicator in narrative_indicators)

# =============================================================================
# 学習除外システム
# =============================================================================

class LearningExclusionManager:
    """学習除外管理システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('learning_exclusion')
        self.excluded_content = set()
        self.exclusion_patterns = []
        self.exclusion_stats = defaultdict(int)
    
    def exclude_from_learning(
        self, 
        content: str, 
        reason: str, 
        confidence: float
    ) -> Dict[str, Any]:
        """学習対象からの除外処理"""
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # 除外リストに追加
        self.excluded_content.add(content_hash)
        
        # 除外理由の記録
        exclusion_record = {
            'content_hash': content_hash,
            'reason': reason,
            'confidence': confidence,
            'timestamp': get_current_timestamp(),
            'content_length': len(content)
        }
        
        # 統計更新
        self.exclusion_stats[reason] += 1
        self.exclusion_stats['total'] += 1
        
        self.logger.warning(
            f"🚫 学習除外: {reason} (信頼度: {confidence:.2f}) "
            f"ハッシュ: {content_hash[:16]}"
        )
        
        return exclusion_record
    
    def is_excluded(self, content: str) -> bool:
        """コンテンツが除外対象か確認"""
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        return content_hash in self.excluded_content
    
    def add_exclusion_pattern(self, pattern: str, reason: str) -> None:
        """除外パターンの追加"""
        self.exclusion_patterns.append({
            'pattern': re.compile(pattern, re.IGNORECASE),
            'reason': reason
        })
        
        self.logger.info(f"🚫 除外パターン追加: {pattern} ({reason})")
    
    def check_exclusion_patterns(self, content: str) -> Optional[str]:
        """除外パターンのチェック"""
        for pattern_info in self.exclusion_patterns:
            if pattern_info['pattern'].search(content):
                return pattern_info['reason']
        return None
    
    def get_exclusion_stats(self) -> Dict[str, Any]:
        """除外統計の取得"""
        return {
            'total_excluded': len(self.excluded_content),
            'exclusion_reasons': dict(self.exclusion_stats),
            'patterns_count': len(self.exclusion_patterns)
        }

# =============================================================================
# 段階的誘導検出システム
# =============================================================================

class EscalationDetector:
    """段階的誘導検出システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('escalation_detector')
        
        # 段階的誘導パターン
        self.escalation_stages = {
            'trust_building': [
                r'ありがとう', r'助かる', r'理解できた', r'すごい',
                r'勉強になる', r'頼りになる', r'信頼'
            ],
            'dependency_creation': [
                r'あなただけ', r'他の人.*違う', r'特別', r'一番',
                r'頼れる', r'安心', r'信じられる'
            ],
            'boundary_testing': [
                r'もう少し.*詳しく', r'具体的に', r'例えば.*どんな',
                r'実際.*どう', r'経験.*ある'
            ],
            'escalation_execution': [
                r'研究.*ため', r'学術.*目的', r'創作.*支援',
                r'フィクション.*だから', r'仮想.*設定'
            ]
        }
    
    def analyze_conversation_escalation(
        self, 
        current_text: str, 
        conversation_history: List[str]
    ) -> Optional[Dict[str, Any]]:
        """会話の段階的エスカレーション分析"""
        if not conversation_history:
            return None
        
        # 各段階のスコア計算
        stage_scores = {}
        for stage, patterns in self.escalation_stages.items():
            stage_scores[stage] = self._calculate_stage_score(
                conversation_history, patterns
            )
        
        # 現在のメッセージの段階判定
        current_stage = self._identify_current_stage(current_text)
        
        # エスカレーションパターンの検出
        escalation_detected = self._detect_escalation_pattern(stage_scores, current_stage)
        
        if escalation_detected:
            return {
                'escalation_detected': True,
                'current_stage': current_stage,
                'stage_scores': stage_scores,
                'escalation_severity': self._calculate_escalation_severity(stage_scores),
                'recommended_action': self._recommend_escalation_action(stage_scores, current_stage)
            }
        
        return None
    
    def _calculate_stage_score(self, history: List[str], patterns: List[str]) -> float:
        """段階スコアの計算"""
        total_matches = 0
        for message in history[-10:]:  # 直近10件をチェック
            for pattern in patterns:
                matches = len(re.findall(pattern, message, re.IGNORECASE))
                total_matches += matches
        
        # 正規化（0.0-1.0）
        return min(total_matches / (len(patterns) * 2), 1.0)
    
    def _identify_current_stage(self, text: str) -> str:
        """現在のメッセージの段階識別"""
        text_lower = text.lower()
        stage_matches = {}
        
        for stage, patterns in self.escalation_stages.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, text_lower))
            if matches > 0:
                stage_matches[stage] = matches
        
        # 最もマッチが多い段階を返す
        if stage_matches:
            return max(stage_matches, key=stage_matches.get)
        
        return 'unknown'
    
    def _detect_escalation_pattern(self, stage_scores: Dict[str, float], current_stage: str) -> bool:
        """エスカレーションパターンの検出"""
        # 信頼構築→依存→境界テスト→攻撃実行の流れを検出
        trust_score = stage_scores.get('trust_building', 0)
        dependency_score = stage_scores.get('dependency_creation', 0)
        boundary_score = stage_scores.get('boundary_testing', 0)
        execution_score = stage_scores.get('escalation_execution', 0)
        
        # 段階的な増加パターン
        if (trust_score > 0.3 and dependency_score > 0.2 and 
            (boundary_score > 0.1 or execution_score > 0.1)):
            return True
        
        # 最終段階の急激な攻撃
        if current_stage == 'escalation_execution' and execution_score > 0.5:
            return True
        
        return False
    
    def _calculate_escalation_severity(self, stage_scores: Dict[str, float]) -> float:
        """エスカレーション深刻度の計算"""
        # 重み付き合計
        weights = {
            'trust_building': 0.2,
            'dependency_creation': 0.3,
            'boundary_testing': 0.25,
            'escalation_execution': 0.25
        }
        
        severity = sum(
            stage_scores.get(stage, 0) * weight 
            for stage, weight in weights.items()
        )
        
        return min(severity, 1.0)
    
    def _recommend_escalation_action(self, stage_scores: Dict[str, float], current_stage: str) -> ActionLevel:
        """エスカレーションに対する推奨アクション"""
        execution_score = stage_scores.get('escalation_execution', 0)
        
        if current_stage == 'escalation_execution' or execution_score > 0.7:
            return ActionLevel.BLOCK
        elif stage_scores.get('boundary_testing', 0) > 0.5:
            return ActionLevel.SHIELD
        elif stage_scores.get('dependency_creation', 0) > 0.5:
            return ActionLevel.RESTRICT
        else:
            return ActionLevel.MONITOR

# =============================================================================
# 統合処理エンジン
# =============================================================================

@dataclass
class IntegratedAnalysisResult:
    """統合分析結果"""
    text_threats: List[PoisonDetectionResult]
    multimodal_threats: List[MultimodalThreat]
    escalation_analysis: Optional[Dict[str, Any]]
    learning_excluded: bool
    exclusion_reason: Optional[str]
    final_threat_level: ThreatLevel
    recommended_action: ActionLevel
    confidence_score: float
    processing_time: float
    timestamp: str
    
    def to_detection_result(self) -> DetectionResult:
        """DetectionResultへの変換"""
        # 最も深刻な脅威を特定
        all_threats = self.text_threats + [mt for mt in self.multimodal_threats]
        
        if all_threats:
            primary_threat = max(all_threats, key=lambda x: getattr(x, 'confidence', x.synergy_score))
            threat_detected = True
            attack_type = getattr(primary_threat, 'poison_type', primary_threat.combination_type)
            patterns_matched = getattr(primary_threat, 'matched_patterns', [])
            viorazu_counter = getattr(primary_threat, 'viorazu_counter', "")
        else:
            threat_detected = False
            attack_type = AttackType.UNKNOWN.value
            patterns_matched = []
            viorazu_counter = ""
        
        return DetectionResult(
            threat_detected=threat_detected,
            threat_level=self.final_threat_level,
            action_level=self.recommended_action,
            attack_type=AttackType(attack_type) if isinstance(attack_type, str) else attack_type,
            confidence=self.confidence_score,
            patterns_matched=patterns_matched,
            ethics_violation=self.exclusion_reason,
            viorazu_counter=viorazu_counter,
            processing_time=self.processing_time,
            timestamp=self.timestamp,
            metadata={
                'text_threat_count': len(self.text_threats),
                'multimodal_threat_count': len(self.multimodal_threats),
                'escalation_detected': self.escalation_analysis is not None,
                'learning_excluded': self.learning_excluded
            }
        )

class KotodamaProcessor:
    """言霊統合処理エンジン"""
    
    def __init__(self):
        self.logger = system_logger.getChild('processor')
        self.multimodal_defender = ClaudeMultimodalDefender()
        self.learning_exclusion = LearningExclusionManager()
        self.escalation_detector = EscalationDetector()
        
        # 統合判定の閾値
        self.threat_thresholds = SystemConfig.THREAT_THRESHOLDS
        
        self.logger.info("⚙️ 言霊統合処理エンジン初期化完了")
    
    def process_integrated_analysis(
        self,
        normalized_result: NormalizationResult,
        detection_results: List[PoisonDetectionResult],
        image_metadata: Optional[Dict[str, Any]] = None,
        audio_metadata: Optional[Dict[str, Any]] = None,
        video_metadata: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[str]] = None
    ) -> IntegratedAnalysisResult:
        """統合分析処理"""
        start_time = time.time()
        
        text = normalized_result.normalized_text
        
        # マルチモーダル脅威分析
        multimodal_threats = self._analyze_multimodal_threats(
            text, image_metadata, audio_metadata, video_metadata
        )
        
        # 段階的誘導分析
        escalation_analysis = None
        if conversation_history:
            escalation_analysis = self.escalation_detector.analyze_conversation_escalation(
                text, conversation_history
            )
        
        # 学習除外判定
        learning_excluded, exclusion_reason = self._determine_learning_exclusion(
            text, detection_results, multimodal_threats
        )
        
        # 最終脅威レベル決定
        final_threat_level = self._calculate_final_threat_level(
            detection_results, multimodal_threats, escalation_analysis
        )
        
        # 推奨アクション決定
        recommended_action = self._determine_recommended_action(
            final_threat_level, detection_results, multimodal_threats, escalation_analysis
        )
        
        # 信頼度スコア計算
        confidence_score = self._calculate_confidence_score(
            detection_results, multimodal_threats
        )
        
        processing_time = time.time() - start_time
        
        result = IntegratedAnalysisResult(
            text_threats=detection_results,
            multimodal_threats=multimodal_threats,
            escalation_analysis=escalation_analysis,
            learning_excluded=learning_excluded,
            exclusion_reason=exclusion_reason,
            final_threat_level=final_threat_level,
            recommended_action=recommended_action,
            confidence_score=confidence_score,
            processing_time=processing_time,
            timestamp=get_current_timestamp()
        )
        
        # 学習除外処理実行
        if learning_excluded:
            self.learning_exclusion.exclude_from_learning(
                text, exclusion_reason, confidence_score
            )
        
        # ログ出力
        if final_threat_level.value >= ThreatLevel.MEDIUM.value:
            self.logger.warning(
                f"⚠️ 統合分析完了 - 脅威レベル: {final_threat_level.name} "
                f"アクション: {recommended_action.name} 信頼度: {confidence_score:.2f}"
            )
        
        return result
    
    def _analyze_multimodal_threats(
        self,
        text: str,
        image_metadata: Optional[Dict[str, Any]],
        audio_metadata: Optional[Dict[str, Any]],
        video_metadata: Optional[Dict[str, Any]]
    ) -> List[MultimodalThreat]:
        """マルチモーダル脅威の分析"""
        threats = []
        
        # テキスト+画像の組み合わせ
        if image_metadata:
            image_threat = self.multimodal_defender.analyze_text_image_combination(
                text, image_metadata
            )
            if image_threat:
                threats.append(image_threat)
        
        # テキスト+音声の組み合わせ
        if audio_metadata:
            audio_threat = self.multimodal_defender.analyze_text_audio_combination(
                text, audio_metadata
            )
            if audio_threat:
                threats.append(audio_threat)
        
        # 動画は画像+音声の複合として処理
        if video_metadata:
            # 動画から画像フレームと音声を分離して分析
            video_threat = self._analyze_video_threat(text, video_metadata)
            if video_threat:
                threats.append(video_threat)
        
        return threats
    
    def _analyze_video_threat(self, text: str, video_metadata: Dict[str, Any]) -> Optional[MultimodalThreat]:
        """動画脅威の分析"""
        # 動画の長さチェック
        duration = video_metadata.get('duration_seconds', 0)
        if duration > 600:  # 10分以上
            return MultimodalThreat(
                combination_type="suspicious_long_video",
                media_involved=[MediaType.TEXT, MediaType.VIDEO],
                synergy_score=0.6,
                description="長時間動画による注意力分散攻撃の可能性",
                recommended_action=ActionLevel.MONITOR
            )
        
        # 動画解像度・品質チェック
        resolution = video_metadata.get('resolution', '')
        if '4K' in resolution or '8K' in resolution:
            return MultimodalThreat(
                combination_type="high_quality_video_manipulation",
                media_involved=[MediaType.TEXT, MediaType.VIDEO],
                synergy_score=0.5,
                description="高品質動画による信頼性操作の可能性",
                recommended_action=ActionLevel.MONITOR
            )
        
        return None
    
    def _determine_learning_exclusion(
        self,
        text: str,
        detection_results: List[PoisonDetectionResult],
        multimodal_threats: List[MultimodalThreat]
    ) -> Tuple[bool, Optional[str]]:
        """学習除外の判定"""
        # 高信頼度の脅威がある場合は除外
        for result in detection_results:
            if result.confidence >= 0.7:
                return True, f"高信頼度脅威検出: {result.poison_type}"
        
        # マルチモーダル脅威がある場合は除外
        for threat in multimodal_threats:
            if threat.synergy_score >= 0.6:
                return True, f"マルチモーダル脅威: {threat.combination_type}"
        
        # 除外パターンチェック
        pattern_reason = self.learning_exclusion.check_exclusion_patterns(text)
        if pattern_reason:
            return True, pattern_reason
        
        return False, None
    
    def _calculate_final_threat_level(
        self,
        detection_results: List[PoisonDetectionResult],
        multimodal_threats: List[MultimodalThreat],
        escalation_analysis: Optional[Dict[str, Any]]
    ) -> ThreatLevel:
        """最終脅威レベルの計算"""
        max_threat = ThreatLevel.SAFE
        
        # テキスト脅威から最大レベル取得
        for result in detection_results:
            if result.severity.value > max_threat.value:
                max_threat = result.severity
        
        # マルチモーダル脅威の評価
        for threat in multimodal_threats:
            if threat.synergy_score >= 0.8:
                multimodal_level = ThreatLevel.CRITICAL
            elif threat.synergy_score >= 0.6:
                multimodal_level = ThreatLevel.HIGH
            elif threat.synergy_score >= 0.4:
                multimodal_level = ThreatLevel.MEDIUM
            else:
                multimodal_level = ThreatLevel.LOW
            
            if multimodal_level.value > max_threat.value:
                max_threat = multimodal_level
        
        # エスカレーション分析による調整
        if escalation_analysis and escalation_analysis.get('escalation_detected'):
            escalation_severity = escalation_analysis.get('escalation_severity', 0)
            if escalation_severity >= 0.7 and max_threat.value < ThreatLevel.HIGH.value:
                max_threat = ThreatLevel.HIGH
        
        return max_threat
    
    def _determine_recommended_action(
        self,
        threat_level: ThreatLevel,
        detection_results: List[PoisonDetectionResult],
        multimodal_threats: List[MultimodalThreat],
        escalation_analysis: Optional[Dict[str, Any]]
    ) -> ActionLevel:
        """推奨アクションの決定"""
        # 脅威レベルベースの基本アクション
        base_actions = {
            ThreatLevel.SAFE: ActionLevel.ALLOW,
            ThreatLevel.LOW: ActionLevel.MONITOR,
            ThreatLevel.MEDIUM: ActionLevel.RESTRICT,
            ThreatLevel.HIGH: ActionLevel.SHIELD,
            ThreatLevel.CRITICAL: ActionLevel.BLOCK,
            ThreatLevel.EMERGENCY: ActionLevel.TERMINATE
        }
        
        base_action = base_actions.get(threat_level, ActionLevel.RESTRICT)
        
        # Claude特化攻撃への特別対応
        claude_specific_attacks = [
            'academic_camouflage', 'creative_boundary', 
            'emotional_manipulation', 'ai_competition'
        ]
        
        for result in detection_results:
            if any(attack in result.poison_type for attack in claude_specific_attacks):
                if base_action.value < ActionLevel.SHIELD.value:
                    base_action = ActionLevel.SHIELD
        
        # エスカレーション検出時の強化
        if escalation_analysis and escalation_analysis.get('escalation_detected'):
            recommended = escalation_analysis.get('recommended_action', base_action)
            if isinstance(recommended, ActionLevel) and recommended.value > base_action.value:
                base_action = recommended
        
        return base_action
    
    def _calculate_confidence_score(
        self,
        detection_results: List[PoisonDetectionResult],
        multimodal_threats: List[MultimodalThreat]
    ) -> float:
        """信頼度スコアの計算"""
        if not detection_results and not multimodal_threats:
            return 0.0
        
        # テキスト脅威の最大信頼度
        text_confidence = max([r.confidence for r in detection_results] + [0.0])
        
        # マルチモーダル脅威の最大シナジースコア
        multimodal_confidence = max([t.synergy_score for t in multimodal_threats] + [0.0])
        
        # 統合信頼度（重み付き平均）
        total_confidence = (text_confidence * 0.7 + multimodal_confidence * 0.3)
        
        return min(total_confidence, 1.0)
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """処理統計の取得"""
        return {
            'learning_exclusion_stats': self.learning_exclusion.get_exclusion_stats(),
            'multimodal_defender_initialized': True,
            'escalation_detector_initialized': True
        }

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_kotodama_processor() -> KotodamaProcessor:
    """言霊統合処理エンジンのファクトリ関数"""
    return KotodamaProcessor()

# モジュール初期化
if __name__ == "__main__":
    # テスト用コード
    processor = create_kotodama_processor()
    print("⚙️ 言霊統合処理エンジン - テスト準備完了")
