from neo4j import GraphDatabase
import sys

NEO4J_URI="neo4j+s://a30b7928.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="nCamqdS9K1F3-gr2OcX5kE2TIYBXsVTusNfst8I1egM"
URI = NEO4J_URI
LOGIN_AND_PWD = [NEO4J_USERNAME,NEO4J_PASSWORD]

with GraphDatabase.driver(URI, auth=tuple(LOGIN_AND_PWD)) as driver:
    try:
        driver.verify_connectivity()
        print(f"Connected to Database URI:{URI}")
    except Exception as ex:
        print(f"Failed to connect to {URI} due to {ex}")
        exit(-1)

def afficher_finales(driver):
    with driver.session() as session:
        resulat =session.run ("MATCH (f:Final) RETURN f.year As Anne, f.country AS pays;")
        for record in resulat:
            print("Pays", record["f.country"])
            print("Année", record["f.year"])

afficher_finales(driver)

driver.close()

print(f"Program finished")