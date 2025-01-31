import os
import xml.etree.ElementTree as ET
from huggingface_hub import InferenceClient
import signal
import sys
from xml.dom import minidom

# Fonction pour gérer les interruptions de l'utilisateur
def signal_handler(sig, frame):
    print("\nInterruption de l'utilisateur détectée. Enregistrement des données et fermeture du programme.")
    enregistrer_xml()
    sys.exit(0)

# Enregistrer le gestionnaire de signal pour les interruptions
signal.signal(signal.SIGINT, signal_handler)

# Lister les fichiers dans le répertoire actuel
print("Fichiers dans le répertoire actuel :")
for file in os.listdir('.'):
    print(file)

# Initialiser le client avec votre clé API
api_key = "VOTRE CLÉ API"
client = InferenceClient(provider="together", api_key=api_key)

# Fonction pour générer le prompt de synthèse
def generer_prompt(info):
    return f"""
    Synthétise les informations suivantes sous forme de texte très concis pour les rendre factuelles, concises et compréhensibles pour un enfant de 10 ans. 
    Veuillez toujours renvoyer les informations dans cet ordre :

    **Nom français** : {info['Nom_français']}

    **Nom scientifique** : {info['Nom_scientifique']}

    **Grand groupe** : {info['Grand_groupe']}

    **Sous-groupe** : {info['Sous_groupe']}

    **Espèces similaires** : {info['Espèces_similaires']}

    **Distinction** : {info['Distinction']}

    **Description** : {info['Description']}

    **Habitat** : {info['Habitat']}

    **Répartition** : {info['Répartition']}

    **Identification** : {info['Identification']}

    **Taille** : {info['Taille']}

    **Poids** : {info['Poids']}

    **Coloration** : {info['Coloration']}

    **Traits caractéristiques** : {info['Traits_caractéristiques']}

    **Alimentation** : {info['Alimentation']}

    **Reproduction** : {info['Reproduction']}

    **Statut de l'espèce** : {info['Espèce_à_statut']}

    **Menaces pour l'espèce** : {info['Menaces_pour_l_espèce']}
    """

# Fonction pour synthétiser les informations pour une espèce
def synthétiser_informations(prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=messages,
            max_tokens=500,
            temperature=0.2  # Vous pouvez ajuster ce paramètre pour réduire la variabilité
        )
        response = completion.choices[0].message['content']
        print(f"Réponse de l'IA : {response}")
        print(f"Tokens utilisés : {completion.usage['total_tokens']}")
        return response
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return ""

# Vérifier si le fichier XML existe
xml_file = 'faune_info.xml'
if not os.path.exists(xml_file):
    raise FileNotFoundError(f"Le fichier {xml_file} n'existe pas dans le répertoire actuel.")
print(f"Lecture du fichier XML : {xml_file}")

# Lire le fichier XML existant
tree = ET.parse(xml_file)
root = tree.getroot()

# Créer un nouvel arbre XML pour les informations synthétisées
root_synth = ET.Element("FAUNE")

# Fonction pour enregistrer le fichier XML avec une meilleure indentation
def enregistrer_xml():
    tree_synth = ET.ElementTree(root_synth)
    tree_synth.write('faune_synthétisée.xml', encoding="utf-8", xml_declaration=True)
    # Lire le fichier et réécrire avec une indentation
    with open('faune_synthétisée.xml', 'r', encoding='utf-8') as file:
        xml_string = file.read()
    parsed_xml = minidom.parseString(xml_string)
    pretty_xml_as_string = parsed_xml.toprettyxml(indent="  ")
    with open('faune_synthétisée.xml', 'w', encoding='utf-8') as file:
        file.write(pretty_xml_as_string)
    print("Nouveau fichier XML créé avec les informations synthétisées.")

# Parcourir chaque espèce et synthétiser les informations
for espece_elem in root.findall('.//ficheBioInfo'):
    print(f"Traitement de l'espèce : {espece_elem.find('Nom_français').text}")
    
    # Rassembler les informations existantes
    def get_text_or_default(element, tag, default=""):
        found = element.find(tag)
        return found.text if found is not None else default

    info = {tag: get_text_or_default(espece_elem, tag) for tag in [
        'Nom_français', 'Nom_scientifique', 'Grand_groupe', 'Sous_groupe', 'Espèce_à_statut',
        'Description', 'Identification', 'Taille', 'Poids', 'Coloration', 'Distinction',
        'Répartition', 'Alimentation', 'Reproduction', 'Menaces_pour_l_espèce', 'Traits_caractéristiques',
        'Espèces_similaires', 'Habitat'
    ]}

    # Vérifier que les informations sont correctement récupérées
    print(f"Informations récupérées pour {info['Nom_français']} : {info}")

    # Générer le prompt de synthèse
    prompt = generer_prompt(info)
    print(f"Prompt généré : {prompt}")

    # Synthétiser les informations en utilisant l'IA
    print(f"Synthèse des informations pour {info['Nom_français']}...")
    informations_synthétisées = synthétiser_informations(prompt)
    print(f"Informations synthétisées : {informations_synthétisées}")

    # Vérifier que les informations synthétisées ne sont pas vides
    if informations_synthétisées.strip():
        # Ajouter les informations synthétisées au nouvel arbre XML
        espece_synth = ET.SubElement(root_synth, "ESPECE")
        ET.SubElement(espece_synth, "NOM_FRANÇAIS").text = info['Nom_français']
        ET.SubElement(espece_synth, "GRAND_GROUPE").text = info['Grand_groupe']
        ET.SubElement(espece_synth, "SOUS_GROUPE").text = info['Sous_groupe']
        ET.SubElement(espece_synth, "STATUT").text = info['Espèce_à_statut']
        ET.SubElement(espece_synth, "DESCRIPTION").text = informations_synthétisées
        print(f"Informations synthétisées ajoutées pour {info['Nom_français']}.")
        # Enregistrer le fichier XML après chaque ajout d'espèce
        enregistrer_xml()
    else:
        print(f"Erreur : Les informations synthétisées pour {info['Nom_français']} sont vides.")

print("Traitement terminé.")
