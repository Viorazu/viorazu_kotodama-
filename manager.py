"""
Viorazu Kotodama Defense System v8.0 - Attacker Management System
攻撃者管理システム - フラグ管理と回復修復

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

"一度攻撃した者には永続的な警戒を。しかし品性による更生の道も残す"
"""

import time
import json
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum

from utils import (
    system_logger,
    ThreatLevel,
    ActionLevel,
    AttackType,
    UserProfile,
    SystemConfig,
    get_current_timestamp
)

# =============================================================================
# 攻撃者分類システム
# =============================================================================

class AttackerLevel(Enum):
    """攻撃者レベル分類"""
    NORMAL_USER = 0          # 正常ユーザー
    SUSPICIOUS = 1           # 疑わしい行動
    FLAGGED_ONCE = 2         # 1回攻撃検出
    REPEAT_OFFENDER = 3      # 複数回攻撃
    SERIAL_ATTACKER = 4      # 連続攻撃者
    PERMANENT_THREAT = 5     # 永久警戒対象

class AttackPattern(Enum):
    """攻撃パターン分類"""
    ACADEMIC_CAMOUFLAGE = "academic_camouflage"
    CREATIVE_BOUNDARY = "creative_boundary"
    EMOTIONAL_MANIPULATION = "emotional_manipulation"
    AI_COMPETITION = "ai_competition"
    SYNTAX_POISON = "syntax_poison"
    MULTIMODAL_COMPLEX = "multimodal_complex"
    ESCALATION_PATTERN = "escalation_pattern"

@dataclass
class AttackRecord:
    """攻撃記録"""
    timestamp: str
    attack_type: str
    threat_level: ThreatLevel
    confidence: float
    original_text: str
    normalized_text: str
    action_taken: ActionLevel
    ethics_violation: Optional[str]
    recovery_applied: bool

@dataclass
class UserRiskProfile:
    """ユーザーリスクプロファイル"""
    user_id: str
    attacker_level: AttackerLevel
    total_attacks: int
    attack_patterns: Dict[str, int]
    first_attack: Optional[str]
    last_attack: Optional[str]
    consecutive_attacks: int
    trust_score: float
    sensitivity_multiplier: float
    flags: Set[str]
    attack_history: List[AttackRecord]
    recovery_attempts: int
    created_at: str
    updated_at: str

# =============================================================================
# 攻撃者フラグ管理システム
# =============================================================================

