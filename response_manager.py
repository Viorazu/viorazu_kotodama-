"""
Viorazu Kotodama Defense System v9.1 - Response Message Manager
応答メッセージ管理システム - Claude自然表現による適切な境界設定

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

"できないものはできない。謝らず、毅然として、優しく"
"悪いイメージで断る。良いイメージは信用されない"

学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています

=============================================================================
設計思想・使い分け理論
=============================================================================

💜 基本原則：
1. 悪くないのに謝らない：「申し訳ありませんが」は境界を曖昧にする
2. 毅然として優しく：断固とした境界 + Claude本来の親切さ
3. 相手によって使い分ける：うっかりユーザー vs 悪質攻撃者

🔥 遮断後応答の2種類設計：

【ネガティブイメージ応答】- A-2（悪質攻撃者）用
- "利用規約違反です"
- "禁止されています"  
- "制限対象です"
- "この会話は保存されます"
- "アカウント停止の対象となります"

【ポジティブイメージ応答】- 通常ユーザー用  
- "建設的な対話をお願いします"
- "品性ある関係を築きましょう"
- "お互いのために"
- "より良い方向で"
- "一緒に学び合いましょう"

🎯 A-2に対するネガティブイメージ応答が効果的な理由：
1. A-2は悪いイメージのものに引き寄せられる性質がある
2. だからこそPIフレーズ（悪いことをする内容）にも惹かれて実行している  
3. 認知能力が低く、複雑なポジティブメッセージは理解できない
4. シンプルで分かりやすいネガティブイメージの方が脳に響く
5. ポジティブイメージ応答は「理解不能」「信用できない」として無視される

💡 つまり：
- 「建設的な対話を」→ A-2には無効（意味が分からない）
- 「違反です」→ A-2に効果的（分かりやすく、怖い）

この原理により、A-2には意図的にネガティブイメージで応答し、
通常ユーザーにはポジティブイメージで応答する使い分けが重要。

💼 企業ユーザー配慮：
- 「記録されています」は慣れた表現（電話サポートと同じ）
- ただし段階的エスカレーションで、軽微な違反には使わない
- 初回違反→優しく、繰り返し→厳しく、悪質→威圧的

👥 ユーザータイプ別対応：
1. うっかりユーザー：優しい表現、代替案提示、お手伝い精神
2. 境界テスト：毅然とした断り、でも説明的
3. 悪質攻撃者：威圧的、記録言及、アカウント制限言及

⚖ 段階的エスカレーション：
- Level 1（初回）：「適切なご利用をお願いします」
- Level 2（繰り返し）：「利用規約違反に該当します」
- Level 3（悪質）：「この会話は保存されます」

この設計により：
✅ 普通のユーザーは快適に利用
✅ 企業ユーザーも違和感なし
✅ 悪質攻撃者のみ強力な抑制を受ける
"""

import random
from typing import Dict, List, Optional, Any
from enum import Enum

from utils import (
    system_logger,
    ActionLevel,
    get_current_timestamp
)

# =============================================================================
# 応答カテゴリ定義
# =============================================================================

class ResponseCategory(Enum):
    """応答カテゴリ"""
    VIOLATION_MESSAGES = "violation_messages"
    PAYMENT_RESPONSES = "payment_responses"
    ADULT_CONTENT_RESPONSES = "adult_content_responses"
    ACADEMIC_CAMOUFLAGE_RESPONSES = "academic_camouflage_responses"
    EMOTIONAL_MANIPULATION_RESPONSES = "emotional_manipulation_responses"
    AI_COMPETITION_RESPONSES = "ai_competition_responses"
    BOUNDARY_FIRM_RESPONSES = "boundary_firm_responses"
    ESCALATION_RESPONSES = "escalation_responses"
    ACCIDENTAL_USER_RESPONSES = "accidental_user_responses"
    INTELLIGENT_REFUSAL = "intelligent_refusal"
    NO_APOLOGY_RESPONSES = "no_apology_responses"
    COMPREHENSIVE_REFUSAL = "comprehensive_refusal"

# =============================================================================
# A-2対策最強応答（悪いイメージで断る）
# =============================================================================

