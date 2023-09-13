from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship, backref

# Replace placeholders with your database connection details
username = "postgres"
password = "mohithappy"
host = "localhost"  # e.g., "localhost" or IP address
port = "5432"  # e.g., 5432 for PostgreSQL default port
database_name = "RocketLabs"

# Construct the database URL
db_url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
engine = create_engine(db_url)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



class Rocket(Base):
    __tablename__ = "rockets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    nodes = relationship("Node", back_populates="rocket")

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rocket_id = Column(Integer, ForeignKey("rockets.id"))
    parent_id = Column(Integer, ForeignKey("nodes.id"))
    value = Column(Float)

    children = relationship("Node", backref=backref('parent', remote_side=[id]))    
    rocket = relationship("Rocket", back_populates="nodes")

    # Add a combined unique constraint on 'parent_id' and 'name'
    _table_args_ = (
        UniqueConstraint('parent_id', 'name', name='uq_parent_name'),
    )

Base.metadata.create_all(bind=engine)
