"""
Desktop UI module for the scraper application.

Two-page interface:
- Home Page: Create jobs and quick scrape
- Results Page: View all scraped news/data from database
"""

from typing import Optional
import tkinter as tk
from tkinter import ttk, messagebox
import json
from scraper_app.crud import CRUDOperations
from scraper_app.scraper_integration import ScraperIntegration


class DeskTopApp:
    """
    Main desktop application with tabbed interface.
    
    Attributes:
        root (tk.Tk): Root tkinter window.
        crud (CRUDOperations): Database operations.
        scraper_integration (ScraperIntegration): Scraper integration.
        notebook (ttk.Notebook): Tabbed interface.
    """
    
    def __init__(self):
        """Initialize desktop application."""
        self.root = tk.Tk()
        self.root.title("Web Scraper Application")
        self.root.geometry("1000x650")
        
        # Initialize database and scraper
        self.crud = CRUDOperations()
        self.crud.create_tables()
        self.scraper_integration = ScraperIntegration()
        
        # Create tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create two pages
        self.home_frame = ttk.Frame(self.notebook)
        self.results_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.home_frame, text="Home - Scrape")
        self.notebook.add(self.results_frame, text="Results - View Data")
    
    def initiate(self) -> None:
        """Launch the application UI."""
        self._create_home_page()
        self._create_results_page()
        self.root.mainloop()
    
    # ============ HOME PAGE ============
    
    def _create_home_page(self) -> None:
        """Create home page with scrape configurations and quick buttons."""
        main_container = ttk.Frame(self.home_frame, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="🕷️ Web Scraper",
            font=('Arial', 20, 'bold')
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_container,
            text="Select a source and click Scrape to get data",
            font=('Arial', 11)
        )
        subtitle_label.pack(pady=5)
        
        # Separator
        ttk.Separator(main_container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Scrape options frame
        options_frame = ttk.LabelFrame(main_container, text="Scrape Options", padding=15)
        options_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scraper source selection
        ttk.Label(options_frame, text="Select Source:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=10
        )
        
        self.scraper_var = tk.StringVar(value="sidhakura")
        
        sources = [
            ("📰 Sidhakura News", "sidhakura"),
            ("💬 Quotes", "quote"),
        ]
        
        for i, (label, value) in enumerate(sources):
            rb = ttk.Radiobutton(
                options_frame,
                text=label,
                variable=self.scraper_var,
                value=value
            )
            rb.grid(row=i+1, column=0, sticky=tk.W, padx=20, pady=5)
        
        # Source details
        details_frame = ttk.LabelFrame(options_frame, text="Source Details", padding=10)
        details_frame.grid(row=1, column=1, rowspan=3, sticky=tk.NSEW, padx=20)
        
        self.details_label = ttk.Label(
            details_frame,
            text=self._get_source_details("sidhakura"),
            font=('Arial', 10),
            justify=tk.LEFT
        )
        self.details_label.pack()
        
        # Bind radio button changes
        def update_details(*args):
            self.details_label.config(text=self._get_source_details(self.scraper_var.get()))
        
        self.scraper_var.trace('w', update_details)
        
        # Scrape button (main action)
        scrape_button = ttk.Button(
            options_frame,
            text="🔄 START SCRAPING",
            command=self._start_scraping
        )
        scrape_button.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=20, padx=20)
        
        # Status label
        self.status_label = ttk.Label(
            main_container,
            text="Ready to scrape",
            font=('Arial', 10),
            foreground="green"
        )
        self.status_label.pack(pady=10)
    
    def _get_source_details(self, source: str) -> str:
        """Get details about a scraper source."""
        details = {
            "sidhakura": "Source: sidhakura.com/society\nData: News articles (title, image, date)\nPages: Up to 10 pages",
            "quote": "Source: quotes.toscrape.com\nData: Quotes\nPages: All available pages"
        }
        return details.get(source, "Unknown source")
    
    def _start_scraping(self) -> None:
        """Start scraping process."""
        source = self.scraper_var.get()
        
        # Preset configurations
        configs = {
            "sidhakura": {
                "name": f"Sidhakura News - {self._get_timestamp()}",
                "url": "https://www.sidhakura.com/society",
                "scraper_type": "sidhakura"
            },
            "quote": {
                "name": f"Quotes - {self._get_timestamp()}",
                "url": "https://quotes.toscrape.com",
                "scraper_type": "quote"
            }
        }
        
        config = configs.get(source)
        if not config:
            messagebox.showerror("Error", "Invalid source selected")
            return
        
        # Update status
        self.status_label.config(text="⏳ Scraping in progress...", foreground="orange")
        self.root.update()
        
        # Create job
        job_id = self.crud.create_scrape_job(config["name"], config["url"], config["scraper_type"])
        
        if not job_id:
            self.status_label.config(text="❌ Failed to create job", foreground="red")
            messagebox.showerror("Error", "Failed to create scrape job")
            return
        
        # Run scraper and store in DB
        success = self.scraper_integration.run_scrape_job(job_id)
        
        if success:
            self.status_label.config(
                text=f"✅ Scraping completed! {job_id} records inserted into database",
                foreground="green"
            )
            messagebox.showinfo("Success", f"Scraping completed!\nGo to 'Results' page to view data.")
            # Auto-switch to results page
            self.notebook.select(1)
            self._refresh_results_page()
        else:
            self.status_label.config(text="❌ Scraping failed", foreground="red")
            messagebox.showerror("Error", "Scraping job failed. Check logs.")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for job naming."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # ============ RESULTS PAGE ============
    
    def _create_results_page(self) -> None:
        """Create results page to view scraped data from database."""
        main_container = ttk.Frame(self.results_frame, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="📊 Scraped Data from Database",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # Job selection frame
        select_frame = ttk.Frame(main_container)
        select_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(select_frame, text="Select Job:").pack(side=tk.LEFT, padx=5)
        
        self.job_combobox = ttk.Combobox(select_frame, state="readonly", width=50)
        self.job_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.job_combobox.bind('<<ComboboxSelected>>', lambda e: self._display_job_data())
        
        refresh_btn = ttk.Button(
            select_frame,
            text="🔄 Refresh",
            command=self._refresh_results_page
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Data display frame
        data_frame = ttk.LabelFrame(main_container, text="Scraped Results", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollable text widget
        scrollbar = ttk.Scrollbar(data_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(
            data_frame,
            height=25,
            width=100,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)
    
    def _refresh_results_page(self) -> None:
        """Refresh job list in results page."""
        jobs = self.crud.get_all_jobs()
        job_names = [f"{j['name']} [{j['status']}]" for j in jobs]
        self.job_combobox['values'] = job_names
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        if jobs:
            self.job_combobox.current(len(jobs) - 1)
            self._display_job_data()
        else:
            self.results_text.insert(tk.END, "No jobs found. Start scraping from the Home page.")
    
    def _display_job_data(self) -> None:
        """Display scraped data for selected job."""
        self.results_text.delete(1.0, tk.END)
        
        # Get selected job
        idx = self.job_combobox.current()
        if idx < 0:
            return
        
        jobs = self.crud.get_all_jobs()
        if idx >= len(jobs):
            return
        
        job = jobs[idx]
        job_id = job['id']
        
        # Display job info
        info_str = f"""
{'='*80}
Job: {job['name']}
Status: {job['status']}
URL: {job['url']}
Type: {job['scraper_type']}
Created: {job['created_at']}
{'='*80}

"""
        self.results_text.insert(tk.END, info_str)
        
        # Fetch and display data
        data_records = self.crud.get_job_data(job_id)
        
        if not data_records:
            self.results_text.insert(tk.END, "No results found for this job.")
            return
        
        # Display each result
        for i, record in enumerate(data_records, 1):
            self.results_text.insert(tk.END, f"\n📋 SCRAPE RESULT {i}\nScraped at: {record['scraped_at']}\n{'-'*80}\n")
            
            try:
                parsed_data = json.loads(record['data'])
                
                if isinstance(parsed_data, list):
                    for item_idx, item in enumerate(parsed_data, 1):
                        self.results_text.insert(tk.END, f"\n  📌 Item {item_idx}:\n")
                        if isinstance(item, dict):
                            for key, value in item.items():
                                self.results_text.insert(tk.END, f"    • {key}: {value}\n")
                        else:
                            self.results_text.insert(tk.END, f"    {item}\n")
                else:
                    self.results_text.insert(tk.END, json.dumps(parsed_data, indent=2, ensure_ascii=False))
                
                self.results_text.insert(tk.END, f"\n{'-'*80}\n")
                
            except json.JSONDecodeError:
                self.results_text.insert(tk.END, f"{record['data']}\n")

