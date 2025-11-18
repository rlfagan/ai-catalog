# Quick Start Guide

Get your AI Model Catalog up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- The `hf_models.jsonl` data file (465MB)

## Step-by-Step Setup

### 1. Verify Your Setup

```bash
# Check if Docker is running
docker --version
docker-compose --version

# Verify you're in the project directory
ls -la
# You should see: docker-compose.yml, backend/, frontend/, etc.

# Verify data file exists
ls -lh hf_models.jsonl
# Should show ~465MB file
```

### 2. Start the Services

```bash
# Start all containers (PostgreSQL, Backend, Frontend)
docker-compose up -d

# Check that all services are running
docker-compose ps
```

You should see 3 services: `aicat_db`, `aicat_backend`, `aicat_frontend`

### 3. Initialize the Database

This step loads the 331,992 models from the JSONL file into PostgreSQL.

**⚠️ Warning: This will take 10-20 minutes depending on your hardware!**

```bash
# Start the database initialization
docker-compose exec backend python scripts/init_db.py
```

You'll see progress logs like:
```
Processed 10000 lines...
Processed 20000 lines...
...
```

### 4. Access the Application

Once initialization is complete:

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Try Your First Search

1. Open http://localhost:3000
2. Search for "llama text-generation"
3. Click on a model to see details
4. Explore trending models!

## Common Issues & Solutions

### Port Already in Use

If ports 3000, 5432, or 8000 are already in use:

```bash
# Stop the conflicting service, or modify docker-compose.yml
# Change port mappings like "3001:3000" instead of "3000:3000"
```

### Database Connection Failed

```bash
# Check if PostgreSQL is healthy
docker-compose logs db

# Restart the database
docker-compose restart db

# Wait 10 seconds and try again
```

### Data File Not Found

```bash
# Ensure hf_models.jsonl is in the project root
cp /path/to/hf_models.jsonl .

# Restart backend to remount the volume
docker-compose restart backend
```

### Frontend Can't Connect to Backend

```bash
# Check if backend is running
docker-compose logs backend

# Verify API health
curl http://localhost:8000/health

# Check CORS settings in backend/app/core/config.py
```

## Useful Commands

```bash
# View logs
docker-compose logs -f backend    # Backend logs
docker-compose logs -f frontend   # Frontend logs
docker-compose logs -f db         # Database logs

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove all data (⚠️ WARNING: Deletes database!)
docker-compose down -v

# Rebuild containers after code changes
docker-compose up -d --build

# Access database directly
docker-compose exec db psql -U aicat_user -d aicat_db

# Execute bash in backend container
docker-compose exec backend bash

# Check database size
docker-compose exec db psql -U aicat_user -d aicat_db -c "\l+"
```

## Development Workflow

### Backend Development

```bash
# Edit files in backend/
# Changes auto-reload (FastAPI --reload flag)

# Run tests
docker-compose exec backend pytest

# Format code
docker-compose exec backend black app/
```

### Frontend Development

```bash
# Edit files in frontend/src/
# Changes auto-reload (React dev server)

# Install new package
docker-compose exec frontend npm install <package>

# Run tests
docker-compose exec frontend npm test
```

### Database Changes

```bash
# After modifying backend/app/db/models.py:

# 1. Stop services
docker-compose down

# 2. Remove database volume (⚠️ data loss!)
docker volume rm hfdata_postgres_data

# 3. Restart and reinitialize
docker-compose up -d
docker-compose exec backend python scripts/init_db.py
```

## Performance Tips

### Faster Database Initialization

If you need to reinitialize frequently during development:

```bash
# Create a backup after first initialization
docker-compose exec db pg_dump -U aicat_user aicat_db > backup.sql

# Restore from backup (much faster!)
docker-compose exec -T db psql -U aicat_user -d aicat_db < backup.sql
```

### Optimize PostgreSQL

Edit `docker-compose.yml` and add under `db` service:

```yaml
environment:
  POSTGRES_SHARED_BUFFERS: 256MB
  POSTGRES_WORK_MEM: 8MB
```

## Next Steps

1. **Implement Real Search**: Edit `backend/app/api/v1.py` to query the database
2. **Add Filters**: Implement pipeline_tag, license, language filters
3. **Build Ancestry Tree**: Create provenance visualization with D3.js
4. **Add Analytics**: Implement trending calculation and statistics

## Need Help?

- Check the full [README.md](./README.md)
- Read [API Documentation](./docs/API.md)
- Review [Architecture](./docs/ARCHITECTURE.md)
- Open an issue on GitHub

---

**Happy Coding!** 🚀
