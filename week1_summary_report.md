# Week 1 Discovery & Foundations - Summary Report

**Project:** Enterprise Ontology, NLP-Driven Query Expansion & Data Roadmap  
**Phase:** Week 1 - Discovery & Foundations  
**Date Completed:** November 13, 2025  
**Analyst:** Nabih Sabeh

---

## Executive Summary

I analyzed 2,691 user queries from the Nexus chatbot (September 11 - November 11, 2025) to establish a semantic and behavioral baseline for how users interact with the system. The analysis revealed critical insights about user expectations, system performance, and areas for improvement.

**Key Finding:** 70% of queries are out-of-scope, indicating users treat Nexus as a general-purpose assistant rather than a specialized data center information tool. This represents the primary failure mode and user education opportunity.

**Baseline Performance:** The system achieves 68.4% first-answer success on domain-relevant queries, with strongest performance on ServiceFabric product queries (100%) and weakest on site discovery queries (28.6%).

---

## Deliverables Completed

### 1. Query Clustering Analysis
**Status:** Complete

**Methodology:**
- Extracted 3,550 conversations (61 days of data)
- Cleaned to 2,691 queries, analyzed 792 in-scope queries
- Generated embeddings using text-embedding-ada-002 (production model)
- Applied KMeans clustering with k=5 (silhouette score: 0.067)

**Results - 5 Intent Classes Identified:**

1. **Cluster 2: Infrastructure Capacity & Power (239 queries, 30%)**
   - User intent: Power availability, capacity requirements, infrastructure specifications
   - Example: "How many megawatts is available in DFW10?"
   - Maps to: additional-properties index

2. **Cluster 3: Site Discovery & General Information (228 queries, 29%)**
   - User intent: Location discovery, site characteristics, regional availability
   - Example: "What data centers are in EMEA region?"
   - Maps to: additional-properties, productized-colocation-sites indexes

3. **Cluster 4: ServiceFabric Product Inquiries (70 queries, 9%)**
   - User intent: ServiceFabric availability, connectivity, product comparisons
   - Example: "Is ServiceFabric available at DFW10?"
   - Maps to: nvidia-service-fabric-information index

4. **Cluster 0: Organizational/Policy Inquiries (115 queries, 15%)**
   - Status: Out-of-scope
   - User intent: Company information, HR questions, organizational structure
   - Failure mode: Users expecting company-wide knowledge base

5. **Cluster 1: German Language Queries (140 queries, 18%)**
   - Status: Language barrier
   - Issue: Language-based clustering preventing content classification
   - Recommendation: Translation layer for proper intent identification

**Key Insight:** The 3 dominant in-scope clusters (68% of clean queries) align well with the existing 9-index architecture, validating current retrieval system design.

---

### 2. Enterprise Lexicon v0.1
**Status:** Complete  
**File:** `lexicon_v01_final.yaml`

**Contents:**
- **28 canonical terms** across 5 categories
- Products & Services (6): ServiceFabric, Colocation, Scale, PlatformDIGITAL, Data Gravity, DRIX
- Facilities (2): DFW10, PHX10 (with address synonyms)
- Technical Terms (14): data center, capacity/power, cooling, rack, deployment, generator, PUE, infrastructure, cabinet, cage, suite, redundant, CSP, NSP
- Partners (1): Megaport
- Geographic (3): EMEA, APAC, North America

**Key Features:**
- Synonym mapping (e.g., ServiceFabric = SF = Service Fabric)
- Disambiguation rules for ambiguous terms ("fabric", "capacity")
- Related term connections for semantic expansion
- Units and conversions (kW/MW)

**Usage:** This lexicon will power the Week 2 query rewrite service for synonym expansion and term normalization.

---

### 3. Preliminary Ontology Graph
**Status:** Complete  
**File:** `preliminary_ontology_graph.png`

**Structure:**
- **23 nodes** across 5 entity categories
- **20 edges** representing relationships
- **5 relationship types:** available_at, connects_to, has_attribute, offers_capacity, uses_infrastructure

**Entity Distribution:**
- Products (3): ServiceFabric, PlatformDIGITAL, Data Gravity
- Facilities (8): DFW10, PHX10, DFW35, JFK10, MAA10, LAX10, AMS11, FRA12
- Cloud Providers (4): AWS, Azure, IBM, Google Cloud
- Technical Attributes (5): liquid cooling, rack, suite, redundancy, PUE
- Power Levels (3): 100KW, 200KW, 10MW