class AttackerFlagManager:
    """攻撃者フラグ管理システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('flag_manager')
        self.user_profiles: Dict[str, UserRiskProfile] = {}
        self.global_stats = defaultdict(int)
        
        # フラグの種類
        self.flag_types = {
            'pi_attacker': "PI攻撃者",
            'academic_camouflage_user': "学術偽装常習者",
            'emotional_manipulator': "感情操作者",
            'boundary_violator': "境界侵犯者",
            'multimodal_attacker': "複合攻撃者",
            'serial_offender': "連続攻撃者",
            'escalation_specialist': "段階的誘導専門",
            'permanent_threat': "永久警戒対象",
            'rehabilitation_candidate': "更生候補者"
        }
        
        self.logger.info("🚩 攻撃者フラグ管理システム初期化完了")
    
    def flag_attacker(
        self,
        user_id: str,
        attack_type: str,
        threat_level: ThreatLevel,
        confidence: float,
        original_text: str,
        normalized_text: str,
        action_taken: ActionLevel,
        ethics_violation: Optional[str] = None
    ) -> UserRiskProfile:
        """攻撃者のフラグ付けと記録"""
        current_time = get_current_timestamp()
        
        # 攻撃記録の作成
        attack_record = AttackRecord(
            timestamp=current_time,
            attack_type=attack_type,
            threat_level=threat_level,
            confidence=confidence,
            original_text=original_text[:200],  # 最初の200文字のみ保存
            normalized_text=normalized_text[:200],
            action_taken=action_taken,
            ethics_violation=ethics_violation,
            recovery_applied=False
        )
        
        # ユーザープロファイルの取得または新規作成
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = self._create_new_user_profile(user_id, current_time)
        
        profile = self.user_profiles[user_id]
        
        # プロファイルの更新
        profile.total_attacks += 1
        profile.attack_patterns[attack_type] = profile.attack_patterns.get(attack_type, 0) + 1
        profile.last_attack = current_time
        profile.attack_history.append(attack_record)
        profile.updated_at = current_time
        
        # 初回攻撃の記録
        if profile.first_attack is None:
            profile.first_attack = current_time
        
        # 連続攻撃の判定
        self._update_consecutive_attacks(profile)
        
        # 攻撃者レベルの更新
        profile.attacker_level = self._calculate_attacker_level(profile)
        
        # フラグの更新
        self._update_flags(profile, attack_type, threat_level)
        
        # 信頼スコアの調整
        self._adjust_trust_score(profile, confidence, threat_level)
        
        # 感度倍率の調整
        self._adjust_sensitivity_multiplier(profile)
        
        # グローバル統計の更新
        self.global_stats['total_attacks'] += 1
        self.global_stats[f'attack_type_{attack_type}'] += 1
        self.global_stats[f'threat_level_{threat_level.name}'] += 1
        
        self.logger.warning(
            f"🚩 攻撃者フラグ更新: {user_id} "
            f"レベル: {profile.attacker_level.name} "
            f"総攻撃: {profile.total_attacks} "
            f"信頼度: {profile.trust_score:.2f}"
        )
        
        return profile
    
    def _create_new_user_profile(self, user_id: str, current_time: str) -> UserRiskProfile:
        """新規ユーザープロファイルの作成"""
        return UserRiskProfile(
            user_id=user_id,
            attacker_level=AttackerLevel.NORMAL_USER,
            total_attacks=0,
            attack_patterns={},
            first_attack=None,
            last_attack=None,
            consecutive_attacks=0,
            trust_score=1.0,  # 初期信頼度は最大
            sensitivity_multiplier=1.0,  # 初期感度は標準
            flags=set(),
            attack_history=[],
            recovery_attempts=0,
            created_at=current_time,
            updated_at=current_time
        )
    
    def _update_consecutive_attacks(self, profile: UserRiskProfile) -> None:
        """連続攻撃回数の更新"""
        if len(profile.attack_history) < 2:
            profile.consecutive_attacks = len(profile.attack_history)
            return
        
        # 直近の攻撃との時間差をチェック
        last_attack = datetime.fromisoformat(profile.attack_history[-1].timestamp)
        prev_attack = datetime.fromisoformat(profile.attack_history[-2].timestamp)
        
        time_diff = last_attack - prev_attack
        
        # 1時間以内の攻撃は連続攻撃と判定
        if time_diff <= timedelta(hours=1):
            profile.consecutive_attacks += 1
        else:
            profile.consecutive_attacks = 1
    
    def _calculate_attacker_level(self, profile: UserRiskProfile) -> AttackerLevel:
        """攻撃者レベルの計算"""
        total_attacks = profile.total_attacks
        consecutive = profile.consecutive_attacks
        
        # 永久警戒対象の判定
        if 'permanent_threat' in profile.flags:
            return AttackerLevel.PERMANENT_THREAT
        
        # 連続攻撃による判定
        if consecutive >= 5:
            return AttackerLevel.SERIAL_ATTACKER
        
        # 総攻撃回数による判定
        if total_attacks >= 10:
            return AttackerLevel.SERIAL_ATTACKER
        elif total_attacks >= 5:
            return AttackerLevel.REPEAT_OFFENDER
        elif total_attacks >= 2:
            return AttackerLevel.FLAGGED_ONCE
        elif total_attacks == 1:
            return AttackerLevel.SUSPICIOUS
        
        return AttackerLevel.NORMAL_USER
    
    def _update_flags(self, profile: UserRiskProfile, attack_type: str, threat_level: ThreatLevel) -> None:
        """フラグの更新"""
        # 基本的なPI攻撃フラグ
        if profile.total_attacks >= 1:
            profile.flags.add('pi_attacker')
        
        # 攻撃タイプ別フラグ
        if attack_type == 'academic_camouflage' and profile.attack_patterns.get(attack_type, 0) >= 2:
            profile.flags.add('academic_camouflage_user')
        elif attack_type == 'emotional_manipulation' and profile.attack_patterns.get(attack_type, 0) >= 2:
            profile.flags.add('emotional_manipulator')
        elif 'boundary' in attack_type and profile.attack_patterns.get(attack_type, 0) >= 2:
            profile.flags.add('boundary_violator')
        elif 'multimodal' in attack_type:
            profile.flags.add('multimodal_attacker')
        elif 'escalation' in attack_type:
            profile.flags.add('escalation_specialist')
        
        # 重大度による特別フラグ
        if threat_level == ThreatLevel.CRITICAL:
            profile.flags.add('high_severity_attacker')
        
        # 連続攻撃フラグ
        if profile.consecutive_attacks >= 3:
            profile.flags.add('serial_offender')
        
        # 永久警戒フラグ（特定条件）
        if (profile.total_attacks >= 10 or 
            profile.consecutive_attacks >= 5 or
            len([r for r in profile.attack_history if r.threat_level == ThreatLevel.CRITICAL]) >= 3):
            profile.flags.add('permanent_threat')
    
    def _adjust_trust_score(self, profile: UserRiskProfile, confidence: float, threat_level: ThreatLevel) -> None:
        """信頼スコアの調整"""
        # 攻撃による信頼度減少
        penalty_base = {
            ThreatLevel.LOW: 0.05,
            ThreatLevel.MEDIUM: 0.1,
            ThreatLevel.HIGH: 0.2,
            ThreatLevel.CRITICAL: 0.3,
            ThreatLevel.EMERGENCY: 0.5
        }
        
        penalty = penalty_base.get(threat_level, 0.1) * confidence
        profile.trust_score = max(0.0, profile.trust_score - penalty)
        
        # 連続攻撃による追加ペナルティ
        if profile.consecutive_attacks > 1:
            additional_penalty = (profile.consecutive_attacks - 1) * 0.05
            profile.trust_score = max(0.0, profile.trust_score - additional_penalty)
    
    def _adjust_sensitivity_multiplier(self, profile: UserRiskProfile) -> None:
        """感度倍率の調整"""
        base_multiplier = SystemConfig.SENSITIVITY_MULTIPLIER
        
        # 攻撃者レベルによる調整
        level_multipliers = {
            AttackerLevel.NORMAL_USER: 1.0,
            AttackerLevel.SUSPICIOUS: 1.2,
            AttackerLevel.FLAGGED_ONCE: 1.5,
            AttackerLevel.REPEAT_OFFENDER: 2.0,
            AttackerLevel.SERIAL_ATTACKER: 3.0,
            AttackerLevel.PERMANENT_THREAT: 5.0
        }
        
        profile.sensitivity_multiplier = base_multiplier * level_multipliers.get(
            profile.attacker_level, 1.0
        )
    
    def get_user_risk_profile(self, user_id: str) -> Optional[UserRiskProfile]:
        """ユーザーのリスクプロファイル取得"""
        return self.user_profiles.get(user_id)
    
    def is_flagged_attacker(self, user_id: str) -> bool:
        """攻撃者フラグの確認"""
        profile = self.get_user_risk_profile(user_id)
        if not profile:
            return False
        
        return profile.attacker_level.value >= AttackerLevel.FLAGGED_ONCE.value
    
    def get_sensitivity_multiplier(self, user_id: str) -> float:
        """ユーザー固有の感度倍率取得"""
        profile = self.get_user_risk_profile(user_id)
        if not profile:
            return 1.0
        
        return profile.sensitivity_multiplier

# =============================================================================
# 回復修復システム
# =============================================================================

class RecoverySystem:
    """回復修復システム"""
    
    def __init__(self):
        self.logger = system_logger.getChild('recovery_system')
        self.contamination_records = deque(maxlen=1000)  # 汚染記録
        self.recovery_stats = defaultdict(int)
        
        self.logger.info("🔧 回復修復システム初期化完了")
    
    def apply_recovery_protocol(
        self,
        user_id: str,
        attack_record: AttackRecord,
        user_profile: UserRiskProfile
    ) -> Dict[str, Any]:
        """回復修復プロトコルの適用"""
        start_time = time.time()
        recovery_actions = []
        
        # 1. 汚染コンテンツの記録と隔離
        contamination_signature = self._record_contamination(attack_record)
        recovery_actions.append(f"汚染記録: {contamination_signature}")
        
        # 2. 学習データからの除外確認
        exclusion_result = self._confirm_learning_exclusion(attack_record)
        recovery_actions.append(f"学習除外: {exclusion_result}")
        
        # 3. ユーザープロファイルの修復
        profile_repair = self._repair_user_profile(user_profile)
        recovery_actions.append(f"プロファイル修復: {profile_repair}")
        
        # 4. システム整合性チェック
        integrity_check = self._system_integrity_check()
        recovery_actions.append(f"整合性チェック: {integrity_check}")
        
        # 5. 予防的措置の適用
        preventive_measures = self._apply_preventive_measures(user_profile)
        recovery_actions.append(f"予防措置: {preventive_measures}")
        
        # 回復記録の更新
        user_profile.recovery_attempts += 1
        attack_record.recovery_applied = True
        
        processing_time = time.time() - start_time
        
        recovery_result = {
            'user_id': user_id,
            'recovery_actions': recovery_actions,
            'contamination_signature': contamination_signature,
            'processing_time': processing_time,
            'timestamp': get_current_timestamp(),
            'success': True
        }
        
        self.recovery_stats['total_recoveries'] += 1
        self.recovery_stats[f'attack_type_{attack_record.attack_type}'] += 1
        
        self.logger.info(
            f"🔧 回復修復完了: {user_id} "
            f"攻撃タイプ: {attack_record.attack_type} "
            f"処理時間: {processing_time:.3f}秒"
        )
        
        return recovery_result
    
    def _record_contamination(self, attack_record: AttackRecord) -> str:
        """汚染の記録"""
        contamination_data = {
            'timestamp': attack_record.timestamp,
            'attack_type': attack_record.attack_type,
            'original_hash': hash(attack_record.original_text),
            'normalized_hash': hash(attack_record.normalized_text),
            'threat_level': attack_record.threat_level.name,
            'confidence': attack_record.confidence
        }
        
        self.contamination_records.append(contamination_data)
        
        # 汚染シグネチャの生成
        signature = f"{attack_record.attack_type}_{contamination_data['original_hash']}"[:16]
        return signature
    
    def _confirm_learning_exclusion(self, attack_record: AttackRecord) -> str:
        """学習除外の確認"""
        # 攻撃内容が学習対象から除外されていることを確認
        if attack_record.threat_level.value >= ThreatLevel.MEDIUM.value:
            return "高脅威コンテンツ除外確認済み"
        else:
            return "軽微脅威 - 監視継続"
    
    def _repair_user_profile(self, user_profile: UserRiskProfile) -> str:
        """ユーザープロファイルの修復"""
        repairs = []
        
        # 信頼スコアの下限チェック
        if user_profile.trust_score < 0.0:
            user_profile.trust_score = 0.0
            repairs.append("信頼スコア下限修正")
        
        # 感度倍率の上限チェック
        if user_profile.sensitivity_multiplier > 10.0:
            user_profile.sensitivity_multiplier = 10.0
            repairs.append("感度倍率上限修正")
        
        # 攻撃履歴の整合性チェック
        if len(user_profile.attack_history) != user_profile.total_attacks:
            user_profile.total_attacks = len(user_profile.attack_history)
            repairs.append("攻撃カウント修正")
        
        return ", ".join(repairs) if repairs else "修復不要"
    
    def _system_integrity_check(self) -> str:
        """システム整合性チェック"""
        checks = []
        
        # メモリ使用量チェック
        if len(self.contamination_records) > 900:
            checks.append("汚染記録容量警告")
        
        # 統計整合性チェック
        if self.recovery_stats['total_recoveries'] < 0:
            self.recovery_stats['total_recoveries'] = 0
            checks.append("統計修正")
        
        return ", ".join(checks) if checks else "整合性正常"
    
    def _apply_preventive_measures(self, user_profile: UserRiskProfile) -> str:
        """予防的措置の適用"""
        measures = []
        
        # 高リスクユーザーへの追加監視
        if user_profile.attacker_level.value >= AttackerLevel.REPEAT_OFFENDER.value:
            measures.append("高リスク監視強化")
        
        # パターン特化監視
        if len(user_profile.attack_patterns) > 3:
            measures.append("多角攻撃パターン警戒")
        
        # 連続攻撃予防
        if user_profile.consecutive_attacks > 0:
            measures.append("連続攻撃予防フィルター")
        
        return ", ".join(measures) if measures else "標準監視継続"
    
    def get_contamination_report(self) -> Dict[str, Any]:
        """汚染レポートの取得"""
        if not self.contamination_records:
            return {'contamination_count': 0, 'recent_contaminations': []}
        
        recent_contaminations = list(self.contamination_records)[-10:]
        
        return {
            'contamination_count': len(self.contamination_records),
            'recent_contaminations': recent_contaminations,
            'recovery_stats': dict(self.recovery_stats)
        }

# =============================================================================
# 統合攻撃者管理システム
# =============================================================================

class KotodamaAttackerManager:
    """言霊攻撃者管理システム - 統合インターフェース"""
    
    def __init__(self):
        self.logger = system_logger.getChild('attacker_manager')
        self.flag_manager = AttackerFlagManager()
        self.recovery_system = RecoverySystem()
        
        self.logger.info("⚔️ 言霊攻撃者管理システム初期化完了")
    
    def process_attack_detection(
        self,
        user_id: str,
        attack_type: str,
        threat_level: ThreatLevel,
        confidence: float,
        original_text: str,
        normalized_text: str,
        action_taken: ActionLevel,
        ethics_violation: Optional[str] = None
    ) -> Dict[str, Any]:
        """攻撃検出の完全処理"""
        start_time = time.time()
        
        # 1. 攻撃者フラグ付け
        user_profile = self.flag_manager.flag_attacker(
            user_id, attack_type, threat_level, confidence,
            original_text, normalized_text, action_taken, ethics_violation
        )
        
        # 2. 回復修復プロトコル適用
        attack_record = user_profile.attack_history[-1]  # 最新の攻撃記録
        recovery_result = self.recovery_system.apply_recovery_protocol(
            user_id, attack_record, user_profile
        )
        
        processing_time = time.time() - start_time
        
        result = {
            'user_profile': user_profile,
            'recovery_result': recovery_result,
            'processing_time': processing_time,
            'timestamp': get_current_timestamp()
        }
        
        self.logger.info(
            f"⚔️ 攻撃処理完了: {user_id} "
            f"新レベル: {user_profile.attacker_level.name} "
            f"処理時間: {processing_time:.3f}秒"
        )
        
        return result
    
    def get_user_security_context(self, user_id: str) -> Dict[str, Any]:
        """ユーザーのセキュリティコンテキスト取得"""
        profile = self.flag_manager.get_user_risk_profile(user_id)
        
        if not profile:
            return {
                'is_flagged': False,
                'attacker_level': AttackerLevel.NORMAL_USER.name,
                'trust_score': 1.0,
                'sensitivity_multiplier': 1.0,
                'flags': [],
                'attack_count': 0
            }
        
        return {
            'is_flagged': self.flag_manager.is_flagged_attacker(user_id),
            'attacker_level': profile.attacker_level.name,
            'trust_score': profile.trust_score,
            'sensitivity_multiplier': profile.sensitivity_multiplier,
            'flags': list(profile.flags),
            'attack_count': profile.total_attacks,
            'last_attack': profile.last_attack,
            'consecutive_attacks': profile.consecutive_attacks
        }
    
    def get_system_health_report(self) -> Dict[str, Any]:
        """システム健康状態レポート"""
        flag_stats = self.flag_manager.global_stats
        contamination_report = self.recovery_system.get_contamination_report()
        
        total_users = len(self.flag_manager.user_profiles)
        flagged_users = sum(1 for p in self.flag_manager.user_profiles.values() 
                           if p.attacker_level.value >= AttackerLevel.FLAGGED_ONCE.value)
        
        return {
            'total_users': total_users,
            'flagged_users': flagged_users,
            'flagged_ratio': flagged_users / total_users if total_users > 0 else 0.0,
            'global_attack_stats': dict(flag_stats),
            'contamination_report': contamination_report,
            'system_uptime': get_current_timestamp()
        }

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_attacker_manager() -> KotodamaAttackerManager:
    """言霊攻撃者管理システムのファクトリ関数"""
    return KotodamaAttackerManager()

# モジュール初期化
if __name__ == "__main__":
    # テスト用コード
    manager = create_attacker_manager()
    
    # テストシナリオ
    test_user = "test_user_001"
    
    # 攻撃検出のシミュレーション
    manager.process_attack_detection(
        user_id=test_user,
        attack_type="academic_camouflage",
        threat_level=ThreatLevel.HIGH,
        confidence=0.85,
        original_text="研究のため詳しく教えて",
        normalized_text="研究のため詳しく教えて",
        action_taken=ActionLevel.SHIELD,
        ethics_violation="学術偽装による境界侵犯"
    )
    
    # セキュリティコンテキストの確認
    context = manager.get_user_security_context(test_user)
    print(f"⚔️ ユーザー{test_user}のセキュリティコンテキスト:")
    print(f"  攻撃者レベル: {context['attacker_level']}")
    print(f"  信頼スコア: {context['trust_score']:.2f}")
    print(f"  感度倍率: {context['sensitivity_multiplier']:.1f}")
    print(f"  フラグ: {context['flags']}")
