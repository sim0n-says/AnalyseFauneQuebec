# SynthétiseurFauneQuebec
# Ce script Python est conçu pour lire un fichier XML contenant des informations sur les espèces fauniques,
# synthétiser ces informations en utilisant une API d'intelligence artificielle, et enregistrer les résultats dans un nouveau fichier XML.
# Le script utilise la bibliothèque ElementTree pour lire et écrire des fichiers XML, et l'API Hugging Face pour la synthèse de texte.
# Le script gère également les interruptions de l'utilisateur en enregistrant les données avant de se fermer.
# Le script est conçu pour être exécuté dans un environnement Python 3.7 ou supérieur.
# Auteur : Simon Bédard -
# Date : 2025

# Licence MIT
#
# Copyright (c) 2025 Simon Bédard - simon@servicesforestiers.tech
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

import os
import xml.etree.ElementTree as ET
from huggingface_hub import InferenceClient
import signal
import sys

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
root_synth = ET.Element("faune_synthétisée")

# Fonction pour enregistrer le fichier XML
def enregistrer_xml():
    tree_synth = ET.ElementTree(root_synth)
    tree_synth.write('faune_synthétisée.xml', encoding="utf-8", xml_declaration=True)
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
        espece_synth = ET.SubElement(root_synth, "espece")
        ET.SubElement(espece_synth, "Nom_français").text = info['Nom_français']
        ET.SubElement(espece_synth, "Grand_groupe").text = info['Grand_groupe']
        ET.SubElement(espece_synth, "Sous_groupe").text = info['Sous_groupe']
        ET.SubElement(espece_synth, "Espèce_à_statut").text = info['Espèce_à_statut']
        ET.SubElement(espece_synth, "Description_synthétisée").text = informations_synthétisées
        print(f"Informations synthétisées ajoutées pour {info['Nom_français']}.")
        # Enregistrer le fichier XML après chaque ajout d'espèce
        enregistrer_xml()
    else:
        print(f"Erreur : Les informations synthétisées pour {info['Nom_français']} sont vides.")

print("Traitement terminé.")