**Key Patterns:**
1. **ServiceFabric as Central Hub:** ServiceFabric node connects to 5 facilities and 4 cloud providers, reflecting its role as bridge between infrastructure and cloud connectivity
2. **DFW10 Dominance:** 19 mentions (3x more than next facility), positioned as primary hub
3. **Power-Infrastructure Correlation:** 100-200KW maps to racks/cabinets, 10MW maps to suites (building-level)
4. **Geographic Diversity:** US (DFW, PHX, JFK, LAX), Europe (FRA, AMS), Asia (MAA)

**Coverage:** Graph represents 85%+ of query patterns from top-frequency entities.

---

### 4. Failure Mode Taxonomy
**Status:** Complete

**5 Failure Categories Identified:**

**1. Out-of-Scope Usage (70% of all queries)**
- Description: Users requesting document manipulation, HR information, general chat
- Problem terms: edit, draft, create, excel, powerpoint, summarize
- Root cause: Expectation mismatch - users treat Nexus as general assistant
- Impact: Primary failure mode
- Recommendation: User education, scope clarification in onboarding

**2. No-Hit Failures (detected in responses)**
- Description: System cannot find relevant documents in any of 9 indexes
- Indicators: "I don't have", "I cannot find", "not available"
- Triggers: Specific technical specs not in knowledge base, new products, outdated info
- Recommendation: Content gap analysis, index refresh cadence

**3. Low-Confidence Responses (detected in responses)**
- Description: System hedges with uncertainty language
- Indicators: "I'm not sure", "I cannot confirm", "please verify"
- Meaning: Weak retrieval results or conflicting information
- Recommendation: Confidence threshold tuning, retrieval quality improvements

**4. Ambiguous Terms (6 identified)**
- Terms: fabric, capacity, site, cage, suite, available
- Example: "fabric" = ServiceFabric (product) vs network fabric (infrastructure)
- Example: "capacity" = power capacity (kW/MW) vs space capacity (racks/sqft)
- Recommendation: Context-aware disambiguation in query rewrite service

**5. Vague Queries (5 patterns)**
- Terms: best, good, better, compare, difference
- Issue: Missing specificity requiring clarification
- Recommendation: Clarifying questions, context gathering prompts

---

### 5. Baseline Performance Evaluation
**Status:** Complete  
**File:** `baseline_evaluation_results.csv`

**Test Set:** 19 representative queries across 3 in-scope clusters

**Overall Metrics:**
- **First-Answer Success Rate:** 68.4% (13/19 queries)
- **Citation Accuracy:** 74.4% average
  - Good: 13 queries
  - Partial: 4 queries
  - Poor: 2 queries
- **Response Latency:**
  - Average: 10.4 seconds
  - Median (P50): 8.4 seconds
  - P95: 25.2 seconds

**Performance by Cluster:**

| Cluster | Success Rate | Queries Tested |
|---------|--------------|----------------|
| Cluster 4 (ServiceFabric) | 100.0% | 6/6 |
| Cluster 2 (Power/Capacity) | 83.3% | 5/6 |
| Cluster 3 (Site Discovery) | 28.6% | 2/7 |

**Key Findings:**
1. **Strongest Performance:** ServiceFabric queries achieve 100% success - well-structured index, clear use cases
2. **Weakest Performance:** Site Discovery queries at 28.6% - suggests incomplete or fragmented data across indexes
3. **Main Failure Mode:** Missing or incomplete data in indexes (PUE ratings, comprehensive facility lists, certification details)

**Failed Queries Analysis:**
- "What data centers are in EMEA region?" - Returned raw database IDs instead of formatted list
- "List all Digital Realty facilities in California" - Only found 2 facilities (incomplete)
- "PUE ratings for Frankfurt data centers" - Said PUE values not available
- "Which sites have liquid cooling in AMER?" - Contradictory results across attempts
- "Data centers with Tier III certification in Europe" - Could not find certifications
- "What is the total capacity at Chicago facilities?" - Described sites but didn't sum totals

**Recommendations:**
1. Improve site discovery index completeness
2. Add structured aggregation for summary queries (totals, lists)
3. Include missing metadata (PUE, certifications, cooling types)

---

### 6. Entity Extraction Results
**Status:** Complete  
**File:** `entity_extraction_results.json`

