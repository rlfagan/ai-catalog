"""
Database models using SQLAlchemy
"""

from sqlalchemy import Column, String, Integer, BigInteger, Float, Boolean, TIMESTAMP, ForeignKey, Text, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Model(Base):
    """Main model metadata table"""
    __tablename__ = "models"

    id = Column(String(500), primary_key=True, index=True)
    author = Column(String(255), nullable=False, index=True)
    model_id = Column(String(500), nullable=False)
    pipeline_tag = Column(String(100), index=True)
    library_name = Column(String(100), index=True)
    likes = Column(Integer, default=0, index=True)
    downloads = Column(BigInteger, default=0, index=True)
    downloads_all_time = Column(BigInteger)
    trending_score = Column(Float, default=0, index=True)
    created_at = Column(TIMESTAMP)
    last_modified = Column(TIMESTAMP)
    gated = Column(Boolean, default=False)
    private = Column(Boolean, default=False)
    sha = Column(String(100))
    security_repo_status = Column(String(50))
    has_base_model = Column(Boolean, default=False, index=True)
    derivative_count = Column(Integer, default=0)
    metadata = Column(JSON)
    indexed_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tags = relationship("ModelTag", back_populates="model", cascade="all, delete-orphan")
    base_model_relations = relationship("BaseModelRelation", back_populates="derivative", cascade="all, delete-orphan", foreign_keys="BaseModelRelation.derivative_id")
    dataset_relations = relationship("DatasetRelation", back_populates="model", cascade="all, delete-orphan")
    siblings = relationship("ModelSibling", back_populates="model", cascade="all, delete-orphan")


class ModelTag(Base):
    """Normalized tags table"""
    __tablename__ = "model_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String(500), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    tag = Column(String(200), nullable=False, index=True)
    tag_type = Column(String(50), index=True)  # license, language, framework, general

    model = relationship("Model", back_populates="tags")


class BaseModelRelation(Base):
    """Model provenance/lineage table"""
    __tablename__ = "base_model_relations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    derivative_id = Column(String(500), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    base_model_id = Column(String(500), nullable=False, index=True)
    relation_type = Column(String(50), index=True)  # finetune, adapter, quantized, merge

    derivative = relationship("Model", back_populates="base_model_relations", foreign_keys=[derivative_id])


class DatasetRelation(Base):
    """Dataset provenance table"""
    __tablename__ = "dataset_relations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String(500), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_name = Column(String(500), nullable=False, index=True)

    model = relationship("Model", back_populates="dataset_relations")


class ModelSibling(Base):
    """Model files table"""
    __tablename__ = "model_siblings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String(500), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(500), nullable=False, index=True)
    size = Column(BigInteger)
    blob_id = Column(String(100))
    lfs = Column(Boolean)

    model = relationship("Model", back_populates="siblings")
