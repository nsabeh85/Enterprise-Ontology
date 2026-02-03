"""
Mock data for local development.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List

def generate_mock_rewriter_data() -> List[Dict[str, Any]]:
    """Generate mock query rewriter data."""
    base_time = datetime.now()
    data = []
    
    # Sample queries
    queries = [
        {"query": "Is SF available at DFW10?", "entities": ["ServiceFabric", "DFW10"], "expanded": True, "results": 45},
        {"query": "What is Metro Connect?", "entities": ["Metro Connect"], "expanded": True, "results": 23},
        {"query": "Show me Dallas facilities", "entities": ["Dallas", "DFW10"], "expanded": True, "results": 12},
        {"query": "How does it work?", "entities": [], "expanded": False, "results": 8},
        {"query": "ServiceFabric pricing", "entities": ["ServiceFabric"], "expanded": True, "results": 34},
    ]
    
    for i, q in enumerate(queries * 20):  # Generate 100 records
        timestamp = base_time - timedelta(hours=i)
        data.append({
            "id": f"rewriter_{i}",
            "conversation": q["query"],
            "conversation_id": f"conv_{i}",
            "timestamp": timestamp.isoformat(),
            "_ts": int(timestamp.timestamp()),
            "resultCount": q["results"],
            "query_rewrite_telemetry": {
                "matched_entities": q["entities"],
                "expansion_count": len(q["entities"]) if q["expanded"] else 0,
                "expanded_query": f"{q['query']} OR {' OR '.join(q['entities'])}" if q["expanded"] else q["query"],
                "rewrite_time_ms": 3.5 + (i % 10) * 0.5
            },
            "evaluation_scores": {
                "relevance": 0.85 + (i % 10) * 0.01,
                "groundedness": 0.82 + (i % 10) * 0.01,
                "completeness": 0.88 + (i % 10) * 0.01
            }
        })
    
    return data

def generate_mock_adoption_data() -> List[Dict[str, Any]]:
    """Generate mock adoption data."""
    base_time = datetime.now()
    data = []
    users = [f"user_{i}" for i in range(1, 51)]
    
    for i in range(200):
        timestamp = base_time - timedelta(hours=i % 168)  # Last week
        user = users[i % len(users)]
        data.append({
            "id": f"adoption_{i}",
            "conversation_id": f"conv_{i}",
            "user_id": user,
            "user_name": user,
            "timestamp": timestamp.isoformat(),
            "_ts": int(timestamp.timestamp()),
            "conversation": f"Sample query {i}",
            "llm_telemetry": {
                "response_time_ms": 2000 + (i % 20) * 100
            }
        })
    
    return data

def generate_mock_feedback_data() -> List[Dict[str, Any]]:
    """Generate mock feedback data."""
    base_time = datetime.now()
    data = []
    feedback_types = ["thumbsUp", "thumbsDown"] * 30
    categories = ["Helpful", "Accurate", "Fast", "Uncategorized"]
    
    for i in range(60):
        timestamp = base_time - timedelta(days=i % 30)
        data.append({
            "id": f"feedback_{i}",
            "conversationId": f"conv_{i}",
            "userName": f"user_{i % 20}",
            "timestamp": timestamp.isoformat(),
            "_ts": int(timestamp.timestamp()),
            "feedbackType": feedback_types[i],
            "comment": f"Sample feedback comment {i}" if i % 3 == 0 else "",
            "category": categories[i % len(categories)]
        })
    
    return data

# Pre-generate mock data
MOCK_REWRITER_DATA = generate_mock_rewriter_data()
MOCK_ADOPTION_DATA = generate_mock_adoption_data()
MOCK_FEEDBACK_DATA = generate_mock_feedback_data()
