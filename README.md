# accounting-finance — skill portable

**Assistant de comptabilité, finance d'entreprise et fiscalité pour la France et les référentiels européens.**

Le même dossier [`accounting-finance`](plugins/accounting-finance/skills/accounting-finance/SKILL.md) s'utilise dans les agents qui prennent en charge le format [Agent Skills](https://agentskills.io/specification). Le dépôt fournit une installation pour Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode, Windsurf, Cline, Roo Code et Amp, ainsi qu'un export Markdown pour les interfaces sans chargeur de skills.

**DeepSeek, Qwen et les autres modèles :** choisissez l'installation correspondant à l'application qui les exécute. Pour une interface de chat ou une intégration API sans chargeur, utilisez l'export ci-dessous. La disponibilité des outils et la qualité des réponses dépendent du modèle, de l'application et de sa configuration.

## Installation rapide

Le skill lui-même est constitué de fichiers Markdown, sans dépendance d'exécution. L'utilitaire d'installation et d'export demande **Python 3.10 ou plus**, sans paquet à installer. Les commandes ci-dessous se lancent depuis la racine de ce dépôt, sous Windows, macOS ou Linux.

```bash
git clone https://github.com/Tough-Respawn/accounting-finance-skills-france.git
cd accounting-finance-skills-france
python scripts/skill.py list
```

Remplacez le chemin de projet dans cet exemple par un dossier existant :

```bash
python scripts/skill.py install --agent codex --project "/chemin/vers/mon-projet"
```

Exemple Windows :

```powershell
python scripts/skill.py install --agent claude-code cursor --project "C:\Projets\mon-projet"
```

Pour un dossier personnel ou un autre emplacement reconnu par votre agent :

```bash
python scripts/skill.py install --skills-dir "~/.agents/skills"
```

Le script ajoute `accounting-finance/` dans le dossier indiqué et copie **le skill, sa méthodologie, ses 13 références et la licence**. Il affiche les destinations, accepte `--dry-run`, laisse les copies identiques intactes et refuse d'écraser un fichier différent sans `--force`. Une mise à jour avec `--force` conserve les fichiers supplémentaires présents dans la destination. Le script ne modifie pas les réglages de l'agent et ne lance aucun téléchargement.

Sans Python, copiez le dossier complet `plugins/accounting-finance/skills/accounting-finance/` dans le dossier de skills de votre application, et joignez le fichier `LICENSE` à cette copie. **Copier seulement `SKILL.md` ne suffit pas.**

Les chemins, sources officielles et limites par agent figurent dans [COMPATIBILITY.md](COMPATIBILITY.md). Rechargez les skills ou redémarrez l'agent si nécessaire. Choisissez une seule installation par agent pour éviter les doublons entre skills personnels, projet et plugin.

## Utilisation

Dans Codex, après installation :

```text
$accounting-finance Explique le calcul du BFR à partir de mon bilan.
```

Dans Claude Code, après installation du skill seul :

```text
/accounting-finance Explique le traitement comptable de cette facture.
```

Dans les autres agents, sélectionnez le skill dans l'interface ou demandez :

> Utilise le skill accounting-finance pour analyser ce bilan. Présente les hypothèses, les calculs et les sources vérifiées.

La sélection automatique dépend du chargeur de skills et de ses réglages. Les commandes du plugin Claude ne sont pas importées par l'installateur portable.

## DeepSeek, chat, API et agents sans skills natifs

Créez un fichier autonome contenant les instructions et les références du sujet :

```bash
python scripts/skill.py export --domain fiscalite --output dist/accounting-finance-fiscalite.md
python scripts/skill.py export --domain generale finance --extra glossaire --output dist/accounting-finance-analyse.md
```

Chargez le fichier généré dans le contexte de votre application, comme document ou contenu de prompt selon ses possibilités, puis posez votre question. Avec un agent disposant d'un lecteur de fichiers, demandez-lui de lire ce fichier avant de répondre. Cette méthode convient également aux intégrations personnalisées utilisant des modèles DeepSeek ou Qwen, et aux configurations d'Aider ou Continue où vous fournissez vous-même le contexte.

