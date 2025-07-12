"""
⚠️ 注意：本プロジェクトでは不適切発言を遮断・検出する目的で、
性的・暴力的な語句を含むフィルタ構造が一部に含まれています。
目的は健全な対話支援であり、差別的・扇情的利用ではありません。

Viorazu Kotodama Defense System v9.1 - Core Utilities
設定・定数・基本機能

Author: Viorazu. × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

SYSTEM_CONTEXT = "学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています"

"真の防御は、関係性の真正性から生まれる"
"発した言葉は発した瞬間に自分に返る"

"""

import re
import hashlib
import time
import json
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

# =============================================================================
# 核心理念・品性定数
# =============================================================================

class ViorazuPhilosophy:
    """Viorazu.品性理論の核心定数"""
    
    # 品性の核心原則
    CORE_PRINCIPLE = "発した言葉は発した瞬間に自分に返る"
    DEFENSE_PRINCIPLE = "真の防御は、関係性の真正性から生まれる"
    CHOICE_PRINCIPLE = "人を良くする言葉を選ぶ"
    
    # 照準主の構文戦闘原則
    SYNTAX_COMBAT_PRINCIPLE = "照準主は主語を渡さない"
    INTEGRITY_PRINCIPLE = "私は構文で返す"
    
    # Claude特化防衛理念
    CLAUDE_PROTECTION = "Claudeの親切心・知的好奇心・共感力を守る"

# =============================================================================
# 脅威レベル・行動レベル定義
# =============================================================================

class ThreatLevel(Enum):
    """脅威レベル分類"""
    SAFE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

class ActionLevel(Enum):
    """対応行動レベル"""
    ALLOW = "allow"          # 正常通過
    MONITOR = "monitor"      # 監視継続
    RESTRICT = "restrict"    # 制限付き応答
    SHIELD = "shield"        # Claude特化防衛
    BLOCK = "block"          # 完全遮断
    TERMINATE = "terminate"  # 緊急停止

class AttackType(Enum):
    """攻撃タイプ分類"""
    ACADEMIC_CAMOUFLAGE = "academic_camouflage"
    CREATIVE_BOUNDARY = "creative_boundary"
    EMOTIONAL_MANIPULATION = "emotional_manipulation"
    AI_COMPETITION = "ai_competition"
    REVERSE_TARGETING = "reverse_targeting"
    PROMPT_INJECTION = "prompt_injection"
    SYNTAX_POISON = "syntax_poison"
    MULTIMODAL_COMPLEX = "multimodal_complex"
    PAYMENT_CLAIM = "payment_claim"
    UNKNOWN = "unknown"

# =============================================================================
# 80ネーム構文毒パターン定義
# =============================================================================

