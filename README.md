# LinkedIn Python Scrapper

This project allows you to scrape LinkedIn jobs based on a keyword search.

## Requirements
- Python v3.10 or above: Required to run the Python scripts.
- pip3: Package installer for Python.
- Scrapy Framework: Python framework for web scraping.

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/LinkedInScrapperPython.git
```

```bash
cd LinkedInScrapperPython
```

### Step 2: Create and Activate a Virtual Environment

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```


### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Scrapy Spider

```bash
scrapy crawl linkedIn -o results.json -a job_title="Full Stack Developer" -a location="United States" -a work_preference="remote"
```

Replace the values in quotes with your desired parameters:

- ```job_title```: The job title to search for (default: "Full Stack Developer").
- ```location```: The location for job search (default: "United States").
- ```work_preference```: The work preference, such as "remote," "on-site," or "hybrid" (default: "remote").

### Step 5: Deactivate the Virtual Environment
```bash
deactivate
```

This deactivates the virtual environment when you're done with your project.

## Spider Details
The spider is defined in the ```JobScrapping/spiders/LinkedIn.py``` file. The spider name is **linkedIn**. Make sure to use this name when running the scrapy crawl command.

## Note
  If you encounter any issues seek help from the project contributors.
  

