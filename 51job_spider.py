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


def get_items(url):
    res = requests.get(url, headers=headers)
    re_result = re.search('window.__SEARCH_RESULT__ = ({.*})', res.text).group(1)
    json_result = json.loads(re_result)

    engine_search_result = json_result['engine_search_result']

    items = []
    for row in engine_search_result:
        item = {}
        salary = row['providesalary_text']
        if not salary:
            continue
        if '元/天' in salary:
            continue
        if '以下' in salary:
            continue

        if '千/月' in salary:
            sal = salary.strip('千/月')
            min_salary = float(sal.split('-')[0])
            max_salary = float(sal.split('-')[1])
        elif '万/月' in salary:
            sal = salary.strip('万/月')
            min_salary = float(sal.split('-')[0]) * 10
            max_salary = float(sal.split('-')[1]) * 10
        else:
            continue
        item['min_salary'] = min_salary
        item['max_salary'] = max_salary
        item['title'] = row['job_title']
        item['company_name'] = row['company_name']
        item['work_area'] = row['workarea_text']
        item['company_type'] = row['companytype_text']
        item['company_size'] = row['companysize_text']
        education = row['attribute_text'][2]
        item['education'] = '不限' if '人' in education else education
        item['detail'] = position_detail(row['job_href'])
        items.append(item)
    return items


def position_detail(url):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.content)
    rows = html.xpath('//div[@class="bmsg job_msg inbox"]/p')

    detail = ''
    for row in rows:
        detail += row.xpath('string()')
    return detail


def save_to_db(items):
    # sql_text = "insert into enterprise_jobs (`company_name`, `title`, `min_salary`, `max_salary`, `education`," \
    #            "`work_area`, `company_type`, `company_size`, `detail`) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"

    sql_text = "insert into enterprise_jobs (`company_name`, `title`, `min_salary`, `max_salary`, `education`," \
               "`work_area`, `company_type`, `company_size`, `detail`) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"

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
            item['company_type'],
            item['company_size'],
            item['detail']
        )
        rows.append(row)
    cursor.executemany(sql_text, rows)
    db.commit()


if __name__ == '__main__':
    # position_detail('https://jobs.51job.com/beijing/124060951.html?s=01&t=0')

    # 搜索条件
    # 工作地点：北京
    # 职能：Java开发工程师、C/C++开发工程师、Python开发工程师
    # 工作年限：在校生/应届生
    for i in tqdm(range(1, 7)):
        root_url = "https://search.51job.com/list/010000,000000,0124%252c0121%252c0122,00,9,99,+,2,{}.html?lang=c&postchannel=0000&workyear=01&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        url = root_url.format(str(i))
        items = get_items(url)
        save_to_db(items)

    db.close()
