# LinkedInScrapperPython
This is an initial project to scrape linkedIn jobs based on keyword search


## Requirements
- python v3.10
- Scrapy Framework
- Python Pandas

### Running the Spider

This project contains Scrapy Framework to scrape linkedin jobs for Full Stack Developer in the last 24 hours.
This is just a test project and does not currently use rotating proxies or customised request headers.
This project returns a json object of all the jobs for 'Full Stack Developer' in the last 24 hours.

In order to run the project, do the following:

- make sure system fulfills the requirements.
- Use command <b>'scrapy crawl LinkedIn -O results.json'</b>
The above command will take the spider to crawl linkedin Domain and return a Json object of all the jobs for 'Full Stack Developer' in the United states in Past 24 Hours.
