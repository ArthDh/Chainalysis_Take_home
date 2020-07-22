import praw
import requests as req
import bs4 as bs


def get_subreddit(subs=["UpliftingNews"], lim=10):
    reddit = praw.Reddit(client_id="tgnInGucwBQiKg",
                         client_secret="LAZuGSps7eG3AMSa3BE2-CkqzWI",
                         user_agent="Agent Pupper")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    d = dict()
    json_dump = []
    for sub in subs:
        for submission in reddit.subreddit(sub).hot(limit=lim):
            d['title'] = submission.title
            d['url'] = submission.url
            source = req.get(submission.url, headers=headers)
            soup = bs.BeautifulSoup(source.text, 'lxml')
            if soup.find("meta", property="og:image"):
                d['img_url'] = soup.find("meta", property="og:image")['content']
            else:
                d['img_url'] = None
            if soup.find("meta", property="article:tag"):
                d['tags'] = soup.find("meta", property="article:tag")['content']
            else:
                d['tags'] = None
            json_dump.append(d)
            d = dict()
    return json_dump


def get_site_data(url="goodnewsnetwork", lim=10):
    if "goodnewsnetwork" in url:
        url = "https://www.goodnewsnetwork.org/"
    else:
        url = "https://www.positive.news/articles/"
    source = req.get(url)
    soup = bs.BeautifulSoup(source.text, 'lxml')
    d = dict()
    json_dump = []
    if "goodnewsnetwork" in url:
        for div in soup.find_all('div', {'class': 'td-module-thumb'})[:lim]:
            d['title'] = div.a['title']
            d['url'] = div.a['href']
            d['img_url'] = div.img['src']
            d['tags'] = div.parent.find_all('a', {'class': 'td-post-category'})[0].text
            json_dump.append(d)
            d = dict()

    elif "positive.news":
        for div in soup.find_all('div', {'class': 'column card '})[:lim]:
            d['title'] = div.div.a.text
            d['url'] = div.a['href']
            d['img_url'] = div.a.img['src']
            d['tags'] = ",".join([tag.text for tag in div.div.find_all('a', {'class': 'card__category'})])
            json_dump.append(d)
            d = dict()

    return json_dump


if __name__ == '__main__':
    json_dump = get_site_data(lim=2)
    for d in json_dump:
        print(d)
        print("*" * 20)
    # json_dump = get_subreddit(lim=5)
    # # print(json_dump)
    # for d in json_dump:
    #     print(d)
    #     print("*" * 20)