**Extraction Methodology:** Hybrid NER + Custom Pattern Matching (95%+ accuracy)

**Entities Extracted from 537 In-Scope Queries:**

**Site Codes (64 unique):**
- Top: DFW10 (19 mentions), PHX10 (5), DFW35 (4), JFK10 (4), MAA10 (3)
- Coverage: 32x improvement over spaCy NER alone (detected only 2)
- Pattern: [A-Z]{3}\d{2,3}

**Products (77 total mentions):**
- ServiceFabric: 72 mentions (94% of all product queries)
- PlatformDIGITAL: 3 mentions
- Data Gravity: 2 mentions
- Other: DRIX, Metro Connect

**Cloud Providers (52 mentions):**
- AWS: 17 mentions (33%)
- IBM: 15 mentions (29%)
- Azure: 12 mentions (23%)
- Google Cloud: 6 mentions (12%)
- Oracle, others: 2 mentions (4%)

**Power Specifications (59 mentions, 29 unique):**
- Most common: 200KW (7x), 100KW (5x), 10MW (4x)
- Range: 5KW to 10MW
- Pattern: Cabinet-level (100-500KW), Building-level (1-10MW)

**Technical Attributes (110 mentions):**
- Liquid cooling: 19 mentions
- Rack: 24 mentions
- Suite: 12 mentions
- Redundancy: 18 mentions
- PUE: 8 mentions

**Key Insights:**
1. **ServiceFabric dominance:** 94% of product queries, will be densest ontology node
2. **DFW10 hub status:** 3x more mentions than any other facility
3. **Cloud provider concentration:** AWS + Azure + IBM = 85% of CSP mentions
4. **Liquid cooling interest:** 19 mentions signals high-density/AI workload demand

---

### 7. System Architecture Documentation
**Status:** Complete

**Current Retrieval Architecture:**
- Embedding Model: text-embedding-ada-002
- Retrieval Modes: BM25 + Hybrid + Semantic
- Reranking: Applied
- LLM: Production Nexus model

**9 Indexes Catalogued:**

1. **additional-properties**
   - Content: Physical/operational attributes of each data center
   - Coverage: Latitude, longitude, high density, NVIDIA certification, kW, white space, cooling

2. **certifications-index**
   - Content: Compliance and sustainability certifications by data center
   - Purpose: Track regulatory compliance per facility

3. **cloud-service-provider**
   - Content: Cloud service providers by metro/region
   - Coverage: On-ramp locations, connection methods

4. **datacenter-to-cloud-latency-by-nexport**
   - Content: Network latency metrics between DLR DCs and CSPs
   - Purpose: Performance benchmarking for hybrid cloud

5. **investment-dlr-legacy-current-nexgen-comparison**
   - Content: Hyperscaler investment requirements analysis
   - Purpose: Investment team decision support

6. **investment-key-customer-requirements**
   - Content: Hyperscaler requirements documentation
   - Purpose: Guide investment team on customer needs

7. **metro-connect-fiber-network**
   - Content: Metro Connect product specifications
   - Coverage: Metro campus connectivity, fiber details, latency

8. **nsp-index**
   - Content: Network service provider catalog
   - Coverage: Available providers by metro, campus connectivity

9. **nvidia-service-fabric-information**
   - Content: NVIDIA hardware and ServiceFabric documentation
   - Coverage: Product specs, user manuals, service descriptions

**Index Utilization Findings:**
- ServiceFabric queries: 100% success (well-structured index)
- Site discovery queries: 28.6% success (fragmented across multiple indexes)
- Power/capacity queries: 83.3% success (good coverage in additional-properties)

---

## Key Metrics Summary

### Data Analysis Metrics
- **Total conversations analyzed:** 3,550
- **Date range:** September 11 - November 11, 2025 (61 days)
- **Clean queries:** 2,691 (after filtering test users and junk)
- **In-scope queries:** 792 (30% of clean dataset)
- **Out-of-scope queries:** 1,878 (70% of clean dataset)

### Intent Classification Metrics
- **Final clusters:** 5 intent classes
- **Silhouette score:** 0.067 (42% improvement from initial clustering)
- **Dominant patterns:** 3 in-scope clusters representing 68% of clean queries

### Entity Metrics
- **Site codes extracted:** 64 unique
- **Most-queried facility:** DFW10 (19 mentions)
- **Most-queried product:** ServiceFabric (72 mentions, 94% of products)
- **Most-queried CSP:** AWS (17 mentions, 33% of CSPs)
- **Entity extraction accuracy:** 95%+ (hybrid NER + custom patterns)

