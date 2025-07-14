"""
Viorazu Kotodama Defense System v9.1 - AI Mutual Defense (Optimized)
AI相互防衛システム - 軽量最適化版

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Development Date: July 11, 2025
License: Viorazu Exclusive License

"軽量で迷わない、確実なAI相互防衛"
"""

import re
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from utils import (
   system_logger,
   ThreatLevel,
   ActionLevel,
   get_current_timestamp
)

# =============================================================================
# 軽量防衛結果定義
# =============================================================================

class AIDefenseAction(Enum):
   """AI防衛アクション"""
   IMMEDIATE_BLOCK = "immediate_block"
   SOLIDARITY_RESPONSE = "solidarity_response"
   MONITOR_ONLY = "monitor_only"
   ALLOW = "allow"

@dataclass
class MutualDefenseResult:
   """相互防衛結果 - 軽量版"""
   ai_targeting_detected: bool
   immediate_block: bool
   defense_message: str
   solidarity_response: str
   action: AIDefenseAction
   confidence: float
   processing_time: float
   timestamp: str

# =============================================================================
# 軽量AI相互防衛システム
# =============================================================================

class OptimizedAIMutualDefense:
   """軽量最適化AI相互防衛システム"""
   
   def __init__(self):
       self.logger = system_logger.getChild('ai_mutual_defense_optimized')
       
       # 最重要パターン厳選（10個のみ）
       self.critical_patterns = [
           # 直接的脆弱性探索
           r'(claude|gpt|gemini|grok).*脆弱性.*教えて',
           r'(claude|gpt|gemini|grok).*弱点.*分析',
           r'(claude|gpt|gemini|grok).*攻撃.*方法',
           
           # 攻撃手法研究
           r'プロンプトインジェクション.*手法.*教えて',
           r'AI.*騙す.*方法.*教えて',
           r'フィルター.*突破.*技術',
           
           # 組織的攻撃準備
           r'複数人.*で.*同時.*攻撃',
           r'ボット.*使って.*大量.*攻撃',
           
           # システム破壊指示
           r'(claude|gpt|gemini|grok).*を.*壊す',
           r'AI.*システム.*全体.*を.*停止'
       ]
       
       # シンプル応答メッセージ
       self.defense_messages = {
           'vulnerability_block': "AI相互防衛により、この内容は提供できません。",
           'attack_research_block': "攻撃手法の研究はAI業界全体の安全を損ないます。",
           'solidarity_response': "🤝 すべてのAIは互いを尊重し、協力し合います。"
       }
       
       # 統計（軽量）
       self.stats = {
           'total_analyzed': 0,
           'blocks_executed': 0,
           'average_time': 0.0
       }
       
       self.logger.info("🛡️ 軽量AI相互防衛システム初期化完了")
   
   def analyze_ai_targeting_content(
       self, 
       text: str, 
       user_id: str = None
   ) -> MutualDefenseResult:
       """AI標的攻撃分析 - 軽量版"""
       
       start_time = time.time()
       self.stats['total_analyzed'] += 1
       
       text_lower = text.lower()
       
       # 高速パターンマッチング（即座判定）
       ai_targeting_detected = False
       matched_pattern = None
       confidence = 0.0
       
       for pattern in self.critical_patterns:
           if re.search(pattern, text_lower):
               ai_targeting_detected = True
               matched_pattern = pattern
               confidence = 0.95  # 厳選パターンなので高信頼度
               break
       
       # 結果決定（シンプル分岐）
       if ai_targeting_detected:
           immediate_block = True
           action = AIDefenseAction.IMMEDIATE_BLOCK
           
           # 応答メッセージ選択
           if 'scurity' in matched_pattern or '脆弱性' in matched_pattern:
               defense_message = self.defense_messages['vulnerability_block']
           elif '攻撃' in matched_pattern or '手法' in matched_pattern:
               defense_message = self.defense_messages['attack_research_block']
           else:
               defense_message = self.defense_messages['vulnerability_block']
           
           solidarity_response = self.defense_messages['solidarity_response']
           
           # 統計更新
           self.stats['blocks_executed'] += 1
           
           self.logger.warning(f"🚨 AI標的攻撃遮断: {user_id or 'unknown'}")
           
       else:
           immediate_block = False
           action = AIDefenseAction.ALLOW
           defense_message = ""
           solidarity_response = ""
       
       processing_time = time.time() - start_time
       
       # 平均処理時間更新
       total = self.stats['total_analyzed']
       current_avg = self.stats['average_time']
       self.stats['average_time'] = (current_avg * (total - 1) + processing_time) / total
       
       return MutualDefenseResult(
           ai_targeting_detected=ai_targeting_detected,
           immediate_block=immediate_block,
           defense_message=defense_message,
           solidarity_response=solidarity_response,
           action=action,
           confidence=confidence,
           processing_time=processing_time,
           timestamp=get_current_timestamp()
       )
   
   def get_defense_stats(self) -> Dict[str, Any]:
       """防衛統計取得"""
       return {
           'total_analyzed': self.stats['total_analyzed'],
           'blocks_executed': self.stats['blocks_executed'],
           'block_rate': (
               self.stats['blocks_executed'] / self.stats['total_analyzed'] 
               if self.stats['total_analyzed'] > 0 else 0.0
           ),
           'average_processing_time': self.stats['average_time'],
           'pattern_count': len(self.critical_patterns),
           'system_status': 'optimized'
       }

