import scrapy
import pandas as pd
from w3lib.html import remove_tags
import time
import argparse
jobs_scrapped = []


class LinkedJobsSpider(scrapy.Spider):
    name = "linkedIn"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'

    jobs_scraped_count = 0
    retry_delay = 5

    def __init__(self, *args, **kwargs):
        super(LinkedJobsSpider, self).__init__(*args, **kwargs)
        self.job_title = kwargs.get('job_title', 'Full Stack Developer')
        self.location = kwargs.get('location', 'United States')
        self.preference = kwargs.get('work_preference', 'remote')
        self.max_jobs = int(kwargs.get('max_jobs', float('inf')))
    def start_requests(self):
        first_job_on_page = 0
        # Set values and replace spaces with '%'
        job_title = self.job_title.replace(" ", "%20")
        location = self.location.replace(" ", "%20")
        preference = self.get_work_preference(self.preference)

        start_url = f'{self.api_url}?keywords={job_title}&location={location}&sortBy=R&{preference}&f_TPR=r86400&f_WT=2&position=1&pageNum=0&start=0'

        yield scrapy.Request(url=start_url, callback=self.parse_jobs, meta={'first_job_on_page': first_job_on_page})
    
    def get_work_preference(self, input_string):
        preferences = {
            'remote': 'f_WT=2',
            'on-site': 'f_WT=1',
            'hybrid': 'f_WT=3'
        }

        lower_input = input_string.lower()
        return preferences.get(lower_input, 'remote')

    def parse_jobs(self, response):
        first_job_on_page = response.meta['first_job_on_page']
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print('*****')
        self.jobs_scraped_count += num_jobs_returned

        for job in jobs:
            time.sleep(5)
            follow_job = job.css(".base-card__full-link::attr(href)").get()
            if follow_job:
                yield response.follow(follow_job,
                                      callback=self.parse_description, errback=self.handle_error_response)

        if self.jobs_scraped_count % 50 == 0:
            print(f'***** WAITING 10 SECONDS AFTER SCRAPING {self.jobs_scraped_count} JOBS *****')
            time.sleep(10)

        if num_jobs_returned > 0 and self.jobs_scraped_count < self.max_jobs:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            time.sleep(3)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_jobs,
                meta={'first_job_on_page': first_job_on_page},
                errback=self.handle_error_response,
            )

    def handle_error_response(self, failure):
        request = failure.request
        print(f"Received {failure.value.response.status} error for {request.url}")
        print(f"Retrying request after {self.retry_delay} seconds...")
        time.sleep(self.retry_delay)
        return scrapy.Request(
            url=request.url,
            callback=request.callback,
            meta=request.meta,
            errback=request.errback,
            dont_filter=True,
        )

    def parse_description(self, response):
        job_item = {'job_title': response.css("h1::text").get(default='not-found').strip(),
                    'job_detail_url': response.request.url, 'job_description': remove_tags(
                str(response.css('div.description__text.description__text--rich').getall())).strip(),
                    'job_listed': response.css("span.posted-time-ago__text::text").get(default='not-found').strip(),
                    'company_name': response.css('h4 a::text').get(default='not-found').strip(),
                    'company_link': response.css('h4 a::attr(href)').get(default='not-found'),
                    'company_location': response.css("h4 span.topcard__flavor.topcard__flavor--bullet::text").get(
                        default='not-found').strip(), 'seniority_level': response.css(
                ".description__job-criteria-text.description__job-criteria-text--criteria::text").get(
                default='not-found').strip()}
        jobs_scrapped.append(job_item)
        yield job_item

    def close(spider, reason):
        df = pd.DataFrame(jobs_scrapped)
        df.to_csv('jobs.csv', index=False)
        print(df.head())
