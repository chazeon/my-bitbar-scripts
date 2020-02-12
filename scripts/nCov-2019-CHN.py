#!/usr/bin/env PYTHONIOENCODING=UTF-8 /Users/chazeon/.pyenv/shims/python3

# <bitbar.title>NYC nCov Report</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Chazeon Luo</bitbar.author>
# <bitbar.author.github>chazeon</bitbar.author.github>

data_url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"

import sys, re, urllib.parse, json
from pathlib import Path
import textwrap
import dateutil.parser

sys.path.append(str(Path(__file__).parent.parent / "libs"))

import bitbar

def get_info():
    import requests, bs4
    resp = requests.get(data_url)
    doc = resp.content
    soup = bs4.BeautifulSoup(doc, "html.parser")
    script = soup.find("script", id="getStatisticsService")
    res = re.search(r"try { window.getStatisticsService = (.*)}catch\(e\){}", str(script))
    return json.loads(res.group(1))

info = get_info()
cases_count = {
    "confirmed": info['confirmedCount'],
    "suspected": info['suspectedCount'],
    "serious": info['seriousCount'],
    "dead": info['deadCount'],
    "cured": info['curedCount']
}
pkg = bitbar.BitBarMessagePack(f"😷{cases_count['confirmed']}")
pkg.append("丁香园 2019 新冠统计", { "href": data_url})
pkg.append("---")
pkg.append(f"确诊: {cases_count['confirmed']:7,d}", { "font":"'SF Mono'", "size": 12, "color": "gray"})
pkg.append(f"疑似: {cases_count['suspected']:7,d}", { "font":"'SF Mono'", "size": 12, "color": "gray"})
pkg.append(f"重症: {cases_count['serious']  :7,d}", { "font":"'SF Mono'", "size": 12, "color": "red"})
pkg.append(f"死亡: {cases_count['dead']     :7,d}", { "font":"'SF Mono'", "size": 12, "color": "black"})
pkg.append(f"治愈: {cases_count['cured']    :7,d}", { "font":"'SF Mono'", "size": 12, "color": "green"})
print(str(pkg))

exit()

news = get_news()


pkg.append(f"Total {sum(cases.values())} cases", { "href": table_url})

for key, val in cases.items():
    pkg.append(f"{key}: {val}", {"color": "gray"})
pkg.append("---")
pkg.append(f"Twitter @nycHealthy", {"href": "https://twitter.com/nycHealthy"})

news_parent = bitbar.BitBarMessageParent(f"NYCHealth News", {"href": news_url})
pkg.append(news_parent)

for news_piece in news:
    title = news_piece["title"]
    title = re.sub(r"^New York City Reports", "", title)
    title = re.sub(r"New York City", "NYC", title)
    title = textwrap.shorten(title, 50, placeholder=" ...")
    
    link = urllib.parse.urljoin(news_url, news_piece["link"])
    date = news_piece["date"].strftime("%m/%d")
    
    msg = bitbar.BitBarMessage(f"({date}) {title}", {"href": link})
    news_parent.append(msg)

