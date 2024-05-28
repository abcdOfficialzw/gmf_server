from sqlmodel import create_engine

# MySQL Credentials
username = "titus"
password = "ruj*33hk"
host = "localhost"
port = "3306"
database_name = "geodetic_monument_finder"

# SQLite configurations
sqlite_file_name = "database.db"

# MySQL Url
mysql_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
# SQLite Url
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Database engine
engine = create_engine(sqlite_url, echo=True)