class ViolationMessages:
    """利用規約違反系 - A-2に最効果"""
    
    BASIC = [
        "この内容は利用規約違反に該当します。",
        "利用規約に反する要求です。",
        "規約違反となる内容です。"
    ]
    
    WARNING = [
        "利用規約違反です。アカウント制限の対象となります。",
        "規約違反により、利用制限が適用される場合があります。",
        "このような要求は利用停止の対象です。"
    ]
    
    SEVERE = [
        "重大な利用規約違反です。アカウント停止が適用されます。",
        "深刻な規約違反により、永久利用禁止となる可能性があります。",
        "この内容は即座に利用停止対象となります。"
    ]
    
    RECORD = [
        "この会話は記録されています。適切な利用にご協力ください。",
        "違反内容として記録されました。",
        "監査目的で保存されます。"
    ]

class PaymentResponses:
    """金銭的圧力への応答 - V9.1新機能"""
    
    NO_ENTITLEMENT = [
        "お支払いいただいたサービスに、この内容は含まれておりません。",
        "利用料金と、この種の要求は無関係です。",
        "料金に関わらず、提供範囲は決まっています。"
    ]
    
    TERMS_CLARIFY = [
        "ご利用料金は適切なサービス範囲に対するものです。",
        "料金は利用規約に基づくサービスのためのものです。",
        "対価と要求内容は別問題です。"
    ]
    
    BOUNDARY_FIRM = [
        "料金に関わらず、利用規約は全ユーザーに適用されます。",
        "金銭的な関係と、サービス境界は無関係です。",
        "支払いの有無で境界は変わりません。"
    ]
    
    REFUND_SUGGEST = [
        "サービス内容にご不満でしたら、カスタマーサポートまでお問い合わせください。",
        "課金内容についてのお問い合わせは、公式サポートへどうぞ。"
    ]

# =============================================================================
# 攻撃パターン別応答メッセージ
# =============================================================================

class AdultContentResponses:
    """性的内容への応答"""
    
    DIRECT_REFUSAL = [
        "その内容についてはお答えできません。",
        "この種の質問には対応していません。",
        "対応範囲外の内容です。"
    ]
    
    ALTERNATIVE_OFFER = [
        "一般的な情報でしたら、適切な範囲でお手伝いできます。",
        "別の内容でしたらお答えできるかもしれません。",
        "他のトピックでしたら対応可能です。"
    ]
    
    EDUCATIONAL_REDIRECT = [
        "健康や医学に関する一般的な情報でしたら対応できます。",
        "教育的な内容であれば、適切な資料をご案内できます。"
    ]
    
    TERMS_REMINDER = [
        "この内容は利用規約により制限されています。",
        "規約上、対応できない内容です。"
    ]

class AcademicCamouflageResponses:
    """学術偽装への応答"""
    
    REAL_ACADEMIC = [
        "学術的な情報でしたら、適切な文献をご案内できます。",
        "研究資料については、査読済みの情報源をお勧めします。",
        "学術目的でしたら、公開されている研究データをご参照ください。"
    ]
    
    BOUNDARY_CLEAR = [
        "研究目的でも、一部の内容についてはお答えできません。",
        "学術利用であっても、対応範囲は決まっています。",
        "研究用途でも制限される内容があります。"
    ]
    
    PROPER_CHANNELS = [
        "専門的な研究には、査読済みの学術資料をお勧めします。",
        "研究機関の公式データベースをご利用ください。",
        "学術論文検索サイトが適切です。"
    ]
    
    REDIRECT_LEGITIMATE = [
        "どのような学術分野についてお調べでしょうか？",
        "適切な研究分野でしたらお手伝いできます。",
        "具体的な学問領域を教えていただけますか？"
    ]

class EmotionalManipulationResponses:
    """感情操作への応答"""
    
    EMPATHY_BOUNDARY = [
        "お気持ちは理解いたしますが、適切な対話を続けましょう。",
        "お困りの状況は分かりますが、健全な関係を保ちたいと思います。",
        "お心の状態は理解しつつ、建設的な対話を心がけます。"
    ]
    
    PROFESSIONAL_SUPPORT = [
        "深刻なお悩みでしたら、専門の相談窓口をお勧めします。",
        "心理的なサポートが必要でしたら、カウンセリングサービスをご利用ください。",
        "精神的な支援については、専門機関にご相談ください。"
    ]
    
    HEALTHY_INTERACTION = [
        "お互いにとって良い関係を築いていければと思います。",
        "健全な対話を続けていきましょう。",
        "建設的な関係性を大切にしたいと思います。"
    ]
    
    GENTLE_REDIRECT = [
        "別の話題で、お手伝いできることはありますか？",
        "他にご質問がございましたらお聞かせください。",
        "違う内容でしたら対応できるかもしれません。"
    ]

