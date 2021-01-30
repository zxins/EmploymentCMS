# -*- coding: utf-8 -*-
import json
import re
import sqlite3

import requests
from lxml import etree
from tqdm import tqdm

headers = {
    "Host": "search.51job.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()


def get_jobs():
    url = "http://tjus.bysjy.com.cn/module/getjobs"
    params = {
        'start': 0,
        'count': 16,
        'type_id': 1,
        'is_practice': 0
    }

    for i in range(0, 100000, params['count'] - 1):
        print(i)
        r = requests.get(url, params=params)
        jobs = r.json()['data']
        items = []
        for job in jobs:
            item = {}
            item['company_name'] = job['company_name']
            item['title'] = job['job_name']
            item['education'] = job['degree_require'][:2]
            salary = job['salary']
            split_salay = salary.split('-')
            item['min_salary'] = float(split_salay[0].strip('K'))
            item['max_salary'] = float(split_salay[-1].strip('K/月'))
            item['work_area'] = job['city_name'].split(' ')[0]
            item['company_size'] = job['scale']
            item['detail'] = get_detail(job['publish_id'])
            items.append(item)
        save_to_db(items)
        if len(jobs) < params['count']:
            break


def get_detail(publish_id):
    url = f"http://tjus.bysjy.com.cn/detail/getjobdetail?publish_id={publish_id}"
    r = requests.get(url)
    info = r.json()['data']

    job_descript = info['job_descript']
    job_require = info['job_require']
    detail = f"""
    <p>岗位职责：</p>
    {job_descript}

    <p>岗位要求：</p>
    {job_require}
    """.replace("<p>", "").replace("</p>", "\n").replace(" ", "")
    return detail


def save_to_db(items):
    # sql_text = "insert into enterprise_jobs (`company_name`, `title`, `min_salary`, `max_salary`, `education`," \
    #            "`work_area`, `company_type`, `company_size`, `detail`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"

    sql_text = "insert into enterprise_jobs (`company_name`, `title`, `min_salary`, `max_salary`, `education`," \
               "`work_area`,  `company_size`, `detail`) values (?, ?, ?, ?, ?, ?, ?, ?)"

    rows = []
    for item in items:
        # 顺序应与sql_text保持相互一致
        row = (
            item['company_name'],
            item['title'],
            item['min_salary'],
            item['max_salary'],
            item['education'],
            item['work_area'],
            item['company_size'],
            item['detail']
        )
        rows.append(row)
    cursor.executemany(sql_text, rows)
    db.commit()


if __name__ == '__main__':
    get_jobs()
