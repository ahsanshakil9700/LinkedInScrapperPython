import scrapy
import pandas as pd
from w3lib.html import remove_tags
import time
import random

jobs_scrapped = []


class LinkedJobsSpider(scrapy.Spider):
    name = "linkedIn"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Full%20Stack%20Developer' \
              '&location=United%20States&locationId=&geoId=103644278&sortBy=R&f_TPR=r86400&position=1&pageNum=0&start='
    jobs_scraped_count = 0
    retry_delay = 5

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_jobs, meta={'first_job_on_page': first_job_on_page})

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

        if num_jobs_returned > 0:
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
