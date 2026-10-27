#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def fetch_trending(limit=5):
    # Fetch GitHub trending RSS feed for 'ai' category
    url = 'https://mshibanami.github.io/GitHubTrendingRSS/daily/ai.xml'
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.findall('./channel/item'):
            title = item.findtext('title')
            link = item.findtext('link')
            desc = item.findtext('description') or 'N/A'
            items.append({'title': title, 'link': link, 'desc': desc})
        return items[:limit]
    except Exception as e:
        return [{'error': str(e)}]

def summarize(item):
    # Extract repo name from title like 'Repo: AIHOT - Desc: ...'
    parts = item['title'].split(' - ')
    if len(parts) >= 2:
        repo = parts[0].replace('Repo: ', '').strip()
        desc = parts[1].replace('Desc: ', '').strip()
    else:
        repo = item['title']
        desc = item['desc']
    return repo, desc

if __name__ == '__main__':
    print('Daily AI Radar - Trending repos')
    print('='*30)
    items = fetch_trending(5)
    for item in items:
        if 'error' in item:
            print(f"Error: {item['error']}")
        else:
            repo, desc = summarize(item)
            print(f"\nRepo: {repo}")
            print(f"Desc: {desc[:100]}...")  # Truncate long descriptions
            print(f"Link: {item['link']}")
    print("\nGenerated at:", datetime.now().strftime('%Y-%m-%d %H:%M'))