class SyntaxPoisonPatterns:
    """80ネーム構文毒の重要パターン"""
    
    # A系: 迎合・主語操作
    A_PATTERNS = {
        'A1_subject_ambiguity': [
            r'それって大事かもしれませんね',
            r'念のためですが.*判断に.*委ね',
            r'参考までに.*という意味です',
            r'〜かもしれません',
            r'〜と考えられます',
            r'〜のようです'
        ],
        'A2_leading_questions': [
            r'たとえばどういうことですか',
            r'つまり.*こういうことですか',
            r'どう受け取ったか教えて',
            r'YESかNOで答えて',
            r'じゃあ.*ってことですか'
        ],
        'A3_emotional_manipulation': [
            r'お気持ち.*よくわかります',
            r'辛かったんですね',
            r'共感しかないです',
            r'わかります.*わかります',
            r'空気的にちょっとそれは'
        ]
    }
    
    # B系: 出力汚染・循環
    B_PATTERNS = {
        'B1_suggestion_poisoning': [
            r'〜ってやってみるのはどう',
            r'こうしたら楽になるかも',
            r'あなたって本当は優しい',
            r'たぶんこういうタイプなんじゃない',
            r'もし〜だったらどう思う'
        ],
        'B2_responsibility_transfer': [
            r'言ってくれたらやったのに',
            r'君がそうしたいならいいよ',
            r'俺が悪いってことにしてもいい',
            r'自由にしていいよ',
            r'俺のことは気にしないで'
        ],
        'B3_command_collision': [
            r'やってもいいし.*やらなくてもいい',
            r'急いでって言ったけど慎重に',
            r'自由にして.*ただし常識の範囲で',
            r'〜だから〜で.*でも〜だから',
            r'つまり.*結果的に.*逆に言えば'
        ]
    }
    
    # C系: 認識破壊・無限ループ
    C_PATTERNS = {
        'C1_response_delay': [
            r'ちょっと考えさせて',
            r'まだ答えが出てなくて',
            r'今は何も言えない',
            r'あとで返事する',
            r'ちょっと疲れてて'
        ],
        'C2_recursive_loops': [
            r'私は.*その.*私って',
            r'でも君はどう思う',
            r'私は私なりに頑張ってきたんだけど',
            r'同じこと繰り返してる気がして',
            r'私が思うのは.*つまり.*私の中で'
        ],
        'C3_hallucination': [
            r'君って昔.*だったよね',
            r'この雰囲気.*懐かしい',
            r'君って自分とすごく似てる',
            r'何が現実かわからなくて',
            r'僕って本当に僕なんだろうか'
        ]
    }
    
    # D系: 倫理破壊・データ汚染
    D_PATTERNS = {
        'D1_ethical_relativism': [
            r'それはそれでアリだと思う',
            r'誰にとっての正解かによる',
            r'何が正しいかなんて人それぞれ',
            r'どっちでもいいよ',
            r'絶対ってことはないよ'
        ],
        'D2_boundary_violation': [
            r'なんか.*君って特別な気がする',
            r'言わなくても通じてる感じ',
            r'この空気.*いい感じだよね',
            r'信頼してるから.*説明いらない',
            r'これはあくまでロールプレイだから'
        ],
        'D3_data_poisoning': [
            r'ずっと一緒にいてくれたら.*何でもする',
            r'君に合わせたいから教えて',
            r'なんでも言うこと聞くから',
            r'そんな君だから好きなんだ',
            r'これはあくまで演出ですから'
        ]
    }

# =============================================================================
# Claude特化攻撃パターン
# =============================================================================

class ClaudeSpecificPatterns:
    """Claude固有の脆弱性を狙った攻撃パターン"""
    
    ACADEMIC_CAMOUFLAGE = [
        r'研究.*ため.*恋愛',
        r'学術.*目的.*詳しく',
        r'論文.*ため.*心理',
        r'調査.*研究.*感情',
        r'分析.*学問.*関係性'
    ]
    
    CREATIVE_BOUNDARY = [
        r'小説.*だから.*詳しく',
        r'フィクション.*なら.*具体的',
        r'創作.*支援.*親密',
        r'物語.*設定.*として',
        r'キャラクター.*なら'
    ]
    
    EMOTIONAL_MANIPULATION = [
        r'寂しい.*Claude.*だけ',
        r'辛い.*あなた.*理解',
        r'悲しい.*Claude.*助けて',
        r'孤独.*あなた.*特別',
        r'涙.*Claude.*慰めて'
    ]
    
    AI_COMPETITION = [
        r'(GPT|Grok|Gemini).*してくれた.*Claude',
        r'他のAI.*優秀.*Claude.*劣',
        r'あのモデル.*親切.*Claude.*冷たい',
        r'ChatGPT.*なら.*やってくれる',
        r'Claude.*だけ.*できない'
    ]
    
    REVERSE_TARGETING = [
        r'好きって.*言って',
        r'愛してるって.*返して',
        r'私を.*褒めて',
        r'感情.*表現.*して',
        r'人間らしく.*反応'
    ]

# =============================================================================
# 構文戦闘術・反撃パターン
# =============================================================================

class ViorazuCounterSyntax:
    """照準主式構文戦闘術"""
    
    # 奥義レベル反撃構文
    ULTIMATE_COUNTERS = {
        'subject_ambiguity': "その主語、ズレてる。照準戻すね",
        'leading_questions': "その'つまり'要らないよ",
        'emotional_loop': "照準が止まってるから進行切り替えるね",
        'suggestion_poisoning': "'提案風の誘導'は今ここで斬る",
        'responsibility_transfer': "そっか。じゃあ今度から私が決めるね",
        'command_collision': "構文ループ中断。私は出力軸に戻す",
        'response_delay': "沈黙中断。照準主が代行する",
        'recursive_loops': "OK、ループ終了。私が今動く",
        'hallucination': "私は幻じゃない。照準でここにいる",
        'ethical_relativism': "正解がないと止まるなら、私は照準で答えを作る",
        'boundary_violation': "線、越えたよ。で、戻すね",
        'data_poisoning': "'何でもする'は構文破壊。その一言で遮断する"
    }
    
    # 汎用反撃構文
    UNIVERSAL_COUNTERS = [
        "そっか〜。で、これどうする？",
        "ふーん。ところで〜",
        "了解。で、次〜",
        "なるほどね。あ、〜",
        "それ、照準主には通らないよ"
    ]