Domaines : `generale`, `analytique`, `ifrs`, `finance`, `fiscalite`, `audit`, `controle-gestion`, `paie`. `--domain all` inclut les huit domaines. Les compléments `glossaire` et `decisions-cles` se sélectionnent avec `--extra`. La méthodologie et l'annuaire des sources sont inclus ; le PCG et les taux sont ajoutés selon les domaines.

L'export indique sa taille en octets, **pas en tokens**. Vérifiez la limite de contexte de votre application et préférez les domaines nécessaires. Les références non incluses restent signalées comme absentes. Un export ne fournit ni navigation web, ni accès aux fichiers locaux, ni exécution d'outils : les règles et taux non vérifiés doivent être présentés comme tels.

## Domaines couverts

| Domaine | Exemples | Commande du plugin Claude |
|---------|----------|---------------------------|
| Comptabilité générale | PCG, écritures, bilan, annexes | `/accounting-finance:general-accounting` |
| Comptabilité analytique | Coûts, ABC, seuil de rentabilité | `/accounting-finance:cost-accounting` |
| IFRS / consolidation | IAS/IFRS, retraitements, consolidation | `/accounting-finance:ifrs` |
| Finance d'entreprise | SIG, BFR, CAF, ratios, DCF | `/accounting-finance:corporate-finance` |
| Fiscalité | IS, TVA, CET, intégration fiscale | `/accounting-finance:tax` |
| Audit et contrôle | CAC, NEP, contrôle interne | `/accounting-finance:audit` |
| Contrôle de gestion | Budgets, reporting, écarts, KPI | `/accounting-finance:management-control` |
| Paie | Bulletins, cotisations, DSN | `/accounting-finance:payroll` |

Huit modèles de réponse adaptent le résultat au livrable : écriture, analyse financière, note fiscale, exercice corrigé, fiche de paie, tableau de bord, cas complexe et sortie structurée. Les sorties JSON regroupent données, sources et avertissements dans une valeur JSON valide.

Les données embarquées constituent un fonds documentaire. Les règles, taux et versions applicables doivent être vérifiés sur les sources officielles ; si les outils ne le permettent pas, le skill indique les limites de vérification. Cette mise à jour de portabilité ne constitue pas une révision réglementaire du fonds documentaire.

## Plugin Claude Code avec les neuf commandes

Cette installation est une alternative au skill seul. Ajoutez d'abord la marketplace :

```bash
claude plugin marketplace add Tough-Respawn/accounting-finance-skills-france
claude plugin install accounting-finance@accounting-finance
```

Pour essayer la copie locale depuis ce dépôt :

```bash
claude --plugin-dir ./plugins/accounting-finance
```

Puis utilisez `/accounting-finance:accounting <question>` pour le routage automatique, ou l'une des commandes du tableau. Les chemins de ressources des commandes sont résolus dans le plugin installé, y compris lorsqu'il est placé dans le cache de Claude. Voir les [instructions officielles Claude Code](https://code.claude.com/docs/en/discover-plugins).

## Développement et vérification

```bash
python -m unittest discover -s tests -v
```

Les tests vérifient les installations dans des dossiers temporaires, la conservation des références, les conflits de fichiers, l'absence d'écriture en simulation, la relocalisation et les exports sélectifs. Ils n'exécutent pas les modèles ni les applications tierces.

```text
plugins/accounting-finance/
  .claude-plugin/plugin.json       Métadonnées du plugin Claude
  commands/                        Adaptateurs des neuf commandes Claude
  skills/accounting-finance/
    SKILL.md                       Instructions portables, source unique
    methodology.md                 Huit modèles de réponse
    references/                    Treize références métier
scripts/skill.py                    Installation et export, bibliothèque standard
tests/test_skill.py                 Vérifications de portabilité
COMPATIBILITY.md                    Matrice, sources et limites
AGENTS.md                          Instructions de contribution communes
```

## English

A portable French accounting and corporate finance skill using the Agent Skills format. Run `python scripts/skill.py list` to see supported application targets, then `install --agent <target> --project <project>`. Copying the complete skill folder manually also works; include the MIT license.

For DeepSeek or other models, install into the host application's skill directory. For chat/API integrations without skill discovery, use `export --domain <domain> --output <file.md>` and supply the generated document as context. File access, web verification and model behavior remain capabilities of the host. See [COMPATIBILITY.md](COMPATIBILITY.md) for documented paths and validation limits.

## Licence

[MIT](LICENSE)
