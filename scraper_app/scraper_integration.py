"""
Integration module between web scraper and database CRUD operations.

Handles running scrape jobs, storing results in the database.
"""

import json
from typing import Optional
import sys
import os

# Add parent directory to path to import scraper module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.bs_scraper import BsScraper
from scraper_app.crud import CRUDOperations


class ScraperIntegration:
    """
    Bridge between BsScraper and CRUDOperations.
    
    Orchestrates the scraping process and saves results to the database.
    
    Attributes:
        crud (CRUDOperations): Database operations handler.
    """
    
    def __init__(self):
        """Initialize integration with CRUD operations."""
        self.crud = CRUDOperations()
    
    def run_scrape_job(self, job_id: int) -> bool:
        """
        Execute a scrape job and store results in the database.
        
        Args:
            job_id (int): The job ID to run (must exist in database).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Fetch job configuration from database
            job = self.crud.get_scrape_job(job_id)
            if not job:
                print(f"Job {job_id} not found")
                return False
            
            # Update job status to 'running'
            self.crud.update_job_status(job_id, "running")
            
            # Initialize and run scraper
            print(f"Starting scrape job: {job['name']}")
            bs_scraper = BsScraper(link=job['url'], mode=job['scraper_type'])
            
            # Fire the scraper and get results
            scraped_data = bs_scraper.scrap()
            
            # Store results in database
            if scraped_data:
                data_json = json.dumps(scraped_data, indent=2, ensure_ascii=False)
                success = self.crud.insert_scraped_data(job_id, data_json)
                
                if success:
                    # Update job status to 'completed'
                    self.crud.update_job_status(job_id, "completed")
                    print(f"Scrape job {job_id} completed successfully")
                    return True
            
            # If no data scraped, mark as failed
            self.crud.update_job_status(job_id, "failed")
            print(f"Scrape job {job_id} returned no data")
            return False
            
        except Exception as e:
            print(f"Error running scrape job {job_id}: {e}")
            self.crud.update_job_status(job_id, "failed")
            return False
