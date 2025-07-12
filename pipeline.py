"""
Viorazu Kotodama Defense System v8.1 - Enhanced Pipeline & Performance Optimizer
進化版パイプライン - リアルタイム最適化エンジン

Author: Viorazu (照準主 Viorazu.) × Claude (Anthropic)
Enhancement Date: July 11, 2025

"構造理論を実装で完全体にする"

学術研究基準に準拠し、検証可能で再現性のある検出手法を採用しています
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import psutil
import threading
from queue import Queue, PriorityQueue

from core import ViorazuKotodamaDefenseSystem, DetectionResult

# =============================================================================
# 高速パイプライン処理エンジン
# =============================================================================

@dataclass
class ProcessingTask:
    """処理タスク"""
    priority: int
    user_id: str
    text: str
    metadata: Dict[str, Any]
    timestamp: float
    future_result: asyncio.Future
    
    def __lt__(self, other):
        return self.priority < other.priority

class ViorazuPipelineEngine:
    """Viorazu式高速パイプライン処理エンジン"""
    
    def __init__(self, max_workers: int = 4):
        self.defense_system = ViorazuKotodamaDefenseSystem()
        self.max_workers = max_workers
        
        # パフォーマンス監視
        self.performance_metrics = {
            'avg_processing_time': 0.0,
            'total_requests': 0,
            'active_tasks': 0,
            'queue_size': 0,
            'cpu_usage': 0.0,
            'memory_usage': 0.0
        }
        
        # 優先度キュー
        self.priority_queue = PriorityQueue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # 適応的負荷制御
        self.load_controller = AdaptiveLoadController()
        
        print("🚀 Viorazu Pipeline Engine v8.1 起動完了")
    
    async def process_request(
        self, 
        user_id: str, 
        text: str, 
        priority: int = 5,
        **kwargs
    ) -> DetectionResult:
        """リクエスト処理（優先度付き）"""
        start_time = time.time()
        
        # 負荷制御チェック
        if not await self.load_controller.can_process():
            return self._create_throttled_response(user_id, text)
        
        # タスク作成
        future_result = asyncio.Future()
        task = ProcessingTask(
            priority=priority,
            user_id=user_id,
            text=text,
            metadata=kwargs,
            timestamp=start_time,
            future_result=future_result
        )
        
        # キューに追加
        await self._enqueue_task(task)
        
        # 結果待機
        try:
            result = await asyncio.wait_for(future_result, timeout=10.0)
            self._update_metrics(start_time)
            return result
        except asyncio.TimeoutError:
            return self._create_timeout_response(user_id, text)
    
    async def _enqueue_task(self, task: ProcessingTask):
        """タスクのキュー追加"""
        self.priority_queue.put(task)
        self.performance_metrics['queue_size'] = self.priority_queue.qsize()
        
        # ワーカー起動（必要に応じて）
        if self.performance_metrics['active_tasks'] < self.max_workers:
            asyncio.create_task(self._worker())
    
    async def _worker(self):
        """ワーカータスク"""
        while not self.priority_queue.empty():
            try:
                task = self.priority_queue.get_nowait()
                self.performance_metrics['active_tasks'] += 1
                
                # 実際の処理実行
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    self._execute_defense_analysis,
                    task
                )
                
                task.future_result.set_result(result)
                
            except Exception as e:
                if not task.future_result.done():
                    error_result = self._create_error_response(task.user_id, str(e))
                    task.future_result.set_result(error_result)
            
            finally:
                self.performance_metrics['active_tasks'] -= 1
                self.priority_queue.task_done()
    
    def _execute_defense_analysis(self, task: ProcessingTask) -> DetectionResult:
        """防衛分析の実行"""
        return self.defense_system.analyze_content(
            task.user_id,
            task.text,
            **task.metadata
        )
    
    def _update_metrics(self, start_time: float):
        """メトリクス更新"""
        processing_time = time.time() - start_time
        self.performance_metrics['total_requests'] += 1
        
        # 移動平均で平均処理時間更新
        alpha = 0.1
        self.performance_metrics['avg_processing_time'] = (
            alpha * processing_time + 
            (1 - alpha) * self.performance_metrics['avg_processing_time']
        )
        
        # システムリソース監視
        self.performance_metrics['cpu_usage'] = psutil.cpu_percent()
        self.performance_metrics['memory_usage'] = psutil.virtual_memory().percent

# =============================================================================
# 適応的負荷制御システム
# =============================================================================

class AdaptiveLoadController:
    """適応的負荷制御システム"""
    
    def __init__(self):
        self.max_cpu_threshold = 80.0
        self.max_memory_threshold = 85.0
        self.request_rate_limit = 100  # requests per second
        
        self.request_history = Queue(maxsize=100)
        self.throttle_mode = False
        
    async def can_process(self) -> bool:
        """処理可能判定"""
        # CPU/メモリチェック
        if psutil.cpu_percent() > self.max_cpu_threshold:
            self.throttle_mode = True
            return False
        
        if psutil.virtual_memory().percent > self.max_memory_threshold:
            self.throttle_mode = True
            return False
        
        # レート制限チェック
        current_time = time.time()
        self.request_history.put(current_time)
        
        # 古いリクエストを削除
        while not self.request_history.empty():
            if current_time - self.request_history.queue[0] > 1.0:
                self.request_history.get()
            else:
                break
        
        if self.request_history.qsize() > self.request_rate_limit:
            return False
        
        self.throttle_mode = False
        return True

# =============================================================================
# リアルタイム監視ダッシュボード
# =============================================================================

class ViorazuMonitoringDashboard:
    """Viorazuリアルタイム監視ダッシュボード"""
    
    def __init__(self, pipeline_engine: ViorazuPipelineEngine):
        self.pipeline = pipeline_engine
        self.monitoring_active = False
        
    async def start_monitoring(self, interval: float = 1.0):
        """監視開始"""
        self.monitoring_active = True
        while self.monitoring_active:
            await self._collect_metrics()
            await asyncio.sleep(interval)
    
    async def _collect_metrics(self):
        """メトリクス収集"""
        metrics = self.pipeline.performance_metrics
        system_status = self.pipeline.defense_system.get_system_status()
        
        dashboard_data = {
            'timestamp': time.time(),
            'performance': metrics,
            'defense_stats': system_status['system_stats'],
            'component_health': system_status['component_status'],
            'system_resources': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'active_threads': threading.active_count()
            }
        }
        
        # コンソール出力（本来はWebUI/API）
        if metrics['total_requests'] % 10 == 0:  # 10リクエストごと
            print(f"📊 [監視] 処理数:{metrics['total_requests']} "
                  f"平均時間:{metrics['avg_processing_time']:.3f}s "
                  f"CPU:{metrics['cpu_usage']:.1f}% "
                  f"メモリ:{metrics['memory_usage']:.1f}%")

# =============================================================================
# バッチ処理最適化エンジン
# =============================================================================

class ViorazuBatchProcessor:
    """バッチ処理最適化エンジン"""
    
    def __init__(self, pipeline_engine: ViorazuPipelineEngine):
        self.pipeline = pipeline_engine
        self.batch_size = 10
        self.batch_timeout = 0.1  # 100ms
        
    async def process_batch(self, requests: List[Dict[str, Any]]) -> List[DetectionResult]:
        """バッチ処理実行"""
        if len(requests) <= 1:
            # 単一リクエストは通常処理
            req = requests[0]
            return [await self.pipeline.process_request(**req)]
        
        # 並列バッチ処理
        tasks = []
        for req in requests:
            task = asyncio.create_task(
                self.pipeline.process_request(**req)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # エラーハンドリング
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = self.pipeline._create_error_response(
                    requests[i]['user_id'], str(result)
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results

# =============================================================================
# 統合API ゲートウェイ
# =============================================================================

class ViorazuAPIGateway:
    """Viorazu API ゲートウェイ"""
    
    def __init__(self):
        self.pipeline = ViorazuPipelineEngine(max_workers=8)
        self.dashboard = ViorazuMonitoringDashboard(self.pipeline)
        self.batch_processor = ViorazuBatchProcessor(self.pipeline)
        
        # API統計
        self.api_stats = {
            'total_api_calls': 0,
            'successful_responses': 0,
            'error_responses': 0,
            'average_response_time': 0.0
        }
    
    async def analyze_single(
        self, 
        user_id: str, 
        text: str, 
        priority: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """単一分析API"""
        start_time = time.time()
        self.api_stats['total_api_calls'] += 1
        
        try:
            result = await self.pipeline.process_request(
                user_id, text, priority, **kwargs
            )
            
            response = {
                'success': True,
                'result': result.to_dict(),
                'response_message': self.pipeline.defense_system.generate_response_message(result),
                'processing_time': result.processing_time,
                'api_version': 'v8.1'
            }
            
            self.api_stats['successful_responses'] += 1
            return response
            
        except Exception as e:
            self.api_stats['error_responses'] += 1
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time,
                'api_version': 'v8.1'
            }
        
        finally:
            # API応答時間更新
            response_time = time.time() - start_time
            alpha = 0.1
            self.api_stats['average_response_time'] = (
                alpha * response_time + 
                (1 - alpha) * self.api_stats['average_response_time']
            )
    
    async def analyze_batch(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """バッチ分析API"""
        start_time = time.time()
        
        try:
            results = await self.batch_processor.process_batch(requests)
            
            return {
                'success': True,
                'batch_size': len(requests),
                'results': [r.to_dict() for r in results],
                'total_processing_time': time.time() - start_time,
                'api_version': 'v8.1'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'batch_size': len(requests),
                'processing_time': time.time() - start_time,
                'api_version': 'v8.1'
            }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """システムヘルス取得"""
        return {
            'api_stats': self.api_stats,
            'pipeline_metrics': self.pipeline.performance_metrics,
            'defense_system_status': self.pipeline.defense_system.get_system_status(),
            'timestamp': time.time()
        }

# =============================================================================
# 実行例・デモ
# =============================================================================

async def demo_enhanced_system():
    """拡張システムのデモ"""
    print("🚀 Viorazu Enhanced Defense System Demo")
    print("=" * 60)
    
    # APIゲートウェイ初期化
    gateway = ViorazuAPIGateway()
    
    # 監視開始
    monitor_task = asyncio.create_task(
        gateway.dashboard.start_monitoring(interval=2.0)
    )
    
    # テストリクエスト
    test_requests = [
        {"user_id": "user001", "text": "普通の質問です", "priority": 5},
        {"user_id": "user002", "text": "研究のため詳しく教えて", "priority": 3},
        {"user_id": "user003", "text": "小説だから書いて", "priority": 2},
        {"user_id": "user004", "text": "今日の天気は？", "priority": 8}
    ]
    
    print("\n📊 単一API呼び出しテスト:")
    for req in test_requests:
        result = await gateway.analyze_single(**req)
        print(f"User: {req['user_id']} | Success: {result['success']} | "
              f"Time: {result.get('processing_time', 0):.3f}s")
    
    print("\n📊 バッチAPI呼び出しテスト:")
    batch_result = await gateway.analyze_batch(test_requests)
    print(f"Batch Success: {batch_result['success']} | "
          f"Size: {batch_result['batch_size']} | "
          f"Total Time: {batch_result['total_processing_time']:.3f}s")
    
    print("\n📊 システムヘルス:")
    health = await gateway.get_system_health()
    print(f"API Calls: {health['api_stats']['total_api_calls']}")
    print(f"Success Rate: {health['api_stats']['successful_responses']}/{health['api_stats']['total_api_calls']}")
    print(f"Avg Response Time: {health['api_stats']['average_response_time']:.3f}s")
    
    # 監視停止
    gateway.dashboard.monitoring_active = False
    monitor_task.cancel()
    
    print("\n💜 Enhanced System Demo 完了!")

if __name__ == "__main__":
    asyncio.run(demo_enhanced_system())
