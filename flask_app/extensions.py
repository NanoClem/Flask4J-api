from neo4j import GraphDatabase, basic_auth
from neo4j_app.settings import DB_URI, USERNAME, PASSWORD


neo4j_driver = GraphDatabase.driver(DB_URI, auth=basic_auth(USERNAME, PASSWORD), encrypted=False)