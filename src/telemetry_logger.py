import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid


class TelemetryLogger:
    """
    Log query pipeline telemetry for analysis and A/B testing
    
    Captures:
    - Query input and rewrite
    - Retrieval results
    - Performance metrics
    - User feedback (if available)
    """
    
    def __init__(self, storage_path='outputs/telemetry_logs.jsonl'):
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        import os
        os.makedirs('outputs', exist_ok=True)
        
    def _hash_user_id(self, user_id: str) -> str:
        """Hash user ID for privacy (PII masking)"""
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]
    
    def log_query(self, 
                  query_id: str,
                  user_id: str,
                  original_query: str,
                  rewritten_query: Dict,
                  performance: Dict,
                  metadata: Optional[Dict] = None) -> None:
        """
        Log a complete query event
        
        Args:
            query_id: Unique ID for this query
            user_id: User identifier (will be hashed)
            original_query: User's original query text
            rewritten_query: Output from query rewriter
            performance: Timing metrics
            metadata: Optional additional context
        """
        
        log_entry = {
            'query_id': query_id,
            'user_id_hash': self._hash_user_id(user_id),  # PII masked
           'timestamp': datetime.now(timezone.utc).isoformat(),
            
            # Query data
            'original_query': original_query,
            'expanded_terms': rewritten_query.get('expanded_terms', []),
            'matched_entities': rewritten_query.get('matched_entities', []),
            'disambiguation_context': rewritten_query.get('disambiguation_context', {}),
            
            # Performance
            'query_rewrite_time_ms': performance.get('total_time_ms', 0),
            
            # Placeholders for downstream pipeline (filled by RAG system)
            'retrieval_time_ms': None,
            'generation_time_ms': None,
            'total_pipeline_time_ms': None,
            
            # Retrieval results (filled by RAG system)
            'retrieval_results': [],
            'rerank_results': [],
            
            # User feedback (filled later if available)
            'first_answer_success': None,  # Manual labeling in Week 3
            'user_feedback': None,  # thumbs up/down
            
            # Metadata
            'metadata': metadata or {}
        }
        
        # Write to JSONL file (one JSON object per line)
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def generate_query_id(self) -> str:
        """Generate unique query ID"""
        return f"query_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    def read_logs(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Read telemetry logs
        
        Args:
            limit: Maximum number of logs to return (most recent)
        
        Returns:
            List of log entries
        """
        logs = []
        try:
            with open(self.storage_path, 'r') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except FileNotFoundError:
            return []
        
        if limit:
            logs = logs[-limit:]
        
        return logs
    
    def get_statistics(self) -> Dict:
        """Get basic statistics from logs"""
        logs = self.read_logs()
        
        if not logs:
            return {'total_queries': 0}
        
        return {
            'total_queries': len(logs),
            'unique_users': len(set(log['user_id_hash'] for log in logs)),
            'avg_rewrite_time_ms': sum(log['query_rewrite_time_ms'] for log in logs) / len(logs),
            'queries_with_matches': sum(1 for log in logs if log['matched_entities']),
            'queries_without_matches': sum(1 for log in logs if not log['matched_entities']),
        }


# Test function
if __name__ == "__main__":
    logger = TelemetryLogger()
    
    # Simulate logging a query
    query_id = logger.generate_query_id()
    
    # Mock query rewrite result
    rewrite_result = {
        'original_query': 'Is SF available at DFW10?',
        'expanded_terms': [
            {'term': 'ServiceFabric', 'weight': 1.0, 'source': 'matched_synonym'}
        ],
        'matched_entities': ['ServiceFabric', 'DFW10'],
        'disambiguation_context': {}
    }
    
    # Mock performance
    performance = {'total_time_ms': 8.5}
    
    # Log it
    logger.log_query(
        query_id=query_id,
        user_id='test_user_123',  # Will be hashed
        original_query='Is SF available at DFW10?',
        rewritten_query=rewrite_result,
        performance=performance,
        metadata={'session_id': 'session_abc', 'source': 'web_chat'}
    )
    
    print("Logged 1 query")
    print(f"\nStatistics:")
    stats = logger.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\nLogs saved to: {logger.storage_path}")