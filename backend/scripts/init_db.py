"""
Database initialization script
Parses JSONL file and populates PostgreSQL database
"""

import json
import sys
import os
from datetime import datetime
import logging
import re

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Model, ModelTag, BaseModelRelation, DatasetRelation, ModelSibling
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_timestamp(ts_str):
    """Parse timestamp string to datetime"""
    if not ts_str:
        return None
    try:
        # Remove timezone info for simplicity
        ts_str = ts_str.replace('+00:00', '')
        return datetime.fromisoformat(ts_str)
    except:
        return None


def parse_siblings(siblings_data):
    """Parse siblings data from string representation"""
    if not siblings_data:
        return []

    try:
        # If it's already a list
        if isinstance(siblings_data, list):
            return siblings_data

        # If it's a string representation
        if isinstance(siblings_data, str):
            # Extract filenames using regex
            pattern = r"rfilename='([^']+)'"
            filenames = re.findall(pattern, siblings_data)
            return [{"filename": f} for f in filenames]

        return []
    except:
        return []


def categorize_tag(tag):
    """Categorize a tag by type"""
    if tag.startswith('license:'):
        return 'license'
    elif tag.startswith('dataset:'):
        return 'dataset'
    elif len(tag) == 2 and tag.isalpha():
        return 'language'
    elif tag in ['transformers', 'diffusers', 'peft', 'pytorch', 'tensorflow', 'jax']:
        return 'framework'
    else:
        return 'general'


def init_database():
    """Initialize database and create tables"""
    logger.info("Initializing database...")

    # Create engine with synchronous driver for setup
    db_url = settings.database_url_computed.replace('asyncpg', 'psycopg2')
    logger.info(f"Connecting to database: {db_url.split('@')[1]}")  # Hide credentials

    engine = create_engine(db_url, echo=False)

    # Create tables
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully")

    return engine


def load_data(engine, data_file):
    """Load data from JSONL file into database"""
    logger.info(f"Loading data from {data_file}...")

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        total_lines = 0
        processed = 0
        errors = 0
        batch_size = 1000
        models_batch = []

        with open(data_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1

                if total_lines % 10000 == 0:
                    logger.info(f"Processed {total_lines} lines...")

                try:
                    data = json.loads(line.strip())

                    # Create Model object
                    model = Model(
                        id=data.get('id'),
                        author=data.get('author'),
                        model_id=data.get('modelId') or data.get('id'),
                        pipeline_tag=data.get('pipeline_tag'),
                        library_name=data.get('library_name'),
                        likes=data.get('likes', 0) or 0,
                        downloads=data.get('downloads', 0) or 0,
                        downloads_all_time=data.get('downloads_all_time'),
                        trending_score=data.get('trending_score', 0) or 0,
                        created_at=parse_timestamp(data.get('created_at')),
                        last_modified=parse_timestamp(data.get('last_modified') or data.get('lastModified')),
                        gated=data.get('gated', False) or False,
                        private=data.get('private', False) or False,
                        sha=data.get('sha'),
                        security_repo_status=data.get('security_repo_status'),
                        has_base_model=False,  # Will update when processing tags
                        derivative_count=0,
                        metadata=data  # Store full JSON
                    )

                    models_batch.append((model, data))
                    processed += 1

                    # Batch insert
                    if len(models_batch) >= batch_size:
                        insert_batch(session, models_batch)
                        models_batch = []

                except Exception as e:
                    errors += 1
                    if errors <= 10:  # Log first 10 errors
                        logger.error(f"Error on line {line_num}: {e}")

        # Insert remaining models
        if models_batch:
            insert_batch(session, models_batch)

        session.commit()
        logger.info(f"Data loading complete!")
        logger.info(f"Total lines: {total_lines}")
        logger.info(f"Successfully processed: {processed}")
        logger.info(f"Errors: {errors}")

    except Exception as e:
        logger.error(f"Fatal error during data loading: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def insert_batch(session, models_batch):
    """Insert a batch of models with related data"""
    for model, data in models_batch:
        try:
            # Add model
            session.add(model)
            session.flush()  # Get the ID

            # Add tags
            tags = data.get('tags', [])
            if tags:
                base_model_tags = []
                dataset_tags = []

                for tag in tags:
                    tag_type = categorize_tag(tag)

                    # Create tag entry
                    model_tag = ModelTag(
                        model_id=model.id,
                        tag=tag,
                        tag_type=tag_type
                    )
                    session.add(model_tag)

                    # Track base model and dataset tags for separate tables
                    if tag.startswith('base_model:'):
                        base_model_tags.append(tag)
                        model.has_base_model = True
                    elif tag.startswith('dataset:'):
                        dataset_tags.append(tag)

                # Process base model relations
                for tag in base_model_tags:
                    parts = tag.replace('base_model:', '').split(':')
                    if len(parts) >= 2:
                        relation_type = parts[0]
                        base_model_id = ':'.join(parts[1:])
                    else:
                        relation_type = 'unknown'
                        base_model_id = parts[0]

                    relation = BaseModelRelation(
                        derivative_id=model.id,
                        base_model_id=base_model_id,
                        relation_type=relation_type
                    )
                    session.add(relation)

                # Process dataset relations
                for tag in dataset_tags:
                    dataset_name = tag.replace('dataset:', '')
                    dataset_rel = DatasetRelation(
                        model_id=model.id,
                        dataset_name=dataset_name
                    )
                    session.add(dataset_rel)

            # Add siblings (file information)
            siblings = parse_siblings(data.get('siblings'))
            for sib in siblings[:50]:  # Limit to first 50 files
                if isinstance(sib, dict) and 'filename' in sib:
                    sibling = ModelSibling(
                        model_id=model.id,
                        filename=sib['filename'],
                        size=sib.get('size'),
                        blob_id=sib.get('blob_id'),
                        lfs=sib.get('lfs')
                    )
                    session.add(sibling)

        except Exception as e:
            logger.error(f"Error inserting model {model.id}: {e}")


def update_derivative_counts(engine):
    """Update derivative counts for base models"""
    logger.info("Updating derivative counts...")

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Update counts using raw SQL for efficiency
        session.execute("""
            UPDATE models
            SET derivative_count = (
                SELECT COUNT(*)
                FROM base_model_relations
                WHERE base_model_relations.base_model_id = models.id
            )
        """)
        session.commit()
        logger.info("Derivative counts updated")
    except Exception as e:
        logger.error(f"Error updating derivative counts: {e}")
        session.rollback()
    finally:
        session.close()


def main():
    """Main execution"""
    logger.info("=" * 60)
    logger.info("AI Model Catalog - Database Initialization")
    logger.info("=" * 60)

    # Check if data file exists
    data_file = settings.DATA_FILE_PATH
    if not os.path.exists(data_file):
        logger.error(f"Data file not found: {data_file}")
        logger.error("Please place hf_models.jsonl in the data directory")
        sys.exit(1)

    # Initialize database
    engine = init_database()

    # Load data
    load_data(engine, data_file)

    # Update derivative counts
    update_derivative_counts(engine)

    logger.info("=" * 60)
    logger.info("Database initialization complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
