"""
CRUD (Create, Read, Update, Delete) operations for scraper app data management.

This module provides database operations for storing and retrieving scraped data,
user configurations, and application state. It abstracts the persistence layer
from the UI and business logic.
"""

from typing import List, Dict, Any, Optional
import sqlite3


class CRUDOperations:
    """
    Handles all database CRUD operations for the scraper application.
    
    Attributes:
        db_path (str): Path to the SQLite database file.
        connection (sqlite3.Connection): Active database connection.
    """
    
    def __init__(self, db_path: str = "scraper_app.db"):
        """
        Initialize CRUD operations with a database connection.
        
        Args:
            db_path (str): Path to the SQLite database. Defaults to 'scraper_app.db'.
        """
        self.db_path = db_path
        self.connection = None
        self.connect()
    
    def connect(self) -> None:
        """
        Establish connection to the SQLite database.
        Creates database file if it doesn't exist.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def create_tables(self) -> None:
        """
        Create necessary database tables if they don't exist.
        Tables: scrape_jobs, scraped_data, user_config
        """
        cursor = self.connection.cursor()
        
        # Table for storing scrape job configurations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scrape_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                scraper_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table for storing scraped data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES scrape_jobs(id)
            )
        """)
        
        # Table for user configuration and preferences
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        print("Database tables created/verified")
    
    # ============ CREATE Operations ============
    
    def create_scrape_job(self, name: str, url: str, scraper_type: str) -> Optional[int]:
        """
        Create a new scrape job record.
        
        Args:
            name (str): Unique name for the scrape job.
            url (str): URL to scrape.
            scraper_type (str): Type of scraper (e.g., 'beautifulsoup', 'scrapy').
        
        Returns:
            Optional[int]: Job ID if successful, None otherwise.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO scrape_jobs (name, url, scraper_type)
                VALUES (?, ?, ?)
            """, (name, url, scraper_type))
            self.connection.commit()
            job_id = cursor.lastrowid
            print(f"Scrape job '{name}' created with ID {job_id}")
            return job_id
        except sqlite3.IntegrityError:
            print(f"Error: Job name '{name}' already exists")
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def insert_scraped_data(self, job_id: int, data: str) -> bool:
        """
        Insert scraped data associated with a scrape job.
        
        Args:
            job_id (int): Foreign key referencing the scrape job.
            data (str): Serialized scraped data (JSON recommended).
        
        Returns:
            bool: True if insertion successful, False otherwise.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO scraped_data (job_id, data)
                VALUES (?, ?)
            """, (job_id, data))
            self.connection.commit()
            print(f"Data inserted for job ID {job_id}")
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    # ============ READ Operations ============
    
    def get_scrape_job(self, job_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single scrape job by ID.
        
        Args:
            job_id (int): The job ID to retrieve.
        
        Returns:
            Optional[Dict]: Job record as dictionary, None if not found.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM scrape_jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        Retrieve all scrape jobs.
        
        Returns:
            List[Dict]: List of all job records.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM scrape_jobs ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_job_data(self, job_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve all scraped data for a specific job.
        
        Args:
            job_id (int): The job ID to query.
        
        Returns:
            List[Dict]: List of scraped data records.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM scraped_data 
            WHERE job_id = ? 
            ORDER BY scraped_at DESC
        """, (job_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # ============ UPDATE Operations ============
    
    def update_job_status(self, job_id: int, status: str) -> bool:
        """
        Update the status of a scrape job.
        
        Args:
            job_id (int): The job ID to update.
            status (str): New status (e.g., 'pending', 'running', 'completed', 'failed').
        
        Returns:
            bool: True if update successful, False otherwise.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE scrape_jobs SET status = ? WHERE id = ?
            """, (status, job_id))
            self.connection.commit()
            print(f"Job {job_id} status updated to '{status}'")
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    # ============ DELETE Operations ============
    
    def delete_scrape_job(self, job_id: int) -> bool:
        """
        Delete a scrape job and its associated data.
        
        Args:
            job_id (int): The job ID to delete.
        
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        try:
            cursor = self.connection.cursor()
            # Delete associated scraped data first (foreign key constraint)
            cursor.execute("DELETE FROM scraped_data WHERE job_id = ?", (job_id,))
            # Delete the job itself
            cursor.execute("DELETE FROM scrape_jobs WHERE id = ?", (job_id,))
            self.connection.commit()
            print(f"Job {job_id} and its data deleted")
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def set_config(self, key: str, value: str) -> bool:
        """
        Set or update a configuration value.
        
        Args:
            key (str): Configuration key.
            value (str): Configuration value.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_config (key, value)
                VALUES (?, ?)
            """, (key, value))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_config(self, key: str) -> Optional[str]:
        """
        Retrieve a configuration value.
        
        Args:
            key (str): Configuration key.
        
        Returns:
            Optional[str]: Configuration value, None if not found.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM user_config WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None
