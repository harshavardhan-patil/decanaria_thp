import scrapy

class JobItem(scrapy.Item):
    # Basic job information
    job_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    
    # Location details
    location = scrapy.Field()
    
    # Job metadata
    employment_type = scrapy.Field()
    hiring_organization = scrapy.Field()
    categories = scrapy.Field()
    apply_url = scrapy.Field()
    
    # Timestamps
    create_date = scrapy.Field()
    update_date = scrapy.Field()
    
    # Additional field for processing metadata
    metadata = scrapy.Field()