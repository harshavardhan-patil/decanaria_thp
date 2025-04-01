BOT_NAME = 'jobs_project'

SPIDER_MODULES = ['jobs_project.spiders']
NEWSPIDER_MODULE = 'jobs_project.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # We're scraping local files, so this isn't needed

# Configure item pipelines
ITEM_PIPELINES = {
    'jobs_project.pipelines.MongoDBPipeline': 300,
    'jobs_project.pipelines.RedisPipeline': 400,
}

# Enable logging
LOG_LEVEL = 'INFO'

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8