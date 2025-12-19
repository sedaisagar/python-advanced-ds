# 🕷️ Web Scraper Application

A desktop application for managing and executing web scraping jobs with persistent storage.

## 📊 Architecture Flow

```
Desktop Application (UI)
    ↓
Scripts To Scrap (Job Configuration)
    ↓
Scraper (BsScraper) ← Web Source
    ↓
Database (CRUD - Store & Retrieve Data)
```

---

## 🚀 Quick Start

### Installation

```bash
pip install beautifulsoup4 requests
```

### Run the Application

```bash
python main.py
```

---

## 📁 Project Structure

```
python-advanced/
├── main.py                          # Entry point
├── scraper/
│   └── bs_scraper.py               # BeautifulSoup scraper (untouched)
├── scraper_app/
│   ├── __init__.py
│   ├── ui.py                       # Desktop UI (tkinter)
│   ├── crud.py                     # Database operations
│   ├── scraper_integration.py      # Scraper ↔ Database bridge
│   └── scraper_app.db              # SQLite database (auto-created)
```

---

## 🔧 Components

### 1. **Desktop Application (ui.py)**
- Tkinter-based GUI
- Job management interface
- Results viewer
- Real-time status updates

**Features:**
- Create new scrape jobs
- Run selected jobs
- View scraped results
- Delete jobs
- Refresh job list

### 2. **Scraper (bs_scraper.py)**
- BeautifulSoup web scraper
- Two modes:
  - **"quote"**: Scrape quotes from quotes.toscrape.com
  - **"sidhakura"**: Scrape news from sidhakura.com/society
- Automatic pagination handling
- Multi-page recursion

**Usage:**
```python
from scraper.bs_scraper import BsScraper

# Scrape news
scraper = BsScraper(
    link="https://www.sidhakura.com/society",
    mode="sidhakura"
)
news_data = scraper.scrap()

# Returns:
# [
#   {"title": "...", "image": "...", "date": "..."},
#   {"title": "...", "image": "...", "date": "..."},
#   ...
# ]
```

### 3. **Scraper Integration (scraper_integration.py)**
- Bridges scraper and database
- Fetches job configuration from DB
- Runs scraper with job parameters
- Stores results as JSON in database
- Updates job status (running → completed/failed)

**Usage:**
```python
from scraper_app.scraper_integration import ScraperIntegration

integration = ScraperIntegration()
success = integration.run_scrape_job(job_id=1)
```

### 4. **Database CRUD (crud.py)**
- SQLite database for persistent storage
- Three tables:
  - `scrape_jobs`: Job configurations
  - `scraped_data`: Scraped results (JSON)
  - `user_config`: User preferences

**Database Schema:**

```sql
-- Scrape Jobs Table
CREATE TABLE scrape_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    scraper_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scraped Data Table
CREATE TABLE scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    data TEXT NOT NULL,          -- Stored as JSON
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES scrape_jobs(id)
);

-- User Config Table
CREATE TABLE user_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📋 Workflow

### Creating a Job

1. Click **"New Job"** button in UI
2. Enter:
   - **Job Name**: Unique identifier
   - **URL**: Website to scrape
   - **Scraper Type**: "beautifulsoup", "scrapy", or "selenium"
3. Click **"Create"** → Job saved in database

### Running a Job

1. Select job from list
2. Click **"Run Selected"** button
3. Application:
   - Fetches job config from database
   - Initializes BsScraper with URL + mode
   - Executes scraper
   - Converts results to JSON
   - Stores in database
   - Updates status to "completed"
4. View results in right panel

### Viewing Results

1. Select job from list
2. Results display automatically:
   - Parses stored JSON
   - Pretty-prints each item
   - Shows scrape timestamp

### Deleting a Job

1. Select job from list
2. Click **"Delete Job"**
3. Confirm deletion
4. Job and all associated data removed

---

## 📊 Job Status States

| Status | Meaning |
|--------|---------|
| `pending` | Job created, not yet run |
| `running` | Job currently executing |
| `completed` | Job finished successfully |
| `failed` | Job encountered an error |

---

## 🔗 Data Flow Example: Scraping Sidhakura News

```
User Action: Click "Run Selected"
    ↓
UI._run_job()
    ↓
scraper_integration.run_scrape_job(job_id=1)
    ↓
CRUD.get_scrape_job(1)
    Returns: {
        id: 1,
        name: "Sidhakura News",
        url: "https://www.sidhakura.com/society",
        scraper_type: "sidhakura",
        status: "pending"
    }
    ↓
CRUD.update_job_status(1, "running")
    ↓
BsScraper(
    link="https://www.sidhakura.com/society",
    mode="sidhakura"
).scrap()
    ↓
Returns: [
    {
        "title": "Breaking News",
        "image": "https://...",
        "date": "2024-01-15"
    },
    ...
]
    ↓
Convert to JSON string
    ↓
CRUD.insert_scraped_data(job_id=1, data=json_string)
    ↓
CRUD.update_job_status(1, "completed")
    ↓
UI._display_job_results()
    Fetches from DB and displays formatted results
```

---

## 🛠️ Supported Scrapers

### BeautifulSoup (Currently Implemented)

- **Mode: "quote"**
  - Source: quotes.toscrape.com
  - Returns: List of quote strings

- **Mode: "sidhakura"**
  - Source: sidhakura.com/society
  - Returns: List of news dicts with title, image, date

### Extensibility

To add new scraper modes:

1. Add method in `BsScraper` class
2. Add case in `BsScraper.scrap()` match statement
3. Add combobox option in `ui.py` `_open_new_job_dialog()`

---

## 💾 Database Operations

### Create Job
```python
crud = CRUDOperations()
job_id = crud.create_scrape_job(
    name="My Job",
    url="https://example.com",
    scraper_type="beautifulsoup"
)
```

### Get All Jobs
```python
jobs = crud.get_all_jobs()
# Returns: List of job dicts
```

### Get Job Results
```python
results = crud.get_job_data(job_id=1)
# Returns: List of scraped data records with JSON
```

### Update Job Status
```python
crud.update_job_status(job_id=1, status="completed")
```

### Delete Job
```python
crud.delete_scrape_job(job_id=1)
```

---

## 🔍 Troubleshooting

### Issue: "Connection refused" error
**Solution**: Ensure the website is accessible and not blocked

### Issue: No results displayed
**Solution**: 
- Check job status is "completed"
- Verify HTML selectors match the website structure
- Run job again

### Issue: Database locked
**Solution**: Close all instances and delete `scraper_app.db`, restart app

---

## 📝 Notes

- Results are stored as JSON in the database for flexibility
- Each scrape job maintains separate result records
- Job history is preserved for reference
- Database is automatically created on first run

---

## 🎯 Future Enhancements

- [ ] Add progress bar for long-running jobs
- [ ] Export results to CSV/Excel
- [ ] Schedule jobs to run automatically
- [ ] Add more scraper modes (Scrapy, Selenium)
- [ ] Multi-threaded job execution
- [ ] Result filtering and search
