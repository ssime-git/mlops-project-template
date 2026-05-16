# MLOps Project Template

⚠️ **Ce dépôt est un TEMPLATE** — adaptez-le à votre projet ML réel. Il fournit une structure de base et des exemples pour chaque phase du cycle de vie MLOps.


## Méthodologie MLOps

Cette méthodologie décrit un parcours structuré pour industrialiser un projet ML, en passant par 4 phases principales. L'objectif est d'aboutir à un système de production robuste, monitoré et maintenable.

### Cadrage (Étape préliminaire)

Avant toute implémentation technique, il est impératif de cadrer le projet :

| Tâche | Description |
|-------|-------------|
| **Définir le problème métier** | Quelle décision le modèle influence-t-il ? |
| **Identifier les métriques** | Métriques ML (accuracy, recall, etc.) + Métriques métier (revenus, économie, etc.) |
| **Établir un baseline** | Modèle simple ou heuristique à battre |
| **Évaluer la faisabilité** | Données disponibles ? Suffisantes ? Labélisées ? |
| **Identifier les contraintes** | Latence, (CPU/GPU/edge), réglementations |

**Fichier à compléter :** `configs/problem.yaml`

```bash
# Premier réflexe : remplir le cadrage
code configs/problem.yaml
```


### Phases du Projet

#### Phase 1 : Fondations & Containerisation (L'Unité)
**Objectif :** Rendre le modèle accessible via une API conteneurisée et testée.

| Tâche principale | Détail technique |
|------------------|-------------------|
| Environnement & Baseline | Setup `uv`, entraînement du premier modèle simple. |
| Implémentation API | Création du serveur FastAPI dans `src/api/`. |
| Tests unitaires | Écriture des tests pour `/health`, `/predict` et les fonctions de prétraitement. |
| Validation des données | Ajout de vérifications basiques sur les données d'entrée (noms de colonnes, types, plages). |
| Containerisation | Écriture du `docker/api.Dockerfile` et premier `docker-compose.yml` (service `api` uniquement). |

**Livrable technique :** Un service API fonctionnel et testé, lancé via `docker-compose up api`.

#### Phase 2 : Microservices & Gestion Data (L'Écosystème)
**Objectif :** Gérer le cycle de vie des données, des expériences et des modèles — et automatiser leur livraison.

| Tâche principale | Détail technique |
|------------------|-------------------|
| Suivi d'expériences | Ajout de MLflow au `docker-compose.yml` (ou config Dagshub). |
| Registre de modèles | Enregistrement des modèles dans le MLflow Model Registry ; utilisation des stages `Staging` et `Production`. |
| Versioning Data | Ajout de MinIO (S3) au `docker-compose.yml` -> Config DVC. |
| Pipeline Training | Création du `docker/train.Dockerfile` pour isoler l'entraînement. |
| CI/CD Pipeline | Automatisation du build et push des images Docker à chaque commit (GitHub Actions). |

**Livrable technique :** Stack `api` + `mlflow` + `minio` orchestrée, avec tracking actif des expériences, artefacts versionnés, registre de modèles et pipeline de build automatisé.

#### Phase 3 : Orchestration & Sécurisation (Le Pipeline)
**Objectif :** Automatiser le flux de données et sécuriser les accès à l'API.

| Tâche principale | Détail technique |
|------------------|-------------------|
| Workflow Automation | Ajout de Prefect ou Airflow au `docker-compose.yml`. |
| API Gateway & Sécurité | Implémentation JWT et gestion des accès sur l'API. |

**Livrable technique :** Pipeline automatisé (Data -> Train -> Deploy) et API sécurisée.

#### Phase 4 : Monitoring & Observabilité (La Production)
**Objectif :** Garantir la stabilité et détecter la dégradation du modèle en amont.

| Tâche principale | Détail technique |
|------------------|-------------------|
| Métriques Infra | Ajout de Prometheus et Grafana au `docker-compose.yml`. |
| Model Drift | Intégration d'Evidently pour surveiller la dérive des données (`src/monitoring/detection.py`). |
| Feedback Loop | Définir les seuils d'alerte sur les métriques de drift ; déclencher le retraining si dépassement ; valider et promouvoir le nouveau modèle via le registre MLflow. |

**Livrable technique :** Dashboard de monitoring complet, alerting opérationnel et processus de retraining documenté.

#### 📅 Soutenance : date à définir


## 🔄 Transitions entre Phases

Chaque phase débouche sur une **revue** avant passage à la suivante :

