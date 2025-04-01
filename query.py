import pandas as pd
import os
import logging
from infra.mongodb_connector import MongoDBConnector

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize MongoDB connector
    mongo_connector = MongoDBConnector()
    if not mongo_connector.connect():
        logging.error("Failed to connect to MongoDB")
        return
    
    try:
        # Retrieve all jobs from the database
        jobs = mongo_connector.find_all('jobs')
        
        if not jobs:
            logging.warning("No jobs found in the database")
            return
            
        logging.info(f"Retrieved {len(jobs)} jobs from MongoDB")
        
        # Convert to a Pandas DataFrame
        df = pd.json_normalize(jobs)
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Export to CSV
        csv_path = 'output/final_jobs.csv'
        df.to_csv(csv_path, index=False)
        
        logging.info(f"Exported jobs data to {csv_path}")
        
    except Exception as e:
        logging.error(f"Error retrieving or exporting jobs: {str(e)}")
        
    finally:
        # Close the MongoDB connection
        mongo_connector.close()

if __name__ == "__main__":
    main()