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
        resulat =session.run ("MATCH (f:Final) RETURN f.year, f.country;")
        for record in resulat:
            print("Pays", record["f.country"])
            print("Année", record["f.year"])
            print("\n")


def afficher_equipes_finale(driver):
    with driver.session() as session:
        resulat =session.run ("MATCH (t:Team) RETURN t.name")
        for record in resulat:
            print(record['t.name'])
            print("\n")

def afficher_resultats_equipe(driver):
    with driver.session() as session:
        resulat =session.run ("MATCH (t:Team)-[r:PLAY_FINAL]->(f:Final) RETURN t.name, f.year, r.winner ORDER BY f.year")
        for record in resulat:
            print(record['t.name'])
            print(record['t.year'])
            print(record['r.winner'])
            print("\n")

# Fonction pour afficher les résultats obtenus pour une équipe donnée toutes années confondues
def afficher_resultats_equipe(driver, equipe):
    with driver.session() as session:
        result = session.run(
            "MATCH (f:Final)-[:PLAY_FINAL]->(t:Team {name: $nomEquipe}) RETURN f.year, f.result",
            nomEquipe=equipe.capitalize()  # Convertir en majuscule la première lettre de l'équipe
        )
        for record in result:
            print("Année:", record["f.year"])
            print("Résultat:", record["f.result"])
            print()
def afficher_details_finale(driver, year):
    with driver.session() as session:
        Yearint = int(year)
        query = "MATCH (f:Final {year: $year})<-[r:PLAY_FINAL]-(t:Team)RETURN f.country, f.city, " \
                "f.stadium, collect(t.name), collect(r.winner) "
        result = session.run(query, year=Yearint)
        print(f"\nDétails de la finale de {year} :")
        for record in result:
            print(f"Pays : {record['f.country']}")
            print(f"Ville : {record['f.city']}")
            print(f"Stade : {record['f.stadium']}")
            print(f"Équipes : {', '.join(record['t.name'])}")
            print(f"Résultat : {record['r.winner'][0]}")

# Fonction principale pour afficher le menu et gérer les choix de l'utilisateur
def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    while True:
        print("\nMenu:")
        print("1. Afficher toutes les finales")
        print("2. Afficher toutes les équipes ayant participé aux finales")
        print("3. Afficher les résultats obtenus pour une équipe donnée toutes années confondues")
        print("4. Afficher le pays, la ville, le stade, les 2 équipes finalistes et le résultat pour une finale donnée")
        print("5. Quitter")
        choix = input("Veuillez sélectionner une option (1-5): ")

        if choix == "1":
            afficher_finales(driver)
        elif choix == "2":
            afficher_equipes_finale(driver)
        elif choix == "3":
            equipe = input("Veuillez entrer le nom de l'équipe : ")
            afficher_resultats_equipe(driver, equipe)
        elif choix == "4":
            annee = input("Veuillez entrer l'année de la finale : ")
            afficher_details_finale(driver, int(annee))
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

    driver.close()
    print("Programme terminé.")


if __name__ == "__main__":
    main()
