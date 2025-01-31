# AnalyseFauneQuebec

Ce repository contient deux scripts Python conçus pour analyser et traiter des informations sur la faune du Québec. Le premier script, `ExtracteurFauneQuebec`, extrait des données sur les espèces fauniques menacées ou vulnérables à partir du site web du gouvernement du Québec et les enregistre dans un fichier XML. Le second script, `SynthétiseurFauneQuebec`, lit ce fichier XML, synthétise les informations en utilisant une API d'intelligence artificielle, et enregistre les résultats dans un nouveau fichier XML. Ces outils sont utiles pour les chercheurs, les écologistes, et les décideurs qui ont besoin d'accéder à des informations détaillées et synthétisées sur la faune du Québec.

## Exemple de Résultat Synthétisé

Voici un exemple de résultat synthétisé pour une espèce, généré par le script `SynthétiseurFauneQuebec` :

**Nom français** : Baleine noire  
**Nom scientifique** : *Eubalaena glacialis*  
**Grand groupe** : Mammifères  
**Sous-groupe** : Mammifères marins  
**Espèces similaires** : Béluga (plusieurs populations)  
**Description** : Grande baleine à fanons, noire avec quelques taches blanches sur le ventre et la tête. Pas de nageoire dorsale. Souffle en forme de «V» pouvant atteindre 5m.  
**Taille** : 15 mètres  
**Poids** : 55 000 kg  
**Habitat** : Eaux tempérées à subarctiques, près des côtes. Hiverne dans les eaux subtropicales.  
**Répartition** : Principalement au large du Nouveau-Brunswick (baie de Fundy) et de la Nouvelle-Écosse. Rarement dans le golfe du Saint-Laurent et près de Terre-Neuve.  
**Alimentation** : Crustacés zooplanctoniques.  
**Reproduction** : Maturité sexuelle entre 5 et 10 ans. Accouplement et naissances en hiver (novembre à février).  
**Statut de l'espèce** : Susceptible d’être menacée ou vulnérable.  
**Menaces** : Perte d’habitat, collisions avec des navires, prises accessoires dans des engins de pêche. 35% des baleines portent des cicatrices dues à ces menaces.
