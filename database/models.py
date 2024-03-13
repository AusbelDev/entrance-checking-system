from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class
Base = declarative_base()


class Customer(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    date_of_birth = Column(Date)
    monthly_payment_made = Column(Boolean)
    photo_path = Column(String)
    last_payment_date = Column(Date)


# Create an engine that stores data in the local directory's database file.
engine = create_engine("sqlite:///database/gym_members_db.sqlite")

# Create all tables in the engine.
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
