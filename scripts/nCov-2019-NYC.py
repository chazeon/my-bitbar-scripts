#!/usr/bin/env PYTHONIOENCODING=UTF-8 /Users/chazeon/.pyenv/shims/python3

# <bitbar.title>NYC nCov Report</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Chazeon Luo</bitbar.author>
# <bitbar.author.github>chazeon</bitbar.author.github>

table_url = "https://www1.nyc.gov/site/doh/health/health-topics/coronavirus.page"
news_url = "https://www1.nyc.gov/site/doh/about/press/recent-press-releases.page"

import sys, re, urllib.parse
from pathlib import Path
import textwrap
import dateutil.parser

sys.path.append(str(Path(__file__).parent.parent / "libs"))

import bitbar

def get_cases():
    import requests, bs4
    resp = requests.get(table_url)
    doc = resp.text
    soup = bs4.BeautifulSoup(doc, "html.parser")
    def parse_soup():
        tables = soup.find_all("table")
        if len(tables) > 0:
            table = tables[0]
            for row in table.find_all("tr")[1:-1]:
                yield (row.find("th").string, sum([int(td.string) for td in row.find_all("td")]))
    return dict(parse_soup())

def get_news():
    import requests, bs4
    resp = requests.get(news_url)
    doc = resp.text
    soup = bs4.BeautifulSoup(doc, "html.parser")
    def parse_soup():
        content = soup.find(attrs={"class": "about-description"})
        for para in content.find_all("p"):
            date = dateutil.parser.parse(para.find("strong").string)
            link = para.find("a")
            yield {"title": link.string, "link": link.attrs["href"], "date": date}
    return list(parse_soup())

cases = get_cases()
news = get_news()

pkg = bitbar.BitBarMessagePack(f"🦠 {cases['Positive']}/{cases['Pending']}")

pkg.append("NYCHealth 2019-nCov", { "href": table_url})
pkg.append("---")
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

print(str(pkg))
