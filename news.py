import re
import time
from datetime import datetime, date
import requests


class SpiderNews(object):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/91.0.4472.114 Safari/537.36",
    }

    def run(self):
        length = 100
        i = 0
        stop_date = date(2019, 1, 1)
        date_ = datetime.now().date()

        while stop_date < date_:
            time.sleep(1)
            with open("./news.txt", "a+", encoding="utf-8") as f:
                for item in self.get_news_list(i * length, length):
                    if not item:
                        continue
                    date_ = item[3]
                    f.write("{}@@{}@@{}\n".format(item[0].replace("-", " "), item[1], item[2]))
                    f.flush()
                else:
                    i += 1
            print(i)

    def get_news_list(self, offset, length):
        query = {
            "operationName": "TagPageQuery",
            "variables": {"slug": "bitcoin", "order": "postPublishedTime", "offset": offset, "length": length,
                          "short": "en",
                          "cacheTimeInMS": 300000},
            "query": """
               query TagPageQuery($short: String, $slug: String!, $order: String, $offset: Int!, $length: Int!) {
                locale(short: $short) {
                    tag(slug: $slug) {
                        cacheKey
                        id
                        slug
                        avatar
                        createdAt
                        updatedAt
                        posts(order: $order, offset: $offset, length: $length) {
                            data {
                            cacheKey
                            id
                            slug
                            views
                            postTranslate {
                                cacheKey
                                id
                                title
                                published
                                bodyText
                                __typename
                            }
                            __typename
                            }
                            postsCount
                            __typename
                        }
                    __typename
                    }
                    __typename
                }
                }
            """}

        data = self.fetch_response("https://conpletus.cointelegraph.com/v1/", query)
        if not data:
            yield None
        try:
            data = data.get("data", dict)
            data = data.get("locale", dict)
            data = data.get("tag", dict)
            data = data.get("posts", dict)
            data = data.get("data", list)
            for item in data:
                try:
                    if not isinstance(item, dict):
                        continue
                    postTranslate = item.get("postTranslate")
                    title = postTranslate.get("title")
                    published = postTranslate.get("published")
                    body = re.sub(r'\s{2,}', '', str(postTranslate.get("bodyText"))).replace("\n", "").replace("\t", "")

                    date_ = str(published).replace("T", " ")[:-6]
                    date_ = datetime.strptime(date_, "%Y-%m-%d %H:%M:%S").date()
                    base = [title, published, body, date_]
                    yield base
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            yield None

    def fetch_response(self, url, data):
        try:
            res = requests.post(url, json=data, headers=self.headers, timeout=8)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(e)
            return dict()


if __name__ == '__main__':
    SpiderNews().run()
