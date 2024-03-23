from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date

from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base class
Base = declarative_base()


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    date_of_birth = Column(Date)
    monthly_payment_made = Column(Boolean)
    photo_path = Column(String)
    last_payment_date = Column(Date)


# Generate a new table for the database where the embedding for the image of each member will be stored
class MemberEmbedding(Base):
    __tablename__ = "member_embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, nullable=False)
    embedding = Column(String, nullable=False)


# Create an engine that stores data in the local directory's database file.
engine = create_engine("sqlite:///database/data.sqlite")

# Create all tables in the engine.
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