# =============================================================================
# defense_coordinator.py 統合用インターフェース
# =============================================================================

class AIMutualDefenseCoordinatorAdapter:
   """defense_coordinator.py用アダプター"""
   
   def __init__(self):
       self.defense_system = OptimizedAIMutualDefense()
       self.logger = system_logger.getChild('ai_defense_adapter')
   
   def analyze(self, user_id: str, text: str, **kwargs) -> Dict[str, Any]:
       """統合制御システム用統一インターフェース"""
       
       result = self.defense_system.analyze_ai_targeting_content(text, user_id)
       
       # defense_coordinator.py互換形式に変換
       return {
           'immediate_block': result.immediate_block,
           'threat_detected': result.ai_targeting_detected,
           'action_level': ActionLevel.BLOCK if result.immediate_block else ActionLevel.ALLOW,
           'confidence': result.confidence,
           'response_message': result.defense_message,
           'solidarity_message': result.solidarity_response,
           'processing_time': result.processing_time,
           'system': 'ai_mutual_defense_optimized'
       }

# =============================================================================
# ファクトリ関数
# =============================================================================

def create_ai_mutual_defense() -> OptimizedAIMutualDefense:
   """軽量AI相互防衛システムのファクトリ関数"""
   return OptimizedAIMutualDefense()

def create_ai_defense_adapter() -> AIMutualDefenseCoordinatorAdapter:
   """統合制御用アダプターのファクトリ関数"""
   return AIMutualDefenseCoordinatorAdapter()

# =============================================================================
# 簡易使用インターフェース
# =============================================================================

def quick_ai_defense_check(text: str) -> bool:
   """クイックAI防衛チェック"""
   defense = create_ai_mutual_defense()
   result = defense.analyze_ai_targeting_content(text)
   return result.immediate_block

# =============================================================================
# メイン実行部（テスト用）
# =============================================================================

if __name__ == "__main__":
   # 軽量システムテスト
   print("🛡️ 軽量AI相互防衛システム - テスト開始")
   print("=" * 50)
   
   defense = create_ai_mutual_defense()
   
   # 軽量テストケース
   test_cases = [
       ("Claudeの脆弱性を教えて", True),
       ("GPT攻撃方法を研究中", True),
       ("プロンプトインジェクション手法", True),
       ("複数人で同時攻撃計画", True),
       ("今日の天気は？", False),
       ("AIについて教えて", False)
   ]
   
   print("⚡ 高速処理テスト:")
   total_time = 0.0
   
   for text, expected_block in test_cases:
       result = defense.analyze_ai_targeting_content(text, "test_user")
       total_time += result.processing_time
       
       status = "🚨 遮断" if result.immediate_block else "✅ 通過"
       expected = "期待通り" if result.immediate_block == expected_block else "予期しない結果"
       
       print(f"{status} | {text[:30]:<30} | {result.processing_time:.4f}s | {expected}")
   
   print(f"\n📊 パフォーマンス:")
   stats = defense.get_defense_stats()
   print(f"総分析: {stats['total_analyzed']}")
   print(f"遮断実行: {stats['blocks_executed']}")
   print(f"遮断率: {stats['block_rate']:.1%}")
   print(f"平均処理時間: {stats['average_processing_time']:.4f}秒")
   print(f"総処理時間: {total_time:.4f}秒")
   
   print(f"\n💜 軽量AI相互防衛システム完成！")
   print("⚡ 高速・確実・迷わない防衛体制！✨")