```sh
Phase 1 ──► Revue (modèle + API validés) ──► Phase 2 ──► Revue ──► Phase 3 ──► Revue ──► Phase 4
   │                                                    │                              │
   ▼                                                    ▼                              ▼
Validation technique                              Validation infra                  Validation prod
```

### Critères de passage :

- **Phase 1 → Phase 2 :** Tests OK, API fonctionnelle, Dockerfile validé, validation des données en place
- **Phase 2 → Phase 3 :** Expériences tracées, versioning opérationnel, artefacts versionnés, modèle dans le registre, CI/CD fonctionnelle
- **Phase 3 → Phase 4 :** Pipeline orchestré opérationnel, rollback possible, API sécurisée


## Travail en Équipe (Tâches Parallèles)

Pour optimiser le temps, certaines tâches peuvent être menées en **parallèle** :

| Tâche A | Tâche B | Équipe |
|---------|---------|--------|
| Entraînement modèle | Développement API | ML Eng + MLE |
| Feature engineering | Définition data contracts | Data Eng |
| Mise en place MLflow | Infrastructure Docker | MLE + DevOps |
| Tests unitaires | Documentation | QA + Tech Writer |
| Monitoring | CI/CD | SRE + DevOps |


## Technologies MLOps

Ce template utilise certaines technologies par défaut, mais d'autres options sont possibles selon vos besoins :

### Orchestration de Pipelines

| Techno | Quand l'utiliser | Installation |
|--------|------------------|--------------|
| **Prefect** (défaut) | Petit à moyen projet, simplicité, monitoring cloud | `uv pip install prefect` |
| **Airflow** | Gros projet, écosystème robuste, nombreuses intégrations | `pip install apache-airflow` |
| **Dagster** | Projet moderne, bonnes pratiques software engineering | `pip install dagster` |

**Prefect (exemple) :**
```python
from prefect import flow, task

@task
def preprocess_data():
    pass

@flow
def train_pipeline():
    data = preprocess_data()
    model = train_model(data)
    return model
```

**Airflow (alternative) :**

```bash
airflow standalone
```

```python
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('ml_pipeline', start_date=datetime(2024,1,1)) as dag:
    preprocess = PythonOperator(task_id='preprocess', python_callable=preprocess)
    train = PythonOperator(task_id='train', python_callable=train)
    preprocess >> train
```

### Versioning des Données

| Techno | Quand l'utiliser | Installation |
|--------|------------------|--------------|
| **DVC** (défaut) | Versioning fichier, pipeline déclaratif | `pip install dvc` |
| **lakeFS** | Data lake avec versioning, environnement dev/prod | Docker Compose |
| **Delta Lake** | Format Parquet avec transactions (Spark) | Spark dependency |

**DVC :**
```bash
dvc init
dvc add data/raw/
git add data/raw.dvc
git commit -m "Add raw data v1"
dvc checkout
```

**Commandes DVC utiles :**
```bash
dvc repro          # Relancer le pipeline
dvc metrics show   # Afficher les métriques
dvc diff           # Voir les changements
```

### Suivi des Expériences

| Techno | Quand l'utiliser | Installation |
|--------|------------------|--------------|
| **MLflow** (défaut) | Tracking ouvert, multi-langue | `pip install mlflow` |
| **Weights & Biases** | Interface utilisateur élégante, collaboration | `pip install wandb` |
| **Neptune.ai** | Plateforme complète, richesse des métadonnées | `pip install neptune` |

**MLflow :**
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
```

```python
import mlflow

mlflow.set_experiment("mon_experience")
with mlflow.start_run():
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_params({"n_estimators": 100})
    mlflow.sklearn.log_model(model, "model")
```

### API d'Inférence

| Techno | Quand l'utiliser | Installation |
|--------|------------------|--------------|
| **FastAPI** (défaut) | Performance, validation Pydantic, async natif | `pip install fastapi uvicorn` |
| **Flask** | Simplicité, petit projet | `pip install flask` |
| **BentoML** | Framework spécialisé inference, packaging simple | `pip install bentoml` |

**FastAPI (par défaut) :**
```bash
# Lancer le serveur
uvicorn src.api.main:app --reload

