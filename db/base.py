
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:Billyboy7!@database-1.cr1i9jzgfqhq.us-east-2.rds.amazonaws.com')
Session = sessionmaker(bind=engine)
Base = declarative_base()
