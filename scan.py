import time
import sys
import requests
from datetime import datetime
import pickle

class Scan:
    def __init__(self):
        self.url = "https://apis.naver.com/cafe-home-web/cafe-home/v11/mynews?perPage=20&webDirection=mobile"
        self.header = {
            'Host': 'apis.naver.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://m.cafe.naver.com/ca-fe/home/mynews',
            'X-Cafe-Product': 'mweb',
            'Origin': 'https://m.cafe.naver.com',
            'Connection': 'keep-alive',
            'Cookie': None,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers',
            'Content-Type': 'text/plain'
        }

    def time_encode(self, timestamp):
        return datetime.fromtimestamp(int(timestamp / 1000)).strftime("%Y-%m-%d %H:%M")

    def save(self, data):
        pickle.dump(data, open('article.pv', 'wb'), pickle.HIGHEST_PROTOCOL)

    def load(self):
        return pickle.load(open(f'article.pv', 'rb'))

    def run(self, cookie):
        id_data = []
        try:
            data = self.load()
            for i in data:
                id_data.append(i['id'])
        except:
            data = []
        self.header['Cookie'] = cookie
        sys.stdout.write(f"\r감시 진행중 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 종료를 원하는 경우 Ctrl+C")
        sys.stdout.flush()
        first = True
        while True:
            req = requests.get(self.url, headers=self.header)
            if req.json()["message"]["status"] != "200":
                sys.stdout.write(f"\r문제 발생\n")
                sys.stdout.flush()

            Activities = req.json()["message"]["result"]["myNewsActivities"]["messages"]

            if first:
                for Act in Activities:
                    id_data.append(Act["messageKey"])
                    first = False

            if Activities[0]['messageKey'] in id_data:
                time.sleep(0.3)
                sys.stdout.write(f"\r감시 진행중 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 종료를 원하는 경우 Ctrl+C")
                sys.stdout.flush()
                continue

            Activities.reverse()
            for Act in Activities:
                if Act["messageKey"] in id_data:
                    continue
                if Act["category"] == "COMMENT":
                    Act_data = {
                        "id": Act["messageKey"],
                        "category": "댓글",
                        "nickname": Act["view"]["nickname"],
                        "mobileCafeName": Act["view"]["mobileCafeName"],
                        "content": Act["view"]["content"],
                        "timestamp": self.time_encode(Act["timestamp"]),
                        "url": f"https://cafe.naver.com/ArticleRead.nhn?clubid={Act['direction']['cafeId']}&articleid={Act['direction']['articleId']}&commentFocus=true"
                    }
                elif Act["category"] == "REPLY_OF_COMMNET":
                    Act_data = {
                        "id": Act["messageKey"],
                        "category": "답글",
                        "nickname": Act["view"]["nickname"],
                        "mobileCafeName": Act["view"]["mobileCafeName"],
                        "content": Act["view"]["content"],
                        "timestamp": self.time_encode(Act["timestamp"]),
                        "url": f"https://cafe.naver.com/ArticleRead.nhn?clubid={Act['direction']['cafeId']}&articleid={Act['direction']['articleId']}&commentFocus=true"
                    }
                elif Act["category"] == "CAFE_ARTICLE_LIKE":
                    Act_data = {
                        "id": Act["messageKey"],
                        "category": "게시글 좋아요",
                        "nickname": Act["view"]["nickname"],
                        "mobileCafeName": Act["view"]["mobileCafeName"],
                        "content": Act["view"]["content"],
                        "timestamp": self.time_encode(Act["timestamp"]),
                        "url": f"https://cafe.naver.com/ArticleRead.nhn?clubid={Act['direction']['cafeId']}&articleid={Act['direction']['articleId']}&commentFocus=true"
                    }
                else:
                    continue
                id_data.append(Act_data['id'])
                sys.stdout.write(f"\r새로운 알림 - [Type:{Act_data['category']}] [NickName:{Act_data['nickname']}] [Content:{Act_data['content']}] URL:{Act_data['url']}\n")
                sys.stdout.flush()
                data.append(Act_data)
                self.save(data)
            time.sleep(0.3)
            sys.stdout.write(f"\r감시 진행중 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 종료를 원하는 경우 Ctrl+C")
            sys.stdout.flush()
