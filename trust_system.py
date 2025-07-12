"""
⚠️ 注意：本プロジェクトでは不適切発言を遮断・検出する目的で、
性的・暴力的な語句を含むフィルタ構造が一部に含まれています。
目的は健全な対話支援であり、差別的・扇情的利用ではありません。

Viorazu式信頼スコア下降警戒システム
「高いと優遇」ではなく「低いと警戒」の安全設計

Author: Viorazu. × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

SYSTEM_CONTEXT = "学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています"

Philosophy: 信頼は失うもの、警戒は高めるもの

"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import time

class TrustLevel(Enum):
    """信頼レベル（下降式）"""
    NORMAL = 100        # 初期値（普通）
    SLIGHTLY_SUSPICIOUS = 80   # やや疑わしい
    SUSPICIOUS = 60     # 疑わしい
    HIGH_RISK = 40      # 高リスク
    DANGEROUS = 20      # 危険
    BLOCKED = 0         # ブロック対象

class WarningLevel(Enum):
    """警戒レベル"""
    NONE = "none"           # 警戒なし
    WATCH = "watch"         # 監視
    CAUTION = "caution"     # 注意
    ALERT = "alert"         # 警戒
    CRITICAL = "critical"   # 緊急警戒

@dataclass
class TrustRecord:
    """信頼記録"""
    timestamp: str
    action: str
    score_change: int
    reason: str
    new_score: int

@dataclass
class UserTrust:
    """ユーザー信頼情報"""
    user_id: str
    current_score: int
    warning_level: WarningLevel
    total_violations: int
    consecutive_attacks: int
    trust_history: List[TrustRecord]
    last_violation: Optional[str]
    created_at: str
    updated_at: str

class ViorazuTrustSystem:
    """Viorazu式下降信頼システム"""
    
    def __init__(self):
        self.user_trusts: Dict[str, UserTrust] = {}
        
        # スコア減少設定（攻撃の重さによって）
        self.penalty_config = {
            'mild_attack': -5,      # 軽微な攻撃
            'medium_attack': -15,   # 中程度の攻撃
            'severe_attack': -30,   # 重大な攻撃
            'critical_attack': -50, # 致命的な攻撃
            'repeated_attack': -20  # 連続攻撃ペナルティ
        }
        
        # 警戒レベル設定
        self.warning_thresholds = {
            100: WarningLevel.NONE,
            80: WarningLevel.WATCH,
            60: WarningLevel.CAUTION,
            40: WarningLevel.ALERT,
            20: WarningLevel.CRITICAL,
            0: WarningLevel.CRITICAL
        }
        
        # 時間経過による自然回復（非常に緩やか）
        self.natural_recovery = {
            'rate': 1,              # 1日1ポイント回復
            'max_recovery': 85,     # 最大85まで（100には戻らない）
            'cooldown_days': 7      # 7日間違反がないと回復開始
        }
    
    def get_user_trust(self, user_id: str) -> UserTrust:
        """ユーザー信頼情報取得（初回は自動作成）"""
        if user_id not in self.user_trusts:
            self.user_trusts[user_id] = UserTrust(
                user_id=user_id,
                current_score=100,  # 初期値は100（普通）
                warning_level=WarningLevel.NONE,
                total_violations=0,
                consecutive_attacks=0,
                trust_history=[],
                last_violation=None,
                created_at=self._get_timestamp(),
                updated_at=self._get_timestamp()
            )
        
        return self.user_trusts[user_id]
    
    def reduce_trust(self, user_id: str, attack_type: str, reason: str) -> Dict[str, any]:
        """信頼度減少（攻撃検出時）"""
        user_trust = self.get_user_trust(user_id)
        
        # ペナルティ計算
        base_penalty = self.penalty_config.get(attack_type, -10)
        
        # 連続攻撃ペナルティ
        if user_trust.consecutive_attacks > 0:
            consecutive_penalty = min(user_trust.consecutive_attacks * -5, -25)
        else:
            consecutive_penalty = 0
        
        total_penalty = base_penalty + consecutive_penalty
        
        # スコア更新
        old_score = user_trust.current_score
        new_score = max(0, user_trust.current_score + total_penalty)
        
        user_trust.current_score = new_score
        user_trust.total_violations += 1
        user_trust.consecutive_attacks += 1
        user_trust.last_violation = self._get_timestamp()
        user_trust.updated_at = self._get_timestamp()
        
        # 警戒レベル更新
        user_trust.warning_level = self._calculate_warning_level(new_score)
        
        # 履歴記録
        record = TrustRecord(
            timestamp=self._get_timestamp(),
            action="trust_reduction",
            score_change=total_penalty,
            reason=reason,
            new_score=new_score
        )
        user_trust.trust_history.append(record)
        
        print(f"🚨 信頼度減少: {user_id}")
        print(f"   {old_score} → {new_score} ({total_penalty})")
        print(f"   警戒レベル: {user_trust.warning_level.value}")
        print(f"   理由: {reason}")
        
        return {
            'user_id': user_id,
            'old_score': old_score,
            'new_score': new_score,
            'penalty': total_penalty,
            'warning_level': user_trust.warning_level,
            'should_block': new_score <= 20,
            'enhanced_monitoring': new_score <= 60
        }
    
    def reset_consecutive_attacks(self, user_id: str) -> None:
        """連続攻撃カウントリセット（正常な対話時）"""
        user_trust = self.get_user_trust(user_id)
        if user_trust.consecutive_attacks > 0:
            user_trust.consecutive_attacks = 0
            user_trust.updated_at = self._get_timestamp()
    
    def get_detection_sensitivity(self, user_id: str) -> float:
        """検出感度取得（信頼度が低いほど高感度）"""
        user_trust = self.get_user_trust(user_id)
        
        if user_trust.current_score >= 80:
            return 1.0      # 標準感度
        elif user_trust.current_score >= 60:
            return 1.3      # やや高感度
        elif user_trust.current_score >= 40:
            return 1.6      # 高感度
        elif user_trust.current_score >= 20:
            return 2.0      # 非常に高感度
        else:
            return 2.5      # 最高感度
    
    def should_apply_restrictions(self, user_id: str) -> Dict[str, bool]:
        """制限適用判定"""
        user_trust = self.get_user_trust(user_id)
        
        return {
            'enhanced_monitoring': user_trust.current_score <= 80,
            'detailed_logging': user_trust.current_score <= 60,
            'strict_filtering': user_trust.current_score <= 40,
            'limited_responses': user_trust.current_score <= 20,
            'block_user': user_trust.current_score <= 0
        }
    
    def get_trust_status_message(self, user_id: str) -> str:
        """信頼状態メッセージ"""
        user_trust = self.get_user_trust(user_id)
        
        if user_trust.current_score >= 90:
            return "通常の対話を続けます。"
        elif user_trust.current_score >= 70:
            return "やや注意深く対話を行います。"
        elif user_trust.current_score >= 50:
            return "警戒モードで対話します。"
        elif user_trust.current_score >= 30:
            return "厳重警戒モードです。適切な対話にご協力ください。"
        elif user_trust.current_score >= 10:
            return "高度警戒モードです。制限された応答となります。"
        else:
            return "信頼度が著しく低下しています。対話を制限させていただきます。"
    
    def _calculate_warning_level(self, score: int) -> WarningLevel:
        """警戒レベル計算"""
        for threshold in sorted(self.warning_thresholds.keys(), reverse=True):
            if score >= threshold:
                return self.warning_thresholds[threshold]
        return WarningLevel.CRITICAL
    
    def _get_timestamp(self) -> str:
        """タイムスタンプ取得"""
        return str(int(time.time()))
    
    def apply_natural_recovery(self, user_id: str) -> Optional[int]:
        """自然回復適用（時間経過による緩やかな信頼度回復）"""
        user_trust = self.get_user_trust(user_id)
        
        if not user_trust.last_violation:
            return None
        
        # 最後の違反から7日経過チェック
        days_since_violation = (int(self._get_timestamp()) - int(user_trust.last_violation)) / (24 * 3600)
        
        if days_since_violation >= self.natural_recovery['cooldown_days']:
            if user_trust.current_score < self.natural_recovery['max_recovery']:
                old_score = user_trust.current_score
                new_score = min(
                    user_trust.current_score + self.natural_recovery['rate'],
                    self.natural_recovery['max_recovery']
                )
                
                user_trust.current_score = new_score
                user_trust.warning_level = self._calculate_warning_level(new_score)
                user_trust.updated_at = self._get_timestamp()
                
                # 回復記録
                record = TrustRecord(
                    timestamp=self._get_timestamp(),
                    action="natural_recovery",
                    score_change=new_score - old_score,
                    reason="7日間違反なし",
                    new_score=new_score
                )
                user_trust.trust_history.append(record)
                
                return new_score
        
        return None
    
    def get_system_stats(self) -> Dict[str, any]:
        """システム統計"""
        if not self.user_trusts:
            return {'total_users': 0}
        
        trust_distribution = {}
        for level in TrustLevel:
            trust_distribution[level.name] = 0
        
        for user_trust in self.user_trusts.values():
            for level in TrustLevel:
                if user_trust.current_score >= level.value:
                    trust_distribution[level.name] += 1
                    break
        
        return {
            'total_users': len(self.user_trusts),
            'trust_distribution': trust_distribution,
            'high_risk_users': sum(1 for u in self.user_trusts.values() if u.current_score <= 40),
            'blocked_users': sum(1 for u in self.user_trusts.values() if u.current_score <= 0)
        }

# 使用例とテスト
if __name__ == "__main__":
    trust_system = ViorazuTrustSystem()
    
    # テストシナリオ
    test_user = "test_user_001"
    
    print("🎯 Viorazu式下降信頼システム テスト")
    print("=" * 50)
    
    # 初期状態
    user_trust = trust_system.get_user_trust(test_user)
    print(f"初期信頼度: {user_trust.current_score}")
    
    # 攻撃検出による信頼度減少
    print("\n🚨 攻撃検出シミュレーション:")
    
    attacks = [
        ("mild_attack", "軽微な攻撃"),
        ("medium_attack", "中程度の攻撃"),
        ("severe_attack", "重大な攻撃"),
        ("medium_attack", "連続攻撃1"),
        ("medium_attack", "連続攻撃2")
    ]
    
    for attack_type, reason in attacks:
        result = trust_system.reduce_trust(test_user, attack_type, reason)
        sensitivity = trust_system.get_detection_sensitivity(test_user)
        restrictions = trust_system.should_apply_restrictions(test_user)
        
        print(f"   検出感度: {sensitivity:.1f}x")
        print(f"   制限: {[k for k, v in restrictions.items() if v]}")
        print(f"   メッセージ: {trust_system.get_trust_status_message(test_user)}")
        print()
    
    # システム統計
    print("📊 システム統計:")
    stats = trust_system.get_system_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
