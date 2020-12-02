"""Database utilites."""

import pandas as pd
from py2neo import Graph
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select

from artist_listener_models import config


def connect_to_db():
    """Connect to Snowflake."""
    return create_engine(URL(
        user=config.SNOWFLAKE_USER,
        password=config.SNOWFLAKE_PASSWORD,
        account=config.SNOWFLAKE_ACCOUNT,
        database=config.SNOWFLAKE_DATABASE,
        schema=config.SNOWFLAKE_SCHEMA,
        role=config.SNOWFLAKE_ROLE,
        warehouse=config.SNOWFLAKE_WAREHOUSE))


def load_table(table_name, index_col=None, db_engine=None):
    """Load table."""
    if db_engine is None:
        db_engine = connect_to_db()

    table = Table(
        table_name, MetaData(), autoload=True, autoload_with=db_engine)
    df = pd.read_sql(select([table]), db_engine, index_col=index_col)

    if index_col:
        return df.sort_index()
    return df


def connect_to_graph_db():
    """Connect to neo4j."""
    return Graph(
        config.NEO4J_URI, user=config.NEO4J_USER,
        password=config.NEO4J_PASSWORD)
