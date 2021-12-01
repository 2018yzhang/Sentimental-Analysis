import requests
import time


class SpiderKLine(object):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/91.0.4472.114 Safari/537.36",
    }

    def run(self):

        stop = int(time.time())

        start = 1514736000

        while start < stop:
            time.sleep(1)
            with open("k_line.txt", "a+", encoding="utf-8") as f:
                for item in self.get_kline(start, start + 24 * 60 * 60):
                    if not item:
                        continue
                    f.write("{},{}\n".format(item[0], item[1]))
                    f.flush()
                else:
                    start += 24 * 60 * 60
                print(start)

    def get_kline(self, start, end):
        url = "https://www.bitmex.com/api/udf/history?symbol=XBTUSD&resolution=1&from={}&to={}".format(start, end)

        data = self.fetch_response(url)

        if not data:
            return None
        t = data.get("t", list)
        c = data.get("c", list)
        if not t or not c:
            return
        if len(t) == len(c):
            le = len(t)
            for i in range(le):
                yield t[i], c[i]
        else:
            return

    def fetch_response(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(e)
            return dict()


if __name__ == '__main__':
    SpiderKLine().run()
