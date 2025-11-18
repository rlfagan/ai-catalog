# System Architecture

## Overview

AI Model Catalog is a full-stack web application designed to help users discover, explore, and analyze AI models from HuggingFace. The system prioritizes performance, scalability, and developer experience.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          Client Layer                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  React Single Page Application (SPA)                      │   │
│  │  - Search Interface                                       │   │
│  │  - Model Detail Pages                                     │   │
│  │  - Ancestry Visualization (D3.js / react-flow)            │   │
│  │  - Charts & Analytics (Recharts)                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST (JSON)
                         │
┌────────────────────────┴────────────────────────────────────────┐
│                      API Gateway Layer                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  NGINX Reverse Proxy                                      │   │
│  │  - Route requests to backend                              │   │
│  │  - SSL termination                                        │   │
│  │  - Static file serving                                    │   │
│  │  - Compression (gzip)                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────────┐
│                     Application Layer                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI Backend (Python 3.11)                            │   │
│  │                                                            │   │
│  │  ┌─────────────────────────────────────────────────┐     │   │
│  │  │  API Routes (/api/v1/*)                         │     │   │
│  │  │  - Search                                        │     │   │
│  │  │  - Model Details                                 │     │   │
│  │  │  - Ancestry                                      │     │   │
│  │  │  - Trending                                      │     │   │
│  │  │  - Statistics                                    │     │   │
│  │  └─────────────────────────────────────────────────┘     │   │
│  │                                                            │   │
│  │  ┌─────────────────────────────────────────────────┐     │   │
│  │  │  Business Logic (Services)                       │     │   │
│  │  │  - SearchService                                 │     │   │
│  │  │  - ModelService                                  │     │   │
│  │  │  - ProvenanceService                             │     │   │
│  │  │  - AnalyticsService                              │     │   │
│  │  └─────────────────────────────────────────────────┘     │   │
│  │                                                            │   │
│  │  ┌─────────────────────────────────────────────────┐     │   │
│  │  │  Data Access Layer (Repository Pattern)          │     │   │
│  │  │  - ModelRepository                               │     │   │
│  │  │  - ProvenanceRepository                          │     │   │
│  │  └─────────────────────────────────────────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │ SQLAlchemy ORM
┌────────────────────────┴────────────────────────────────────────┐
│                       Data Layer                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  PostgreSQL 15                                            │   │
│  │                                                            │   │
│  │  Tables:                                                   │   │
│  │  - models (main model metadata)                           │   │
│  │  - model_tags (normalized tags)                           │   │
│  │  - model_siblings (file information)                      │   │
│  │  - base_model_relations (provenance)                      │   │
│  │  - dataset_relations (training data)                      │   │
│  │                                                            │   │
│  │  Indexes:                                                  │   │
│  │  - Full-text search (GIN index on tsvector)              │   │
│  │  - B-tree indexes on filters (author, pipeline_tag)       │   │
│  │  - Composite indexes for common queries                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      Supporting Services                          │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │ Redis Cache    │  │ Background     │  │ Monitoring       │   │
│  │ (Phase 2)      │  │ Jobs (Phase 2) │  │ (Phase 2)        │   │
│  │ - API caching  │  │ - Data updates │  │ - Prometheus     │   │
│  │ - Rate limiting│  │ - Trending calc│  │ - Grafana        │   │
│  └────────────────┘  └────────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: React 18
- **Language**: JavaScript/TypeScript
- **UI Library**: Material-UI / TailwindCSS
- **State Management**: React Context / Redux Toolkit (if needed)
- **Data Visualization**:
  - D3.js for ancestry trees
  - Recharts for charts
  - react-flow for network diagrams
- **HTTP Client**: Axios
- **Build Tool**: Create React App / Vite

### Backend
- **Framework**: FastAPI (Python 3.11)
- **ORM**: SQLAlchemy 2.0
- **Database Driver**: asyncpg
- **Validation**: Pydantic
- **API Documentation**: OpenAPI/Swagger (automatic)
- **Testing**: pytest, pytest-asyncio

### Database
- **Primary**: PostgreSQL 15
- **Features Used**:
  - Full-text search (tsvector/tsquery)
  - JSON/JSONB for flexible metadata
  - Array types for tags
  - Materialized views for analytics

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Reverse Proxy**: NGINX (Phase 2)
- **Caching**: Redis (Phase 2)
- **CI/CD**: GitHub Actions
- **Hosting**: AWS/DigitalOcean/Render (TBD)

## Data Model

### Core Entities

#### models
Primary table storing model metadata.

```sql
CREATE TABLE models (
    id VARCHAR(500) PRIMARY KEY,  -- e.g., "meta-llama/Llama-3.1-8B"
    author VARCHAR(255) NOT NULL,
    modelId VARCHAR(500) NOT NULL,  -- redundant but useful
    pipeline_tag VARCHAR(100),
    library_name VARCHAR(100),
    likes INTEGER DEFAULT 0,
    downloads BIGINT DEFAULT 0,
    downloads_all_time BIGINT,
    trending_score FLOAT DEFAULT 0,
    created_at TIMESTAMP,
    last_modified TIMESTAMP,
    gated BOOLEAN DEFAULT FALSE,
    private BOOLEAN DEFAULT FALSE,
    sha VARCHAR(100),
    security_repo_status VARCHAR(50),

    -- Full-text search
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(id, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(author, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(pipeline_tag, '')), 'C')
    ) STORED,

    -- Computed fields
    has_base_model BOOLEAN DEFAULT FALSE,
    derivative_count INTEGER DEFAULT 0,

    -- Metadata JSON
    metadata JSONB,

    -- Timestamps
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_models_author ON models(author);
CREATE INDEX idx_models_pipeline_tag ON models(pipeline_tag);
CREATE INDEX idx_models_library ON models(library_name);
CREATE INDEX idx_models_likes ON models(likes DESC);
CREATE INDEX idx_models_downloads ON models(downloads DESC);
CREATE INDEX idx_models_trending ON models(trending_score DESC);
CREATE INDEX idx_models_search ON models USING GIN(search_vector);
CREATE INDEX idx_models_created ON models(created_at DESC);
```

#### model_tags
Normalized tags for efficient filtering.

```sql
CREATE TABLE model_tags (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(500) REFERENCES models(id) ON DELETE CASCADE,
    tag VARCHAR(200) NOT NULL,
    tag_type VARCHAR(50),  -- 'license', 'language', 'framework', 'general'

    UNIQUE(model_id, tag)
);

CREATE INDEX idx_tags_model ON model_tags(model_id);
CREATE INDEX idx_tags_tag ON model_tags(tag);
CREATE INDEX idx_tags_type ON model_tags(tag_type);
```

#### base_model_relations
Tracks provenance relationships.

```sql
CREATE TABLE base_model_relations (
    id SERIAL PRIMARY KEY,
    derivative_id VARCHAR(500) REFERENCES models(id) ON DELETE CASCADE,
    base_model_id VARCHAR(500) NOT NULL,  -- May not exist in our DB
    relation_type VARCHAR(50),  -- 'finetune', 'adapter', 'quantized', 'merge'

    UNIQUE(derivative_id, base_model_id)
);

CREATE INDEX idx_relations_derivative ON base_model_relations(derivative_id);
CREATE INDEX idx_relations_base ON base_model_relations(base_model_id);
CREATE INDEX idx_relations_type ON base_model_relations(relation_type);
```

#### dataset_relations
Tracks training data provenance.

```sql
CREATE TABLE dataset_relations (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(500) REFERENCES models(id) ON DELETE CASCADE,
    dataset_name VARCHAR(500) NOT NULL,

    UNIQUE(model_id, dataset_name)
);

CREATE INDEX idx_datasets_model ON dataset_relations(model_id);
CREATE INDEX idx_datasets_name ON dataset_relations(dataset_name);
```

#### model_siblings
File information for models.

```sql
CREATE TABLE model_siblings (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(500) REFERENCES models(id) ON DELETE CASCADE,
    filename VARCHAR(500) NOT NULL,
    size BIGINT,
    blob_id VARCHAR(100),
    lfs BOOLEAN
);

CREATE INDEX idx_siblings_model ON model_siblings(model_id);
CREATE INDEX idx_siblings_filename ON model_siblings(filename);
```

### Materialized Views (Phase 2)

For expensive analytics queries:

```sql
-- Top authors by total engagement
CREATE MATERIALIZED VIEW author_stats AS
SELECT
    author,
    COUNT(*) as model_count,
    SUM(likes) as total_likes,
    SUM(downloads) as total_downloads,
    AVG(trending_score) as avg_trending
FROM models
GROUP BY author;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY author_stats;
```

## API Design Principles

### RESTful Conventions
- Use nouns for resources (`/models`, `/authors`)
- Use HTTP verbs correctly (GET, POST, PUT, DELETE)
- Use proper status codes
- Version the API (`/api/v1`)

### Response Format
All responses follow this structure:

**Success**
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

**Error**
```json
{
  "error": {
    "code": "MODEL_NOT_FOUND",
    "message": "Model not found",
    "details": { ... }
  }
}
```

### Performance Optimizations

1. **Database Query Optimization**
   - Use indexes on all filter columns
   - Limit result sets with pagination
   - Use EXPLAIN ANALYZE to optimize queries
   - Connection pooling (SQLAlchemy)

2. **API Response Caching** (Phase 2)
   - Redis caching for frequent queries
   - ETag headers for conditional requests
   - Cache invalidation on data updates

3. **Frontend Optimization**
   - Code splitting
   - Lazy loading for ancestry trees
   - Virtual scrolling for long lists
   - Asset compression (gzip, brotli)

## Security Considerations

### Phase 1 (Current)
- Input validation with Pydantic
- SQL injection prevention (ORM)
- CORS configuration
- Rate limiting (basic)

### Phase 2
- API key authentication
- JWT tokens for sessions
- Rate limiting per user/IP

### Phase 3
- OAuth2 integration
- Role-based access control (RBAC)
- Audit logging
- Data encryption at rest

## Scalability Strategy

### Horizontal Scaling
- Stateless API servers (scale with load balancer)
- Read replicas for PostgreSQL
- CDN for static assets

### Vertical Scaling
- Database connection pooling
- Async I/O (FastAPI + asyncpg)
- Database partitioning (by date/author)

### Caching Strategy (Phase 2)
```
Request Flow:
1. Check Redis cache
2. If miss, query database
3. Store in Redis (TTL: 5 minutes for search, 1 hour for model details)
4. Return response
```

## Monitoring & Observability (Phase 2)

### Metrics
- API request latency (p50, p95, p99)
- Database query performance
- Error rates
- Cache hit rates

### Logging
- Structured JSON logs
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request tracing

### Alerting
- API downtime
- High error rates
- Database connection issues
- Disk space warnings

## Deployment Strategy

### Development
```bash
docker-compose up
```

### Staging
- Deploy to DigitalOcean/AWS
- Automatic deployment on `develop` branch
- Database seeding with subset of data

### Production
- Blue-green deployment
- Database migrations with Alembic
- Zero-downtime deployments
- Automated backups

## Testing Strategy

### Backend Testing
```python
# Unit tests
tests/unit/services/test_search_service.py
tests/unit/repositories/test_model_repository.py

# Integration tests
tests/integration/test_api_search.py
tests/integration/test_database.py

# End-to-end tests
tests/e2e/test_search_flow.py
```

### Frontend Testing
```javascript
// Component tests
src/components/__tests__/SearchBar.test.js

// Integration tests
src/pages/__tests__/ModelDetail.test.js

// E2E tests (Cypress/Playwright)
cypress/e2e/search.cy.js
```

### Test Coverage Goals
- Backend: > 80%
- Frontend: > 70%
- Critical paths: 100%

## Future Enhancements

### Phase 2
- Real-time updates (WebSockets)
- Advanced analytics dashboard
- Model comparison tool
- User accounts & saved searches

### Phase 3
- ML-powered recommendations
- Automated model quality scoring
- Integration with HF Inference API
- Community features (comments, ratings)

### Phase 4
- Multi-cloud deployment
- GraphQL API
- Mobile apps (React Native)
- Enterprise features (SSO, audit logs)