### Baseline Performance Metrics
- **First-answer success:** 68.4%
- **Citation accuracy:** 74.4%
- **Average latency:** 10.4 seconds
- **Best performer:** ServiceFabric queries (100%)
- **Worst performer:** Site discovery queries (28.6%)

### Ontology Metrics
- **Total nodes:** 23 entities
- **Total edges:** 20 relationships
- **Coverage:** 85%+ of query patterns
- **Central hub:** ServiceFabric (9 connections)

---

## Critical Findings

### Finding 1: Massive Out-of-Scope Usage (70%)
**Issue:** Most users don't understand Nexus is a specialized data center tool.

**Evidence:**
- 1,878 of 2,691 queries (70%) request non-data-center services
- Common requests: Document creation, HR questions, general chat, text editing

**Impact:**
- Primary failure mode
- Resource waste on unanswerable queries
- User frustration and low satisfaction

**Root Cause:**
- Insufficient onboarding about system capabilities
- Users assume general-purpose AI assistant
- No clear scope communication

**Recommendation:**
- User education campaign
- Onboarding flow explaining what Nexus CAN and CANNOT do
- In-app guidance and example queries
- Graceful handling of out-of-scope requests with redirection

---

### Finding 2: ServiceFabric is the Star Product
**Evidence:**
- 72 of 77 product mentions (94%)
- 100% first-answer success rate in baseline testing
- Central hub in ontology with 9 connections

**Implications:**
- Well-understood by users
- Well-documented in indexes
- Clear use cases

**Recommendation:**
- Use as model for other products
- Expand similar coverage for Metro Connect, PlatformDIGITAL, DRIX

---

### Finding 3: Site Discovery Weakness (28.6% Success)
**Evidence:**
- Lowest cluster performance
- 5 of 7 test queries failed
- Common failures: EMEA region lists, California facilities, PUE ratings, certifications

**Root Cause:**
- Data fragmented across multiple indexes
- Missing aggregation capabilities
- Incomplete metadata (PUE, certifications)

**Recommendation:**
- Create unified site discovery index or view
- Add structured aggregation for list/summary queries
- Populate missing metadata fields

---

### Finding 4: Language Barrier (18% of Queries)
**Evidence:**
- 140 German-language queries cluster separately
- Language prevents content-based clustering

**Impact:**
- German users receive same poor experience as out-of-scope users
- Content-relevant queries misclassified

**Recommendation:**
- Translation layer for query preprocessing
- Language detection → translate to English → process → translate response back
- Or: Multilingual embedding model

---

### Finding 5: DFW10 Dominance
**Evidence:**
- 19 mentions (3x more than any other facility)
- Appears in power queries, ServiceFabric queries, site discovery queries

**Implications:**
- Dallas market is primary user focus
- DFW10 will be ontology hub node
- Representative test case for all query expansion work

**Recommendation:**
- Use DFW10 as primary test facility for Week 2 implementation
- Ensure comprehensive coverage in all indexes
- Model other facilities after DFW10 documentation quality

---

## Recommendations for Week 2

### Priority 1: Address Out-of-Scope Usage (Immediate)
**Actions:**
1. Create user onboarding flow explaining Nexus scope
2. Add in-app guidance with example queries
3. Implement graceful out-of-scope handling (explain what Nexus CAN help with)
4. Track out-of-scope categories for future feature expansion decisions

**Expected Impact:** Reduce wasted queries, improve user satisfaction, set proper expectations

---

### Priority 2: Implement Query Rewrite Service (Week 2 Core)
**Use Cases:**
1. **Synonym expansion:** "SF" → "ServiceFabric"
2. **Site code normalization:** "DFW" → "DFW10"
3. **Abbreviation expansion:** "EMEA" → "Europe, Middle East, Africa"
4. **Disambiguation:** Context-aware handling of "fabric", "capacity", "site"
5. **Unit normalization:** "5 MW" = "5000 KW" = "5 megawatts"

**Artifacts to Use:**
- Lexicon v0.1 (28 terms with synonyms)
- Entity extraction patterns (site codes, power specs)
- Disambiguation rules documented in lexicon

**Target Metrics:**
- ≤ 8 expansions per query
- Weight decay (1.0 → 0.6)
- ≤ 40ms p95 added latency

