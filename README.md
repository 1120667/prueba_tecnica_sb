# 📊 Data Pipeline End-to-End

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![ClickHouse](https://img.shields.io/badge/clickhouse-%23FFCC01.svg?style=for-the-badge&logo=clickhouse&logoColor=white)
![Airbyte](https://img.shields.io/badge/airbyte-%236151FF.svg?style=for-the-badge&logo=airbyte&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-%23FF694B.svg?style=for-the-badge&logo=dbt&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## 🚀 Overview

Este proyecto implementa un pipeline de datos completo y automatizado. El objetivo es demostrar una arquitectura moderna de ingeniería de datos (Modern Data Stack), completamente containerizada para facilitar su despliegue y escalabilidad.

El flujo abarca desde la extracción de los datos hasta su modelado final:
- **Ingestión:** Extracción de datos desde una API externa.
- **Landing Zone:** Almacenamiento inicial en PostgreSQL.
- **Replicación (EL):** Sincronización hacia ClickHouse mediante Airbyte.
- **Transformación (T):** Modelado y limpieza de datos con dbt.
- **Orquestación:** Gestión y automatización del flujo con Apache Airflow.

---

## 🧱 Arquitectura

![Arquitectura de Datos](screenshots/architecture.png)

### Flujo de datos
`API` ➔ `PostgreSQL` ➔ `Airbyte` ➔ `ClickHouse` ➔ `dbt` ➔ `Data Mart`

---

## ⚙️ Tecnologías Utilizadas

* **Docker & Docker Compose:** Infraestructura y containerización.
* **PostgreSQL:** Base de datos transaccional (Landing zone).
* **ClickHouse:** Base de datos analítica orientada a columnas (Data Warehouse).
* **Airbyte:** Herramienta de integración de datos (ELT / Replicación).
* **dbt (Data Build Tool):** Herramienta de transformación y pruebas de calidad de datos.
* **Apache Airflow:** Plataforma de orquestación de flujos de trabajo.

---

## 🔐 Variables de Entorno (`.env`)

Este proyecto utiliza variables de entorno para manejar credenciales y la configuración de los contenedores de forma segura.

### 📄 Ejemplo `.env.example`

```env
# PostgreSQL Config
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=landing_db
POSTGRES_PORT=5432

# ClickHouse Config
CLICKHOUSE_DB=dwh
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=password

# Airbyte Config
AIRBYTE_EMAIL=your_email
AIRBYTE_PASSWORD=your_password
```

---

## ▶️ Cómo ejecutar el proyecto

### 1. Requisitos previos
Asegúrate de tener instalados:
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)

### 2. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/data-pipeline-e2e.git
cd data-pipeline-e2e
```

### 3. Configurar el entorno
Copia la plantilla de variables de entorno y edítala con tus credenciales:
```bash
cp .env.example .env
```
*(Abre el archivo `.env` en tu editor de código preferido y actualiza los valores)*.

### 4. Levantar los servicios
Ejecuta el siguiente comando para construir y levantar toda la infraestructura:
```bash
docker compose up -d
```
*Tip: Puedes usar `docker compose ps` para verificar que todos los contenedores estén en estado "Up".*

---

## 🔄 Componentes del Pipeline

1.  📥 **Ingestión (Python/API):** Un script/servicio que obtiene datos financieros desde la fuente original (API) y los almacena en su estado crudo dentro de PostgreSQL.
2.  🚚 **Airbyte (Replicación):** Configurado para leer los datos de PostgreSQL y replicarlos de forma eficiente en ClickHouse, actuando como nuestra capa de extracción y carga (EL).
3.  🛠️ **dbt (Transformación):** Se conecta a ClickHouse para transformar los datos crudos en modelos de negocio. 
    * Modelos generados: `stg_stock_prices` (Staging) y `mart_stock_prices_monthly` (Data Mart).
    * Incluye pruebas de calidad de datos (tests), como verificar que no existan nulos (`not_null`) en columnas clave.

---

## 🧠 Orquestación (Airflow)

Todo el proceso está automatizado y monitoreado mediante Apache Airflow. 

**DAG Principal:** `data_pipeline_e2e`

El grafo de dependencias de las tareas se ejecuta en el siguiente orden estricto para garantizar la integridad de los datos:

```text
[ run_ingestion ] ➔ [ airbyte_sync ] ➔ [ dbt_run ] ➔ [ dbt_test ]
```
```
