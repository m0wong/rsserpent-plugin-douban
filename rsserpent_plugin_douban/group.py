import datetime
from typing import Any, Dict

import arrow
import lxml.html
import requests
from rsserpent.utils import cached


path = "/douban/group/{gid}/"


def timeHandler(t):
    # 02-16 13:21
    if t.find(':') != -1:
        year = datetime.datetime.now().year
        t = f'{year}-{t}'
    # 2021-12-22
    else:
        t = f'{t} 00:00'
    return t


@cached
async def provider(gid: str) -> Dict[str, Any]:
    """订阅小组讨论。"""
    url = f'https://m.douban.com/group/{gid}/'
    base_url = 'https://m.douban.com{href}'
    headers = {
        'Host': 'm.douban.com',
        'Referer': 'https://m.douban.com/group/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
    }
    author = ''
    items = []
    try:
        r = requests.get(url, headers=headers)
        root = lxml.html.fromstring(r.content.decode('utf-8'))
        author = root.xpath('//title/text()')[0].split('-')[0].strip()
        for a in root.xpath('//li[@class="topic-item"]/a[@class="item-containor"]'):
            item = {}
            href = a.xpath('@href')[0]
            if len(href.split('&amp;')) > 1:
                href = href.split('&amp;')[1]
            item['link'] = base_url.format(href=href)
            d = a.xpath('div[@class="content"]')[0]
            title = d.xpath('h3[@class="title"]/text()')[0]
            degree = d.xpath('*/span[@class="reply-num"]/text()')[0]
            item['title'] = '[{degree}]{title}'.format(degree=degree, title=title)
            time = d.xpath('*/time/text()')[0]
            item['time'] = timeHandler(time)
            item['cover'] = ''
            if a.xpath('div[@class="topic-cover"]/img/@src'):
                item['cover'] = a.xpath('div[@class="topic-cover"]/img/@src')[0]
            items.append(item)
        # pubdate = items[0]['time']
    except Exception:
        pass
    return {
        "title": f"{author}的讨论",
        "link": f"https://www.douban.com/group/{gid}/",
        "description": f"{author}的讨论",
        "items": [
            {
                "title": item["title"],
                "description": '',
                "link": item["link"],
                "pub_date": arrow.get(item["time"]),
                "author": author,
                "cover": item['cover']
            }
            for item in items
        ],
    }
