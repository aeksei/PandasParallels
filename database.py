from sqlalchemy import create_engine, MetaData

SQLALCHEMY_DATABASE_URL = """postgresql://postgres:postgres_password@localhost:5432/postgres"""

engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()
