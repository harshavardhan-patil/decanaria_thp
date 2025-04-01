import json
import scrapy
import os
from pathlib import Path
from ..items import JobItem
import glob

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    
    def __init__(self, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        # Set default paths to JSON files
        self.json_files = glob.glob("/decanaria_thp/data/*.json")
        self.logger.info(f"JSON Files: {self.json_files}")
    
    def start_requests(self):
        # Just yield a dummy request to trigger the spider
        yield scrapy.Request(url='file:///dev/null', callback=self.parse_files)
    
    def parse_files(self, response):
        # Process each JSON file directly
        for json_file in self.json_files:
            self.logger.info(f"Processing file: {json_file}")
            
            try:
                # Read and parse the file directly
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    self.logger.info(f"Successfully loaded JSON from {json_file}")
                    
                    # Check for jobs key
                    if 'jobs' not in data:
                        self.logger.error(f"No 'jobs' key in {json_file}")
                        self.logger.info(f"Available keys: {list(data.keys())}")
                        continue
                    
                # Process each job entry
                for job_entry in data['jobs']:
                    # Extract job data from the entry
                    job_data = job_entry.get('data', {})
                    
                    # Create a JobItem with the extracted data
                    job_item = JobItem(
                        job_id=job_data.get('req_id', ''),
                        title=job_data.get('title', ''),
                        description=job_data.get('description', ''),
                        location={
                            'street_address': job_data.get('street_address', ''),
                            'city': job_data.get('city', ''),
                            'state': job_data.get('state', ''),
                            'country_code': job_data.get('country_code', ''),
                            'postal_code': job_data.get('postal_code', ''),
                            'latitude': job_data.get('latitude'),
                            'longitude': job_data.get('longitude')
                        },
                        employment_type=job_data.get('employment_type', ''),
                        hiring_organization=job_data.get('hiring_organization', ''),
                        categories=job_data.get('categories', []), # Not sure how to handle multiple categories...
                        apply_url=job_data.get('apply_url', ''),
                        create_date=job_data.get('create_date', ''),
                        update_date=job_data.get('update_date', '')
                    )
                    
                    yield job_item
                        
            except FileNotFoundError:
                self.logger.error(f"File not found: {json_file}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in {json_file}: {str(e)}")
            except Exception as e:
                self.logger.error(f"Error processing {json_file}: {str(e)}")