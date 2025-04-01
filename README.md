# Job Data Ingestion Pipeline

This project implements a data ingestion pipeline that scrapes job data from JSON files, stores it in MongoDB, and optionally uses Redis for caching/deduplication.
The pipeline will:
1. Read job data from local JSON files
2. Process and extract relevant information
3. Store the data in MongoDB
4. Optionally use Redis for caching and deduplication
5. Export the data to a CSV file

## Project Structure

```
├── docker-compose.yaml     # Docker Compose configuration
├── dockerfile              # Docker configuration for the Scrapy service
├── infra/                  # Infrastructure module
│   ├── mongodb_connector.py  # MongoDB connection and operations
│   └── redis_connector.py    # Redis connection and caching (optional)
├── jobs_project/           # Scrapy project
│   ├── scrapy.cfg            # Scrapy configuration
│   └── jobs_project/         # Scrapy project module
│       ├── __init__.py
│       ├── items.py          # Item definitions
│       ├── middlewares.py    # Middleware components
│       ├── pipelines.py      # Item pipelines
│       ├── settings.py       # Scrapy settings
│       └── spiders/          # Spiders directory
│           ├── __init__.py
│           └── json_spider.py  # Spider for JSON files
├── data/                   # Data directory for JSON files
│   ├── s01.json              # Source JSON file 1
│   └── s02.json              # Source JSON file 2
├── query.py                # Script to query MongoDB and export data
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies
```

## Setup and Installation

1. Make sure Docker and Docker Compose are installed on your system.
2. Clone this repository.
3. Place JSON files with jobs array in the `data/` directory.
4. Run the following command to start the services:

   ```bash
   docker-compose up -d
   ```

## Running the Pipeline

You might require sudo access in certain cases. If you get permission denied run the commands below with sudo prefix

1. Start the containers:

   ```bash
   docker-compose up -d
   ```

2. Execute the Scrapy spider to process the JSON files:

   ```bash
    docker compose exec scrapy bash
    cd jobs_project
    scrapy crawl job_spider

   ```

3. Query the database and export the data:

   ```bash
   docker-compose exec scrapy python query.py
   ```

4. The exported CSV file will be available in the `output/` directory.

## Stopping the Pipeline

To stop the containers:

```bash
docker-compose down
```

To remove the containers and volumes:

```bash
docker-compose down -v
```
