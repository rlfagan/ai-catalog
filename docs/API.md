# API Documentation

Base URL: `http://localhost:8000/api/v1`

## Authentication

Phase 1 (MVP): No authentication required
Phase 3: API key authentication for rate limiting and premium features

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

---

### Search Models

#### GET /api/v1/search

Search for models with various filters.

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | No | Search query (searches id, author, tags) |
| `pipeline_tag` | string | No | Filter by pipeline type (e.g., "text-generation") |
| `library` | string | No | Filter by library (e.g., "transformers") |
| `license` | string | No | Filter by license (e.g., "apache-2.0") |
| `language` | string | No | Filter by language (e.g., "en", "zh") |
| `min_likes` | integer | No | Minimum number of likes |
| `min_downloads` | integer | No | Minimum number of downloads |
| `has_base_model` | boolean | No | Filter models with/without base model |
| `sort_by` | string | No | Sort field: "likes", "downloads", "trending", "created_at" (default: "trending") |
| `order` | string | No | Sort order: "asc" or "desc" (default: "desc") |
| `page` | integer | No | Page number (default: 1) |
| `per_page` | integer | No | Results per page (default: 20, max: 100) |

**Example Request**
```bash
GET /api/v1/search?q=llama&pipeline_tag=text-generation&min_likes=100&sort_by=likes&per_page=10
```

**Response**
```json
{
  "total": 245,
  "page": 1,
  "per_page": 10,
  "total_pages": 25,
  "results": [
    {
      "id": "meta-llama/Llama-3.1-8B",
      "author": "meta-llama",
      "pipeline_tag": "text-generation",
      "library_name": "transformers",
      "likes": 4947,
      "downloads": 10587714,
      "trending_score": 513,
      "created_at": "2024-07-23T10:30:00Z",
      "last_modified": "2024-11-15T14:22:00Z",
      "tags": ["transformers", "pytorch", "llama", "text-generation"],
      "has_base_model": false,
      "derivative_count": 24,
      "gated": false,
      "license": "llama3.1"
    }
  ]
}
```

---

### Get Model Details

#### GET /api/v1/models/{model_id}

Get detailed information about a specific model.

**Path Parameters**
- `model_id`: URL-encoded model ID (e.g., `meta-llama%2FLlama-3.1-8B`)

**Example Request**
```bash
GET /api/v1/models/meta-llama%2FLlama-3.1-8B
```

**Response**
```json
{
  "id": "meta-llama/Llama-3.1-8B",
  "author": "meta-llama",
  "pipeline_tag": "text-generation",
  "library_name": "transformers",
  "likes": 4947,
  "downloads": 10587714,
  "downloads_all_time": null,
  "trending_score": 513,
  "created_at": "2024-07-23T10:30:00Z",
  "last_modified": "2024-11-15T14:22:00Z",
  "tags": ["transformers", "pytorch", "llama", "text-generation", "license:llama3.1"],
  "gated": false,
  "private": false,
  "siblings": [
    {
      "filename": "model.safetensors",
      "size": 16000000000
    }
  ],
  "base_model": null,
  "base_model_relation": null,
  "datasets": ["wikipedia", "common_crawl"],
  "derivative_count": 24,
  "security_repo_status": null,
  "license": "llama3.1"
}
```

---

### Get Model Ancestry

#### GET /api/v1/models/{model_id}/ancestry

Get the full lineage tree of a model (parents and grandparents).

**Path Parameters**
- `model_id`: URL-encoded model ID

**Example Request**
```bash
GET /api/v1/models/unsloth%2Fllama-3.1-8B-bnb-4bit/ancestry
```

**Response**
```json
{
  "model_id": "unsloth/llama-3.1-8B-bnb-4bit",
  "lineage": [
    {
      "id": "meta-llama/Llama-3.1-8B",
      "relation": "base_model",
      "generation": 1,
      "author": "meta-llama",
      "likes": 4947,
      "downloads": 10587714
    },
    {
      "id": "unsloth/llama-3.1-8B-bnb-4bit",
      "relation": "quantized",
      "generation": 2,
      "author": "unsloth",
      "likes": 523,
      "downloads": 125430
    }
  ],
  "depth": 2,
  "root_model": "meta-llama/Llama-3.1-8B"
}
```

---

### Get Model Derivatives

#### GET /api/v1/models/{model_id}/derivatives

Get all models that were derived from this model.

**Path Parameters**
- `model_id`: URL-encoded model ID

**Query Parameters**
- `relation_type`: Filter by relation type ("finetune", "adapter", "quantized", "merge")
- `min_likes`: Minimum likes
- `sort_by`: Sort field (default: "likes")
- `limit`: Max results (default: 50)

**Example Request**
```bash
GET /api/v1/models/meta-llama%2FLlama-3.1-8B/derivatives?relation_type=quantized&min_likes=10
```

