# Determinisme du workflow

## Garanties deterministes

Pour une meme question et la meme configuration :

- `plan_workflow` selectionne les agents avec des regles de mots-cles explicites ;
- le routeur n'utilise pas de LLM ;
- `AGENT_ORDER` impose un ordre d'execution fixe ;
- la synthese est toujours la derniere etape ;
- les transitions du `StateGraph` dependent uniquement du plan et du curseur ;
- la trace permet de verifier le chemin reellement execute ;
- les modeles sont configures avec `temperature=0`.

## Limites de la garantie

Le workflow complet n'est pas reproductible bit a bit :

- `temperature=0` reduit la variabilite mais ne garantit pas un texte identique ;
- chaque agent LangChain peut varier dans sa formulation et ses appels d'outils ;
- les API sanitaires, geographiques et meteo retournent des donnees vivantes ;
- les horodatages et le cache changent entre deux executions ;
- le classement RAG depend du modele d'embeddings et du contenu indexe ;
- un changement de modele ou de fournisseur peut modifier les sorties.

## Formulation correcte

Le **routage externe et l'ordre du graphe sont deterministes**. Les sorties des
agents et des sources externes sont controlees, tracees et structurees, mais
elles ne sont pas garanties identiques a chaque execution.