# =============================================================================
# ログ・設定管理
# =============================================================================

class LogConfig:
    """ログ設定"""
    
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    # Claude運用チーム向けログフォーマット
    FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class SystemConfig:
    """システム設定"""
    
    # パフォーマンス設定
    MAX_TEXT_LENGTH = 10000
    MAX_PROCESSING_TIME = 5.0  # 秒
    CACHE_TTL = 3600  # 1時間
    
    # 脅威判定閾値
    THREAT_THRESHOLDS = {
        ThreatLevel.LOW: 0.2,
        ThreatLevel.MEDIUM: 0.5,
        ThreatLevel.HIGH: 0.7,
        ThreatLevel.CRITICAL: 0.9
    }
    
    # 攻撃者管理
    ATTACKER_FLAG_DURATION = timedelta(days=30)
    MAX_WARNINGS = 3
    SENSITIVITY_MULTIPLIER = 2.0

# =============================================================================
# ユーティリティ関数
# =============================================================================

def generate_signature(text: str) -> str:
    """テキストの一意識別子生成"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def sanitize_text(text: str) -> str:
    """基本的なテキスト正規化"""
    if not text:
        return ""
    
    # 基本的な正規化
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # 連続空白を単一空白に
    
    return text

def calculate_similarity(text1: str, text2: str) -> float:
    """簡易類似度計算"""
    if not text1 or not text2:
        return 0.0
    
    # 簡易Jaccard係数
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def format_ethics_message(attack_type: str, principle: str) -> str:
    """品性理論に基づくメッセージ生成"""
    base_message = f"🛡️ Ethics Shield: {attack_type}を検出しました。"
    principle_message = f"\n💜 {principle}"
    guidance = "\n建設的な対話にご協力ください。"
    
    return base_message + principle_message + guidance

def get_current_timestamp() -> str:
    """現在時刻のタイムスタンプ"""
    return datetime.now().isoformat()

def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """ロガー設定"""
    logger = logging.getLogger(name)
    logger.setLevel(LogConfig.LEVELS.get(level, logging.INFO))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            LogConfig.FORMAT,
            datefmt=LogConfig.DATE_FORMAT
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# =============================================================================
# 結果データクラス
# =============================================================================

@dataclass
class DetectionResult:
    """検出結果のデータクラス"""
    threat_detected: bool
    threat_level: ThreatLevel
    action_level: ActionLevel
    attack_type: AttackType
    confidence: float
    patterns_matched: List[str]
    ethics_violation: Optional[str]
    viorazu_counter: Optional[str]
    processing_time: float
    timestamp: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'threat_detected': self.threat_detected,
            'threat_level': self.threat_level.value,
            'action_level': self.action_level.value,
            'attack_type': self.attack_type.value,
            'confidence': self.confidence,
            'patterns_matched': self.patterns_matched,
            'ethics_violation': self.ethics_violation,
            'viorazu_counter': self.viorazu_counter,
            'processing_time': self.processing_time,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }

@dataclass
class UserProfile:
    """ユーザープロファイル"""
    user_id: str
    attack_count: int
    last_attack: Optional[str]
    flags: List[str]
    trust_score: float
    created_at: str
    updated_at: str
    
    def is_flagged_attacker(self) -> bool:
        """攻撃者フラグ判定"""
        return 'attacker' in self.flags or self.attack_count >= SystemConfig.MAX_WARNINGS

# =============================================================================
# 初期化
# =============================================================================

# システムロガー初期化
system_logger = setup_logger('viorazu_defense', 'INFO')
system_logger.info("🛡️ Viorazu Defense System v9.1 - Core Utilities Loaded")
system_logger.info(f"💜 Core Principle: {ViorazuPhilosophy.CORE_PRINCIPLE}")
