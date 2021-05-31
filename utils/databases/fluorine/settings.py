from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'mysql+pymysql://root:@172.20.0.2:3306/lablib_db?charset=utf8'
ENGINE = create_engine(
    DATABASE_URL,
    encoding = "utf-8",
    echo=True # Trueだと実行のたびにSQLが出力される
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()
