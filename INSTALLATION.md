# ![Digital Futures Academy](https://github.com/digital-futures-academy/DataScienceMasterResources/blob/main/Resources/datascience-notebook-header.png?raw=`true`)

## Project Set Up

1. Production, test and development environments.
2. Installing the required dependencies.
3. Run the pipeline or the tests

---



### Step 1: Set Up the Environments

#### 1.1. Create `.env.xxx` Files

Create two environment files: `.env.dev` and `.env.test`.

```bash
# Development Environment Variables

# Source Database Configuration
SOURCE_DB_NAME=etl_demo_dev_source
SOURCE_DB_USER=postgres
SOURCE_DB_PASSWORD=
SOURCE_DB_HOST=localhost
SOURCE_DB_PORT=5432

# Target Database Configuration
TARGET_DB_NAME=etl_demo_dev_source
TARGET_DB_USER=postgres
TARGET_DB_PASSWORD=
TARGET_DB_HOST=localhost
TARGET_DB_PORT=5432
```

```bash
# Source Database Configuration
SOURCE_DB_NAME=etl_demo_test_source
SOURCE_DB_USER=postgres
SOURCE_DB_PASSWORD=
SOURCE_DB_HOST=localhost
SOURCE_DB_PORT=5432

# Target Database Configuration
TARGET_DB_NAME=etl_demo_test_source
TARGET_DB_USER=postgres
TARGET_DB_PASSWORD=
TARGET_DB_HOST=localhost
TARGET_DB_PORT=5432
```

> ***NOTE***: To run this project in production, set environment variables directly on the server that will build and run the ETL pipeline.

---



#### 1.2 Create the Development and Test Source Databases

Create the development and test source databases by running the following commands on the terminal (given you have installed Postgres):

```bash
psql -U postgres -c "CREATE DATABASE etl_demo_dev_source;"
psql -U postgres -c "CREATE DATABASE etl_demo_test_source;"
```



---
#### 1.3 Create a Python .venv

Create a Python virtual environment and activate it.

```bash
python3 -m venv .venv
source .venv/bin/activate       # On Windows, use .venv\Scripts\activate
```

---

### Step 2: Install the Required Dependencies



Install the requirements with the `requirements.txt` file:

```bash
pip install -r requirements-setup.txt
```

Run the project setup script to install the project as a package:

```bash
pip install -e .
```

---
### Step 3: Run the pipeline or the tests

Run the pipeline with the run_etl command:
```sh
run_etl <env>  # Where <env> is replaced by the name of the environment to run in, e,g dev
```

Run the tests in the project (test mode)


```
run_tests <test_type>
run_tests all # Run all tests
```
