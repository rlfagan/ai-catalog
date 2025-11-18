# AI Model Catalog

A comprehensive discovery and intelligence platform for AI models from HuggingFace. Search, explore lineage, compare quality, and make informed decisions about which models to use.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

## 🎯 Features

### Phase 1 (MVP - Current)
- **Smart Search**: Find models by task, size, license, language, and tags
- **Model Ancestry**: Visualize lineage trees showing base models and derivatives
- **Quality Comparison**: Compare derivatives with engagement metrics
- **Provenance Tracking**: See which datasets and base models were used

### Phase 2 (Planned)
- **Fork Recommender**: AI-powered suggestions for which model/version to use
- **Trending Detector**: Real-time tracking of hot models and categories
- **Quality Scoring**: Automated quality ratings based on engagement and derivatives

### Phase 3 (Planned)
- **License Validator**: Check commercial use compatibility
- **Compliance Reports**: Enterprise-grade model provenance reports
- **API Access**: Programmatic access for integration

## 📊 Data Insights

This catalog contains **331,992+ AI models** with:
- 3,429 unique base models with derivative tracking
- 1,320 multi-generation derivative chains
- 57,724 models with dataset provenance
- Coverage of 184+ languages

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│  - Search Interface                                  │
│  - Model Detail Pages                                │
│  - Ancestry Visualization (D3.js)                    │
└─────────────────┬───────────────────────────────────┘
                  │ REST API
┌─────────────────┴───────────────────────────────────┐
│              FastAPI Backend                         │
│  - Search Endpoints                                  │
│  - Model Details API                                 │
│  - Ancestry/Provenance API                           │
│  - Analytics Engine                                  │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────┐
│            PostgreSQL Database                       │
│  - Indexed model metadata                            │
│  - Provenance relationships                          │
│  - Full-text search                                  │
└──────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rlfagan/ai-catalog.git
   cd ai-catalog
   ```

2. **Place your data file**
   ```bash
   # Copy your hf_models.jsonl file to the root directory
   cp /path/to/hf_models.jsonl .
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec backend python scripts/init_db.py
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - API Health: http://localhost:8000/health

## 🔧 Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=aicat_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=aicat_db
DATABASE_URL=postgresql://aicat_user:your_secure_password@db:5432/aicat_db

# Backend
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## 📚 API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `GET /api/v1/search` - Search models with filters
- `GET /api/v1/models/{model_id}` - Get model details
- `GET /api/v1/models/{model_id}/ancestry` - Get model lineage
- `GET /api/v1/models/{model_id}/derivatives` - Get all derivatives
- `GET /api/v1/trending` - Get trending models
- `GET /api/v1/stats` - Get catalog statistics

See [API Documentation](./docs/API.md) for detailed endpoint specifications.

## 🗂️ Project Structure

```
ai-catalog/
├── backend/
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── scripts/
│   │   └── init_db.py      # Database initialization
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   └── App.js
│   ├── Dockerfile
│   └── package.json
├── docs/
│   ├── API.md              # API documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── DATA_MODEL.md       # Database schema
│   └── CONTRIBUTING.md     # Contribution guidelines
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Run all tests in Docker
docker-compose exec backend pytest
docker-compose exec frontend npm test
```

## 📈 Performance

- Database indexing on key fields (author, pipeline_tag, tags)
- Full-text search using PostgreSQL's tsvector
- API response caching with Redis (Phase 2)
- Lazy loading for ancestry trees

Expected performance:
- Search queries: < 100ms
- Model details: < 50ms
- Ancestry trees: < 200ms (with caching)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- HuggingFace for providing the model ecosystem
- Data sourced from HuggingFace model metadata
- Built with FastAPI, React, PostgreSQL, and Docker

## 📧 Contact

- GitHub Issues: [https://github.com/rlfagan/ai-catalog/issues](https://github.com/rlfagan/ai-catalog/issues)
- Project Link: [https://github.com/rlfagan/ai-catalog](https://github.com/rlfagan/ai-catalog)

## 🗺️ Roadmap

- [x] Phase 1: MVP with search and ancestry
- [ ] Phase 2: Intelligence features (recommendations, trending)
- [ ] Phase 3: Commercial features (licensing, compliance)
- [ ] Phase 4: Marketplace (deployment, monetization)

## 📊 Data Statistics

```
Total Models:        331,992
Base Models:         3,429
With Provenance:     34,682 (10.3%)
With Datasets:       57,724 (17.1%)
Multi-gen Chains:    1,320
Languages:           184+
Pipeline Types:      30+
```

---

**Made with ❤️ for the AI community**