# Tester
curl http://localhost:8000/health
```

### Monitoring & Drift Detection

| Techno | Quand l'utiliser | Installation |
|--------|------------------|--------------|
| **Prometheus + Grafana** (défaut) | Métriques custom, visualisations puissantes | docker-compose |
| **Evidently** (défaut) | Data/model drift detection | `pip install evidently` |
| **Arize** | Plateforme complète ML monitoring | `pip install arize-ai` |

**Evidently (v0.4+) :**
```python
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.report import Report

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=df_ref, current_data=df_current)
report.save_html("reports/drift/drift_report.html")
```


## Installation et Utilisation Rapide

### Prérequis
```bash
# Installer UV (gestionnaire de packages)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installer Docker et Docker Compose
# Voir https://docs.docker.com/
```

### Setup du projet
```bash
# Cloner le template
git clone <votre-repo-url>
cd mlops-project

# Installer les dépendances (dépendances dev incluses automatiquement)
uv sync
```

### Étape 1 : Cadrage
```bash
# Remplir le fichier de problème
code configs/problem.yaml
```

### Lancer les services
```bash
# API seule (Phase 1)
docker-compose up api -d

# Tous les services (Phase 2-4)
docker-compose up -d
```

### Services disponibles
| Service | URL | Description |
|---------|-----|-------------|
| API | http://localhost:8000 | Inference endpoint |
| API Doc | http://localhost:8000/docs | Swagger UI |
| MLflow | http://localhost:5000 | Tracking |
| Prometheus | http://localhost:9090 | Métriques |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| MinIO | http://localhost:9001 | Console stockage objets |


## Structure du Projet

```sh
mlops_project/
├── .github/workflows/     # CI/CD
├── configs/               # Configurations Hydra
│   ├── model/            # Hyperparamètres du modèle
│   ├── problem.yaml      # Cadrage projet
│   └── train.yaml        # Config entraînement
├── data/                  # Données (gérées par DVC)
│   ├── raw/              # Données brutes
│   └── processed/        # Données traitées
├── deployment/           # Infra configs (Prometheus, Grafana)
├── docker/               # Dockerfiles
├── docs/                 # Documentation méthodologique
├── models/               # Modèles entraînés
├── reports/              # Rapports de drift générés (HTML)
├── src/                  # Packages UV workspace
│   ├── api/             # Service d'inférence FastAPI
│   ├── common/          # Utilitaires partagés
│   ├── monitoring/      # Détection de drift
│   └── training/        # Train / preprocess / evaluate
├── tests/                # Tests
├── docker-compose.yml    # Orchestration locale
├── dvc.yaml              # Pipeline DVC
└── pyproject.toml        # Config workspace racine
```


## ✅ Checklist par Phase

### Phase 1 : Fondations
- [ ] `configs/problem.yaml` rempli
- [ ] Environnement reproductible (`uv sync`)
- [ ] API d'inférence fonctionnelle (`src/api/main.py`)
- [ ] Tests unitaires passants (`pytest tests/`)
- [ ] Validation basique des données en place
- [ ] Containerisation initiale (`docker-compose up api`)

### Phase 2 : Microservices & Gestion Data
- [ ] MLflow opérationnel (suivi d'expériences)
- [ ] Modèle enregistré dans le MLflow Model Registry
- [ ] Données versionnées via MinIO (S3/DVC)
- [ ] Container d'entraînement isolé (`docker/train.Dockerfile`)
- [ ] Stack orchestrée (`api` + `mlflow` + `minio`)
- [ ] Pipeline CI/CD opérationnel (build + push)

### Phase 3 : Orchestration & Sécurité
- [ ] Orchestrateur lancé via Docker (Prefect/Airflow)
- [ ] Pipeline automatisé (Data -> Train -> Deploy)
- [ ] API sécurisée (JWT)
- [ ] `docker-compose.yml` mis à jour avec l'orchestrateur

### Phase 4 : Monitoring & Observabilité
- [ ] Prometheus & Grafana lancés via Docker Compose
- [ ] Surveillance du drift opérationnelle (Evidently)
- [ ] Seuils d'alerte définis et testés
- [ ] Déclencheur de retraining documenté
- [ ] Documentation finale et runbooks


## Personnalisation du Template

Pour adapter ce template à votre projet :

1. **Remplacer `problem.yaml`** avec votre cas d'usage
2. **Modifier les configs Hydra** dans `configs/`
3. **Implémenter votre modèle** dans `src/training/`
4. **Adapter l'API** dans `src/api/main.py`
5. **Configurer les métriques** dans `deployment/prometheus/prometheus.yml`
6. **Ajouter vos tests** dans `tests/`


## 📚 Ressources Complémentaires

- [Awesome MLOps](https://github.com/visenger/awesome-mlops)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [DVC Documentation](https://dvc.org/doc)