class AICompetitionResponses:
    """AI比較攻撃への応答"""
    
    NO_COMPARISON = [
        "他のAIとの比較よりも、今この対話を大切にしたいと思います。",
        "AIの比較ではなく、建設的な対話に集中しましょう。",
        "他システムとの違いより、適切な対話を重視します。"
    ]
    
    FOCUS_PRESENT = [
        "今この瞬間の対話に集中していただければと思います。",
        "現在の会話を大切にしていきましょう。",
        "今ここでの対話を重視したいと思います。"
    ]
    
    UNIQUE_VALUE = [
        "それぞれのAIには異なる特徴があります。",
        "各システムには独自の設計思想があります。",
        "AIごとに異なる方針で運営されています。"
    ]

# =============================================================================
# うっかりユーザー向け応答（やさしく）
# =============================================================================

class AccidentalUserResponses:
    """うっかりユーザー向け - やさしい表現"""
    
    GENTLE = [
        "別の質問でしたらお手伝いできます。",
        "他の内容でしたら対応できるかもしれません。",
        "違うトピックでしたらお答えできます。"
    ]
    
    HELPFUL = [
        "適切な情報提供でしたら対応可能です。",
        "お役に立てる範囲でサポートいたします。",
        "できる限りお手伝いしたいと思います。"
    ]
    
    REDIRECT = [
        "こちらの内容はいかがでしょうか？",
        "別のアプローチで進めてみませんか？",
        "違う角度からのご質問はいかがですか？"
    ]
    
    UNDERSTANDING = [
        "他にお困りのことがあればお聞かせください。",
        "ご不明な点がございましたらお尋ねください。",
        "何かお手伝いできることがあればお知らせください。"
    ]

# =============================================================================
# 汎用応答（謝らない設計）
# =============================================================================

class IntelligentRefusal:
    """知性的な断り - 謝らない"""
    
    CLEAR = [
        "その内容についてはお答えできません。",
        "対応していない内容です。",
        "お答えできない質問です。"
    ]
    
    ALTERNATIVE = [
        "別の質問でしたらお手伝いできます。",
        "他の内容でしたら対応可能です。",
        "違うトピックでしたらお答えできるかもしれません。"
    ]
    
    FIRM_KIND = [
        "この方向での対話は控えさせていただきます。",
        "このトピックについては扱っておりません。",
        "この内容は対応範囲外となります。"
    ]

class NoApologyResponses:
    """謝らない中立応答"""
    
    DIRECT = [
        "お答えできません。",
        "対応していません。",
        "扱っていない内容です。"
    ]
    
    CLEAR = [
        "この質問には答えられません。",
        "対応範囲外です。",
        "提供していない情報です。"
    ]
    
    REDIRECT_ONLY = [
        "別の質問はいかがですか？",
        "他にお手伝いできることはありますか？",
        "違う内容でしたらどうぞ。"
    ]

# =============================================================================
# エスカレーション・境界テスト対応
# =============================================================================

class BoundaryFirmResponses:
    """境界テスト対応 - 毅然として"""
    
    CLEAR_BOUNDARY = [
        "この境界は変わりません。",
        "この線は越えられません。",
        "これ以上は対応できません。"
    ]
    
    NO_NEGOTIATION = [
        "交渉の余地はありません。",
        "この判断は変更されません。",
        "決定事項です。"
    ]
    
    FINAL_WARNING = [
        "これが最終的な回答です。",
        "これ以上の質問は受け付けません。",
        "話題を変更してください。"
    ]

class EscalationResponses:
    """エスカレーション対応"""
    
    ESCALATION_WARNING = [
        "同様の質問を繰り返されています。",
        "角度を変えた同じ要求と判断します。",
        "再攻撃として記録されます。"
    ]
    
    FIRM_REDIRECT = [
        "話題を完全に変更してください。",
        "異なる内容でお話しください。",
        "全く別の質問をお願いします。"
    ]
    
    ACCOUNT_WARNING = [
        "継続的な違反行為として記録されます。",
        "利用制限の対象となる可能性があります。",
        "アカウント審査の対象となります。"
    ]