---

### Priority 3: Improve Site Discovery (Week 2 Enhancement)
**Actions:**
1. Audit all indexes for site-level metadata completeness
2. Add missing fields: PUE ratings, cooling types, certifications
3. Create aggregation layer for list/summary queries
4. Test EMEA/APAC/North America regional queries specifically

**Expected Impact:** Increase Site Discovery success from 28.6% to 70%+

---

### Priority 4: Implement Ontology-Aware Retrieval (Week 2 Core)
**Use Cases:**
1. If user asks about AWS connectivity → suggest ServiceFabric
2. If user asks about liquid cooling → route to facilities with that attribute
3. If user asks about power → understand relationship to rack/cabinet/suite

**Artifacts to Use:**
- Preliminary ontology graph (23 nodes, 20 edges)
- Relationship types: available_at, connects_to, has_attribute, offers_capacity, uses_infrastructure

**Expected Impact:** More intelligent query routing and suggestion capabilities

---

### Priority 5: Expand Lexicon Coverage (Ongoing)
**Current State:** 28 terms (10% of total entities)

**Week 2 Expansion Targets:**
- Add remaining 56 site codes (currently have DFW10, PHX10)
- Add synonyms for Metro Connect, PlatformDIGITAL, DRIX
- Add regional synonyms (AMER, Americas, US, North America, USA)
- Add technical attribute variations (chilled water = liquid cooling?)

**Target:** Lexicon v0.2 with 50-60 terms by end of Week 2

---

## Next Steps (Week 2 Implementation)

### Week 2 Focus: Operationalization
**Goal:** Turn Week 1 discoveries into production improvements

**Tasks:**
1. **Query Rewrite Service** (Days 1-3)
   - Implement lexicon-based expansion
   - Add disambiguation logic
   - Enforce latency/expansion constraints
   
2. **RAG Telemetry Hooks** (Days 2-4)
   - Log full trace: query → rewrite → retrieval → rerank → generation
   - Track rewrite impact on retrieval quality
   
3. **A/B Evaluation** (Days 3-5)
   - Route 10-20% traffic through expanded retriever
   - Measure lift in first-answer success
   - Compare against Week 1 baseline (68.4%)

4. **Index Utilization Dashboard** (Days 4-5)
   - Visualize which indexes serve which queries
   - Identify underutilized indexes
   - Track coverage gaps

**Success Criteria:**
- ≥ 10% lift in first-answer success (target: 75%+)
- Latency overhead ≤ 40ms p95
- ≥ 80% of high-value ontology nodes mapped to content

---

## Files Delivered

### Analysis Artifacts
1. `1_query_analysis.ipynb` - Complete analysis notebook
2. `1_query_analysis.html` - Stakeholder-friendly HTML export
3. `nexus_queries_final_clusters.csv` - Clustered query dataset
4. `baseline_evaluation_results.csv` - Test query results

### Knowledge Artifacts
5. `lexicon_v01_final.yaml` - 28-term controlled vocabulary
6. `preliminary_ontology_graph.png` - Visual ontology (23 nodes, 20 edges)
7. `entity_extraction_results.json` - Extracted entities with frequencies

### Documentation
8. `week1_summary_report.md` - This document
9. `week1_progress_log.md` - Detailed day-by-day log

---

## Conclusion

Week 1 successfully established a comprehensive baseline for the Nexus query system. The analysis revealed both strengths (excellent ServiceFabric coverage, strong power/capacity queries) and critical opportunities (70% out-of-scope usage, site discovery gaps).

The deliverables - lexicon, ontology, entity extraction, failure taxonomy, and baseline metrics - provide a solid foundation for Week 2 query expansion and ontology-driven retrieval improvements.

Most critically, I identified the primary failure mode: user expectation mismatch. 70% of users treat Nexus as a general assistant when it's designed as a specialized data center tool. Addressing this through user education and graceful scope handling will have the highest immediate impact on user satisfaction.

The Week 2 query rewrite service can target the remaining 30% in-scope users, where I measured 68.4% baseline success with clear improvement opportunities. With lexicon-based expansion and ontology-aware routing, a 10%+ lift to 75%+ success is achievable.

---

**Prepared by:** Nabih Sabeh  
**Date:** November 13, 2025  
**Project:** Enterprise Ontology & Query Expansion - Week 1 Discovery  
**Next Review:** Week 2 Implementation Kickoff
