import os
from zoneinfo import ZoneInfo
from datetime import datetime
import logging
import requests
import json

SH_TZ = ZoneInfo("Asia/Shanghai")

def LeetCode_contests(json_file: str):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if os.path.exists(json_file):
        contests = json.loads(open(json_file, "r").read())
    else:
        contests = {}
    
    url = "https://leetcode.cn/graphql"
    payload = {
        "query": """
        {
        contestUpcomingContests {
            containsPremium
            title
            cardImg
            titleSlug
            description
            startTime
            duration
            originStartTime
            isVirtual
            isLightCardFontColor
            company {
            watermark
            __typename
            }
            __typename
        }
        }
        """
    }
    response = requests.post(url, json=payload)
    leetcode_contests = response.json()['data']['contestUpcomingContests']
    contests = {}
    
    for contest in leetcode_contests:
        contest_id = f'Leetcode_{contest["titleSlug"]}'
        contests[contest_id] = {}
        contests[contest_id]['summary'] = contest['title']
        contests[contest_id]['description'] = f'https://leetcode.cn/contest/{contest["titleSlug"]}'
        contests[contest_id]['dtstart'] = datetime.fromtimestamp(contest['startTime'], tz=SH_TZ).isoformat()
        contests[contest_id]['dtend'] = datetime.fromtimestamp(contest['startTime'] + contest['duration'], tz=SH_TZ).isoformat()
        contests[contest_id]['url'] = f'https://leetcode.cn/contest/{contest["titleSlug"]}'
        logging.info(f'{contest["title"]} has processed')
    json.dump(contests, open(json_file, 'w'), indent=4)

    logging.info(f'{len(leetcode_contests)} contests found in LeetCode')

if __name__ == '__main__':
    LeetCode_contests('json/LeetCodeContests.json')