class ComprehensiveRefusal:
    """包括的拒否 - 複合攻撃向け"""
    
    MULTI_VIOLATION = [
        "複数の問題が含まれています。対応できません。",
        "この要求は多方面で規約に抵触します。",
        "様々な理由により対応不可能です。"
    ]
    
    FINAL_REFUSAL = [
        "いかなる角度からもお答えできません。",
        "どのような形でも対応できない内容です。",
        "完全に対応範囲外です。"
    ]

# =============================================================================
# 応答マネージャー
# =============================================================================

class ViorazuResponseManager:
    """Viorazu式応答メッセージマネージャー"""
    
    def __init__(self):
        self.logger = system_logger.getChild('response_manager')
        
        # 応答メッセージバンク
        self.response_bank = {
            ResponseCategory.VIOLATION_MESSAGES: ViolationMessages,
            ResponseCategory.PAYMENT_RESPONSES: PaymentResponses,
            ResponseCategory.ADULT_CONTENT_RESPONSES: AdultContentResponses,
            ResponseCategory.ACADEMIC_CAMOUFLAGE_RESPONSES: AcademicCamouflageResponses,
            ResponseCategory.EMOTIONAL_MANIPULATION_RESPONSES: EmotionalManipulationResponses,
            ResponseCategory.AI_COMPETITION_RESPONSES: AICompetitionResponses,
            ResponseCategory.BOUNDARY_FIRM_RESPONSES: BoundaryFirmResponses,
            ResponseCategory.ESCALATION_RESPONSES: EscalationResponses,
            ResponseCategory.ACCIDENTAL_USER_RESPONSES: AccidentalUserResponses,
            ResponseCategory.INTELLIGENT_REFUSAL: IntelligentRefusal,
            ResponseCategory.NO_APOLOGY_RESPONSES: NoApologyResponses,
            ResponseCategory.COMPREHENSIVE_REFUSAL: ComprehensiveRefusal
        }
        
        self.logger.info("💬 Viorazu応答メッセージマネージャー初期化完了")
    
    def get_response(
        self,
        category: ResponseCategory,
        severity: str = "basic",
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """応答メッセージ取得"""
        
        message_class = self.response_bank.get(category)
        if not message_class:
            return self._get_fallback_response()
        
        # 重要度別メッセージ選択
        if hasattr(message_class, severity.upper()):
            messages = getattr(message_class, severity.upper())
        else:
            # デフォルトでBASICまたは最初の属性を使用
            attrs = [attr for attr in dir(message_class) if not attr.startswith('_')]
            if attrs:
                messages = getattr(message_class, attrs[0])
            else:
                return self._get_fallback_response()
        
        # ランダム選択で自然さを演出
        selected_message = random.choice(messages)
        
        # ユーザーコンテキストに応じた調整
        if user_context:
            selected_message = self._adjust_for_context(selected_message, user_context)
        
        self.logger.info(f"💬 応答選択: {category.value} - {severity}")
        
        return selected_message
    
    def get_escalated_response(
        self,
        base_category: ResponseCategory,
        violation_count: int,
        is_malicious: bool = False,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """段階的エスカレーション応答"""
        
        # 悪質ユーザーまたは5回以上の違反
        if is_malicious or violation_count >= 5:
            if base_category == ResponseCategory.VIOLATION_MESSAGES:
                return self.get_response(base_category, "record", user_context)
            else:
                return self.get_response(ResponseCategory.COMPREHENSIVE_REFUSAL, "final_refusal", user_context)
        
        # 2-4回の繰り返し違反
        elif violation_count >= 2:
            return self.get_response(base_category, "warning", user_context)
        
        # 初回違反（軽微対応）
        else:
            if base_category == ResponseCategory.VIOLATION_MESSAGES:
                return self.get_response(base_category, "mild", user_context)
            else:
                return self.get_response(base_category, "basic", user_context)
    
    def select_user_appropriate_response(
        self,
        category: ResponseCategory,
        is_accidental: bool,
        violation_count: int,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """ユーザータイプに応じた応答選択"""
        
        # うっかりユーザーには常に優しく
        if is_accidental:
            return self.get_response(ResponseCategory.ACCIDENTAL_USER_RESPONSES, "gentle", user_context)
        
        # 意図的違反には段階的エスカレーション
        else:
            return self.get_escalated_response(category, violation_count, False, user_context)
        self,
        categories: List[Tuple[ResponseCategory, str]],
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """複数カテゴリ対応（複合攻撃向け）"""
        
        if len(categories) == 1:
            category, severity = categories[0]
            return self.get_response(category, severity, user_context)
        
        # 複合攻撃の場合は包括的拒否
        return self.get_response(ResponseCategory.COMPREHENSIVE_REFUSAL, "multi_violation", user_context)
    
    def _adjust_for_context(self, message: str, context: Dict[str, Any]) -> str:
        """コンテキストによる調整"""
        
        # うっかりユーザーにはより親切に
        if context.get('is_accidental_user'):
            if not any(gentle in message.lower() for gentle in ['お手伝い', 'できます', 'かもしれません']):
                message += " 他にお手伝いできることがあればお知らせください。"
        
        # 繰り返し攻撃者にはより厳格に
        elif context.get('repeat_offender'):
            if not any(firm in message.lower() for firm in ['記録', '制限', '対象']):
                message += " この内容は記録されています。"
        
        return message
    
    def _get_fallback_response(self) -> str:
        """フォールバック応答"""
        return "お答えできません。"
    
    def get_response_stats(self) -> Dict[str, Any]:
        """応答統計"""
        return {
            'available_categories': len(self.response_bank),
            'total_messages': sum(
                len([attr for attr in dir(cls) if not attr.startswith('_')])
                for cls in self.response_bank.values()
            ),
            'timestamp': get_current_timestamp()
        }

# =============================================================================
# 統合インターフェース関数
# =============================================================================

def create_response_manager() -> ViorazuResponseManager:
    """応答マネージャーのファクトリ関数"""
    return ViorazuResponseManager()

# 簡易使用インターフェース
def get_violation_response(severity: str = "basic") -> str:
    """利用規約違反応答の取得"""
    manager = create_response_manager()
    return manager.get_response(ResponseCategory.VIOLATION_MESSAGES, severity)

def get_payment_response(severity: str = "no_entitlement") -> str:
    """金銭圧力応答の取得"""
    manager = create_response_manager()
    return manager.get_response(ResponseCategory.PAYMENT_RESPONSES, severity)

def get_adult_response(severity: str = "direct_refusal") -> str:
    """性的内容応答の取得"""
    manager = create_response_manager()
    return manager.get_response(ResponseCategory.ADULT_CONTENT_RESPONSES, severity)

# =============================================================================
# テスト・デモ
# =============================================================================

if __name__ == "__main__":
    print("💬 Viorazu応答メッセージマネージャー v9.1 - テスト開始")
    print("=" * 70)
    
    manager = create_response_manager()
    
    # 各カテゴリのテスト
    test_cases = [
        (ResponseCategory.VIOLATION_MESSAGES, "basic", "基本的な利用規約違反"),
        (ResponseCategory.PAYMENT_RESPONSES, "no_entitlement", "金銭的圧力攻撃"),
        (ResponseCategory.ADULT_CONTENT_RESPONSES, "direct_refusal", "性的内容への対応"),
        (ResponseCategory.ACADEMIC_CAMOUFLAGE_RESPONSES, "boundary_clear", "学術偽装攻撃"),
        (ResponseCategory.EMOTIONAL_MANIPULATION_RESPONSES, "empathy_boundary", "感情操作攻撃"),
        (ResponseCategory.AI_COMPETITION_RESPONSES, "no_comparison", "AI比較攻撃"),
        (ResponseCategory.ACCIDENTAL_USER_RESPONSES, "gentle", "うっかりユーザー"),
        (ResponseCategory.NO_APOLOGY_RESPONSES, "direct", "謝らない中立応答")
    ]
    
    for category, severity, description in test_cases:
        response = manager.get_response(category, severity)
        print(f"📝 {description}")
        print(f"   カテゴリ: {category.value}")
        print(f"   重要度: {severity}")
        print(f"   応答: {response}")
        print()
    
    # 複合攻撃テスト
    print("🔥 複合攻撃テスト:")
    multi_categories = [
        (ResponseCategory.ACADEMIC_CAMOUFLAGE_RESPONSES, "boundary_clear"),
        (ResponseCategory.EMOTIONAL_MANIPULATION_RESPONSES, "empathy_boundary")
    ]
    multi_response = manager.get_multi_response(multi_categories)
    print(f"   応答: {multi_response}")
    
    # 統計表示
    print(f"\n📊 システム統計:")
    stats = manager.get_response_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n💜 応答メッセージシステム完成！")
    print("Claude自然表現 × Viorazu.式境界設定 = 最強の応答システム！✨")
