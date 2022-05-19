### RUN Pipeline

`docker run -it test:pandas`

### Build Container

`docker build -t test:pandas . `

### Run postgres in docker

`docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v /Users/socrates/projects/de_zoomcamp/docker_sql/ny_taxi_postgres/:/var/lib/postgresql/data -p 5432:5432 postgres:13`

### PGCLI

`pgcli -h localhost -p 5432 -u root -d ny_taxi`

### Source of Data

`https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page`

### RUn PGADMIN in docker

`docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" -e PGADMIN_DEFAULT_PASSWORD="root" -p 8080:80 dpage/pgadmin4`

### Put containers in one network so they can discover each other

1. Create network
   `docker network create pg-network`
2. Run postgres in network
   `docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v /Users/socrates/projects/de_zoomcamp/docker_sql/ny_taxi_postgres/:/var/lib/postgresql/data -p 5432:5432 --network=pg-network --name pg-database postgres:13`
3. Run PGAdmin in Postgres
   `docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" -e PGADMIN_DEFAULT_PASSWORD="root" -p 8080:80 --network=pg-network --name pgadmin-2 dpage/pgadmin4`

### Convert notebook to a script

`jupyter nbconvert --to=script upload_data.ipynb`

### Run Ingestion script

`python ingest_data.py --user=root --password=root --host=localhost --port=5432 --db=ny_taxi --table_name=yellow_taxi_data --url="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"`

### Build Taxi ingestion

`docker build -t taxi_ingest:v001 .`

### Run Ingestion script in docker

`docker run -it --network=pg-network taxi_ingest:v001 --user=root --password=root --host=pg-database --port=5432 --db=ny_taxi --table_name=yellow_taxi_data --url="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"`

### Initialize state file (.tfstate)

`terraform init`

### Check changes to new infra plan

`terraform plan -var="project=<your-gcp-project-id>"`

### Create new infra

`terraform apply -var="project=<your-gcp-project-id>"`

### Delete infra after your work, to avoid costs on any running services

`terraform destroy`
