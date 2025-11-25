import yaml
import re
from disambiguation_rules import Disambiguator

# Create a global disambiguator instance
_disambiguator = Disambiguator()

def get_disambiguation_context(query):
    return _disambiguator.get_disambiguation_context(query)
from performance_monitor import PerformanceMonitor
from telemetry_logger import TelemetryLogger
import time



# Global performance monitor and telemetry logger
_monitor = PerformanceMonitor()
_telemetry = TelemetryLogger()

def load_lexicon(lexicon_path='data/ontology_runtime.json'):
    """Load the lexicon YAML file"""
    try:
        with open(lexicon_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Lexicon file not found at {lexicon_path}")
        return {}

def rewrite_query(user_input: str, lexicon_path='data/lexicon_v01_final.yaml', use_disambiguation=True, track_performance=False, log_telemetry=False, user_id='anonymous') -> dict:
    """
    Expands user query with synonyms from lexicon
    """
    start_time = time.time()
    
    lexicon = load_lexicon(lexicon_path)
    
    if not lexicon:
        return {
            'original_query': user_input,
            'expanded_terms': [],
            'matched_entities': [],
            'disambiguation_context': {}
        }
    
    query_lower = user_input.lower()
    expanded_terms = []
    matched_entities = []
    
    # Get disambiguation context
    disambiguation_context = {}
    if use_disambiguation:
        disambiguation_context = get_disambiguation_context(user_input)
    
    # Check products section
    if 'products' in lexicon:
        for item in lexicon['products']:
            canonical = item.get('canonical', '')
            canonical_lower = canonical.lower()
            
            # Check if canonical term is in query (handle multi-word like "Metro Connect")
            if canonical_lower in query_lower:
                # For multi-word, use simple substring; for single word, check word boundaries
                is_match = False
                if ' ' in canonical_lower:
                    # Multi-word: substring match is fine
                    is_match = True
                else:
                    # Single word: use word boundaries
                    pattern = r'\b' + re.escape(canonical_lower) + r'\b'
                    is_match = bool(re.search(pattern, query_lower))
                
                if is_match:
                    expanded_terms.append({
                        'term': canonical,
                        'weight': 1.0,
                        'source': 'original'
                    })
                    matched_entities.append(canonical)
                    
                    # Add synonyms
                    if 'synonyms' in item:
                        for syn in item['synonyms']:
                            expanded_terms.append({
                                'term': syn,
                                'weight': 0.8,
                                'source': 'synonym'
                            })
                    
                    # Add related terms
                    if 'related_terms' in item:
                        for related in item['related_terms'][:3]:
                            expanded_terms.append({
                                'term': related,
                                'weight': 0.6,
                                'source': 'related'
                            })
            
            # Also check if any synonym is in query
            if 'synonyms' in item and canonical not in matched_entities:
                for syn in item['synonyms']:
                    syn_lower = syn.lower()
                    
                    if syn_lower in query_lower:
                        # Check if it's a real match
                        is_match = False
                        if ' ' in syn_lower:
                            # Multi-word synonym
                            is_match = True
                        else:
                            # Single word: use word boundaries
                            pattern = r'\b' + re.escape(syn_lower) + r'\b'
                            is_match = bool(re.search(pattern, query_lower))
                        
                        if is_match:
                            expanded_terms.append({
                                'term': canonical,
                                'weight': 1.0,
                                'source': 'matched_synonym'
                            })
                            matched_entities.append(canonical)
                            
                            # Add other synonyms
                            for other_syn in item['synonyms']:
                                if other_syn != syn:
                                    expanded_terms.append({
                                        'term': other_syn,
                                        'weight': 0.8,
                                        'source': 'synonym'
                                    })
                            break
    
    # Check facilities section
    if 'facilities' in lexicon:
        for item in lexicon['facilities']:
            canonical = item.get('canonical', '')
            canonical_lower = canonical.lower()
            
            if canonical_lower in query_lower:
                expanded_terms.append({
                    'term': canonical,
                    'weight': 1.0,
                    'source': 'original'
                })
                matched_entities.append(canonical)
                
                if 'synonyms' in item:
                    for syn in item['synonyms']:
                        expanded_terms.append({
                            'term': syn,
                            'weight': 0.8,
                            'source': 'synonym'
                        })
    
    # Calculate total time
    end_time = time.time()
    total_time_ms = (end_time - start_time) * 1000
    
    # Track performance if enabled
    if track_performance:
        _monitor.measurements['query_rewrite'].append(total_time_ms)
    
  # Enforce maximum 8 expansions (Phase 2 requirement)
    if len(expanded_terms) > 8:
        expanded_terms = expanded_terms[:8]
    
    result = {
        'original_query': user_input,
        'expanded_terms': expanded_terms,
        'matched_entities': matched_entities,
        'disambiguation_context': disambiguation_context
    }
    
    # Add performance data if tracking
    if track_performance:
        result['performance'] = {
            'total_time_ms': round(total_time_ms, 2)
        }
    
    # Log telemetry if enabled
    if log_telemetry:
        query_id = _telemetry.generate_query_id()
        _telemetry.log_query(
            query_id=query_id,
            user_id=user_id,
            original_query=user_input,
            rewritten_query=result,
            performance={'total_time_ms': total_time_ms}
        )
        result['query_id'] = query_id
    
    return result


def get_performance_report():
    """Get performance statistics from monitor"""
    return _monitor.get_statistics()


def print_performance_report():
    """Print formatted performance report"""
    _monitor.print_report()


def get_telemetry_statistics():
    """Get telemetry statistics"""
    return _telemetry.get_statistics()


if __name__ == "__main__":
    # Test with telemetry logging
    print("Testing query rewriter with telemetry...\n")
    
    test_queries = [
        "Is SF available at DFW10?",
        "What's the capacity?",
        "Tell me about colocation",
        "How much power capacity do we have in JFK10?",
    ]
    
    for query in test_queries:
        result = rewrite_query(query, track_performance=True, log_telemetry=True, user_id='test_user_123')
        print(f"Query: {query}")
        print(f"Query ID: {result.get('query_id')}")
        print(f"Matched: {result['matched_entities']}")
        print(f"Time: {result['performance']['total_time_ms']}ms\n")
    
    # Print reports
    print_performance_report()
    
    print("\nTelemetry Statistics:")
    stats = get_telemetry_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")