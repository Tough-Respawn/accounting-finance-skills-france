# Compatibilité des agents et modèles

Sources officielles consultées le **10 septembre 2026**. Les chemins ci-dessous correspondent aux mécanismes documentés ; ce dépôt ne garantit pas le comportement de toutes les versions, politiques d'entreprise ou interfaces distantes.

## Format commun

La source unique est `plugins/accounting-finance/skills/accounting-finance/`. Elle suit le format [Agent Skills](https://agentskills.io/specification) : `SKILL.md` avec métadonnées YAML standard, ressources Markdown et chemins relatifs au dossier du skill. Le frontmatter n'impose aucun outil propre à un fournisseur.

Le nom de l'agent désigne ici l'application qui découvre les instructions et fournit les outils. Le modèle utilisé par cette application est un choix distinct.

## Installation native dans un projet

L'utilitaire ajoute `accounting-finance/` au dossier de chaque ligne. Tous les fichiers du skill restent ensemble.

| Application | Valeur de `--agent` | Dossier dans le projet | Source officielle |
|-------------|----------------------|------------------------|-------------------|
| Claude Code | `claude-code` | `.claude/skills/` | [Skills Claude Code](https://code.claude.com/docs/en/skills) |
| Codex | `codex` | `.agents/skills/` | [Skills OpenAI](https://learn.chatgpt.com/docs/build-skills) |
| Cursor | `cursor` | `.cursor/skills/` | [Skills Cursor](https://cursor.com/docs/skills) |
| GitHub Copilot | `github-copilot` | `.github/skills/` | [Agent skills GitHub](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Gemini CLI | `gemini-cli` | `.gemini/skills/` | [Skills Gemini CLI](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `opencode` | `.opencode/skills/` | [Skills OpenCode](https://opencode.ai/docs/skills/) |
| Windsurf / Cascade | `windsurf` | `.windsurf/skills/` | [Skills Cascade, documentation redirigée vers Devin Desktop](https://docs.devin.ai/desktop/cascade/skills) |
| Cline | `cline` | `.cline/skills/` | [Skills Cline](https://docs.cline.bot/customization/skills) |
| Roo Code | `roo-code` | `.roo/skills/` | [Skills Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) |
| Amp | `amp` | `.agents/skills/` | [Skills Amp](https://ampcode.com/docs/customize/skills) |

`--agent universal` installe dans `.agents/skills/`. Ce dossier commun est documenté par plusieurs applications ci-dessus ; le nom « universal » n'implique pas que chaque outil le détecte. Choisissez le chemin natif de votre application si sa prise en charge du dossier commun est absente ou incertaine. Codex, Amp et `universal` partagent ici la même destination, dédupliquée par le script.

```bash
python scripts/skill.py install --agent codex claude-code --project "/chemin/projet" --dry-run
python scripts/skill.py install --agent codex claude-code --project "/chemin/projet"
```

Le répertoire de projet doit déjà exister. Les chemins avec espaces sont acceptés lorsqu'ils sont entre guillemets. Une copie identique est laissée intacte. Un conflit sur une destination est détecté avant toute écriture ; `--force` remplace les fichiers distribués qui diffèrent et conserve les fichiers supplémentaires. Les destinations traversant des liens symboliques ou jonctions sont refusées.

## Installation personnelle ou emplacement personnalisé

Utilisez `--skills-dir` avec le dossier personnel documenté par votre application. Cet argument désigne **le parent** des skills, pas le dossier `accounting-finance` lui-même.

Exemples :

```bash
python scripts/skill.py install --skills-dir "~/.agents/skills"
python scripts/skill.py install --skills-dir "~/.claude/skills"
python scripts/skill.py install --skills-dir "~/.config/opencode/skills"
```

Les trois exemples correspondent respectivement à l'emplacement personnel commun décrit par OpenAI, à Claude Code et à OpenCode dans les documentations du tableau. Pour une configuration personnalisée ou une ancienne version, utilisez l'emplacement effectivement reconnu par celle-ci. L'installateur ne déduit pas les chemins d'autres agents à partir de variables propres à Codex.

Un dossier personnel de votre machine ne se retrouve pas automatiquement dans un agent distant ou cloud. Installez le skill dans l'environnement d'exécution ou versionnez la copie de projet selon les mécanismes de l'application. Rechargez la session si elle ne découvre pas immédiatement les nouveaux fichiers.

## Modèles DeepSeek, Qwen, modèles locaux et interfaces sans skills

DeepSeek propose notamment une API de modèles avec [appels d'outils](https://api-docs.deepseek.com/guides/tool_calls/). C'est l'application appelante qui fournit et exécute les outils. Ce dépôt n'invente donc pas de dossier `.deepseek/skills` ni de commande d'installation propre au modèle.

Deux modes sont fournis :

1. **Application avec skills :** installez le dossier pour OpenCode, Cline ou toute autre application du tableau que vous avez configurée avec le modèle souhaité. La connexion au fournisseur reste à configurer dans cette application.
2. **Contexte fourni manuellement :** exportez les domaines nécessaires, puis transmettez le Markdown au modèle via l'interface de chat, un lecteur de fichiers ou votre intégration API. Cela s'applique aussi à Aider, Continue ou à un agent personnalisé lorsque vous contrôlez son contexte.

```bash
python scripts/skill.py export --domain paie --output dist/paie.md
python scripts/skill.py export --domain generale fiscalite --extra decisions-cles --output dist/cas-complexe.md
```

L'export est un document de contexte, pas un plugin ni une implémentation d'API. Il contient le skill, la méthodologie, les domaines choisis, les sources et les compléments nécessaires. Il signale les ressources absentes. Le chargement progressif est préférable avec un agent natif ; dans un chat, limitez l'export au sujet pour respecter la fenêtre de contexte.

## Capacités et comportement de repli

| Capacité du système hôte | Comportement attendu |
|-------------------------|---------------------|
| Lecture de fichiers | Résoudre les références depuis le dossier du `SKILL.md` chargé |
| Recherche dans les fichiers | Charger les sections utiles, puis élargir si nécessaire |
| Aucun accès local | Utiliser les ressources réellement incluses dans le contexte ; demander les extraits manquants |
| Recherche / navigation web | Vérifier les règles, sources et taux applicables à la période demandée |
| Aucun accès web ou échec de vérification | Identifier les points non vérifiés ; analyse conditionnelle et sources à confirmer |
| Parseur PDF / tableur absent | Demander des données accessibles ; ne pas prétendre avoir analysé le document |
| Sortie JSON ou automatisation | Une seule valeur JSON, avertissements et notice dans les métadonnées |
| Interface sans progression séparée | Répondre directement ; aucun statut simulé ni prose ajoutée au JSON |

## Plugin Claude Code

Les fichiers `commands/*.md` et les manifestes `.claude-plugin` sont des adaptateurs Claude. Ils restent dans le plugin et ne sont pas copiés par l'installation du skill seul.

Les commandes lisent `${CLAUDE_PLUGIN_ROOT}/skills/accounting-finance/SKILL.md`, transmettent `$ARGUMENTS` et sélectionnent un domaine. La logique métier et les règles de sortie restent dans le skill. La marketplace doit être ajoutée avant d'installer `accounting-finance@accounting-finance`, comme décrit dans la [documentation des plugins Claude](https://code.claude.com/docs/en/discover-plugins).

## Portée de la validation

Les tests locaux vérifient la structure, l'intégrité des copies et exports, la relocalisation, les chemins avec espaces, les conflits et les simulations. Les métadonnées du skill et des commandes sont vérifiées séparément lors de la modification.

La correspondance des chemins est étayée par les documentations officielles ci-dessus. Elle ne remplace pas un essai de chargement et une évaluation des réponses dans chaque application/version. Les tests de fichiers ne prouvent ni l'exactitude réglementaire du fonds documentaire, ni une qualité de raisonnement identique entre modèles.