**Response**
```json
{
  "base_model": "meta-llama/Llama-3.1-8B",
  "total_derivatives": 24,
  "derivatives": [
    {
      "id": "unsloth/llama-3.1-8B-bnb-4bit",
      "author": "unsloth",
      "relation": "quantized",
      "likes": 523,
      "downloads": 125430,
      "created_at": "2024-08-05T09:15:00Z",
      "tags": ["gguf", "quantized", "4bit"]
    },
    {
      "id": "bartowski/llama-3.1-8B-GGUF",
      "author": "bartowski",
      "relation": "quantized",
      "likes": 412,
      "downloads": 98234,
      "created_at": "2024-08-10T14:30:00Z",
      "tags": ["gguf", "quantized"]
    }
  ]
}
```

---

### Get Trending Models

#### GET /api/v1/trending

Get currently trending models.

**Query Parameters**
- `pipeline_tag`: Filter by pipeline type
- `timeframe`: "day", "week", "month" (default: "week")
- `limit`: Number of results (default: 20, max: 100)

**Example Request**
```bash
GET /api/v1/trending?pipeline_tag=text-generation&limit=10
```

**Response**
```json
{
  "timeframe": "week",
  "updated_at": "2025-11-18T12:00:00Z",
  "models": [
    {
      "id": "moonshotai/Kimi-K2-Thinking",
      "author": "moonshotai",
      "pipeline_tag": "text-generation",
      "trending_score": 451,
      "likes": 1223,
      "downloads": 141717,
      "growth_rate": 0.35,
      "rank": 1,
      "rank_change": 0
    }
  ]
}
```

---

### Get Catalog Statistics

#### GET /api/v1/stats

Get overall statistics about the catalog.

**Response**
```json
{
  "total_models": 331992,
  "total_authors": 45213,
  "total_organizations": 3421,
  "pipeline_types": {
    "text-classification": 30607,
    "text-generation": 28189,
    "text-to-image": 12448
  },
  "top_libraries": {
    "transformers": 140016,
    "diffusers": 12731,
    "peft": 7204
  },
  "total_derivatives": 34682,
  "avg_derivatives_per_base": 10.1,
  "models_with_datasets": 57724,
  "languages_supported": 184,
  "last_updated": "2025-11-18T12:00:00Z"
}
```

---

### Get Author Details

#### GET /api/v1/authors/{author_name}

Get information about a specific author and their models.

**Path Parameters**
- `author_name`: Author username

**Query Parameters**
- `include_models`: Include model list (default: true)
- `limit`: Max models to return (default: 20)

**Example Request**
```bash
GET /api/v1/authors/meta-llama?limit=5
```

**Response**
```json
{
  "author": "meta-llama",
  "total_models": 34,
  "total_likes": 15234,
  "total_downloads": 45632123,
  "specialization": {
    "text-generation": 32,
    "text-classification": 2
  },
  "is_organization": true,
  "derivative_count": 245,
  "models": [
    {
      "id": "meta-llama/Llama-3.1-8B",
      "likes": 4947,
      "downloads": 10587714
    }
  ]
}
```

---

### Get Dataset Impact

#### GET /api/v1/datasets/{dataset_name}/impact

Get models trained on a specific dataset and their performance.

**Path Parameters**
- `dataset_name`: Dataset identifier

**Example Request**
```bash
GET /api/v1/datasets/openorca/impact
```

**Response**
```json
{
  "dataset": "openorca",
  "total_models": 236,
  "unique_authors": 119,
  "avg_likes": 18.2,
  "avg_downloads": 234567,
  "top_models": [
    {
      "id": "openchat/openchat-3.5",
      "likes": 1523,
      "downloads": 3456789
    }
  ]
}
```

---

## Error Responses

All endpoints return standard HTTP status codes:

### 400 Bad Request
```json
{
  "error": "Invalid parameter",
  "message": "per_page must be between 1 and 100",
  "code": "INVALID_PARAMETER"
}
```

### 404 Not Found
```json
{
  "error": "Model not found",
  "message": "Model 'invalid/model-id' does not exist",
  "code": "MODEL_NOT_FOUND"
}
```

### 429 Too Many Requests (Phase 3)
```json
{
  "error": "Rate limit exceeded",
  "message": "API rate limit exceeded. Upgrade to premium for higher limits.",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR",
  "request_id": "req_abc123"
}
```

---

## Rate Limiting (Phase 3)

- Free tier: 100 requests/hour
- Premium tier: 10,000 requests/hour
- Enterprise: Custom limits

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1637265600
```

---

## Pagination

All list endpoints support pagination:

**Request**
```bash
GET /api/v1/search?page=2&per_page=20
```

**Response Headers**
```
Link: <http://localhost:8000/api/v1/search?page=3&per_page=20>; rel="next",
      <http://localhost:8000/api/v1/search?page=1&per_page=20>; rel="prev",
      <http://localhost:8000/api/v1/search?page=25&per_page=20>; rel="last"
X-Total-Count: 500
X-Page: 2
X-Per-Page: 20
X-Total-Pages: 25
```

---

## Filtering Best Practices

1. **Use specific filters** to reduce response size
2. **Combine filters** for targeted results
3. **Use pagination** for large result sets
4. **Cache responses** when appropriate

**Example: Find production-ready text generation models**
```bash
GET /api/v1/search?pipeline_tag=text-generation&min_likes=100&license=apache-2.0&has_base_model=false&sort_by=downloads
```
