# LinkedIn Python Scrapper

This is an initial project to scrape LinkedIn jobs based on a keyword search.

## Requirements
- Python v3.10 or above
- pip3
- Scrapy Framework
- Python Pandas

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
scrapy crawl linkedIn -o results.json
```

This command will execute the spider to scrape LinkedIn jobs for **Full Stack Developer** in the *United States** in the past 24 hours.

### Step 5: Deactivate the Virtual Environment
```bash
deactivate
```

This deactivates the virtual environment when you're done with your project.

## Spider Details
The spider is defined in the ```JobScrapping/spiders/LinkedIn.py``` file. The spider name is **linkedIn**. Make sure to use this name when running the scrapy crawl command.

## Note
- The spider currently does not use rotating proxies or customized request headers.
- If you encounter any issues seek help from the project contributors.

