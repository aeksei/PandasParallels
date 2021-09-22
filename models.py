from geoalchemy2 import Table

from database import engine, metadata

KgiopObjects = Table("kgiop_objects", metadata,
                     autoload=True, autoload_with=engine)

Streets = Table("street", metadata,
                autoload=True, autoload_with=engine)
