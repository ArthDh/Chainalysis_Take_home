import praw
import requests as req
import bs4 as bs
from gensim.summarization.summarizer import summarize


def get_soup_text(soup=None):
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text


def summarize_soup(soup, wc=60):
    url_text = get_soup_text(soup).replace(u"Â", u"").replace(u"â", u"")
    final_summary = ""
    if len(url_text) > wc:
        final_summary = summarize(url_text, word_count=wc)
        final_summary = final_summary.replace("\n", "")
    return final_summary


def get_url_json(url=""):
    source = req.get(url)
    soup = bs.BeautifulSoup(source.text, 'lxml')
    d = dict()
    if soup.find("meta", property="og:image"):
        d['img_url'] = soup.find("meta", property="og:image")['content']
    else:
        d['img_url'] = None
    if soup.find("meta", property="article:tag"):
        d['tags'] = soup.find("meta", property="article:tag")['content']
    else:
        d['tags'] = None
    if soup.find("meta", property="og:title"):
        d['title'] = soup.find("meta", property="og:title")['content']
    else:
        d['title'] = None
    d['summary'] = summarize_soup(soup, wc=100)
    d['url'] = url

    return d


def get_subreddit(subs=["UpliftingNews"], lim=10):
    reddit = praw.Reddit(client_id="tgnInGucwBQiKg",
                         client_secret="LAZuGSps7eG3AMSa3BE2-CkqzWI",
                         user_agent="Agent Pupper")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    d = dict()
    json_dump = []
    for sub in subs:
        for submission in reddit.subreddit(sub).hot(limit=lim):
            d = get_url_json(submission.url)
            json_dump.append(d)
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
            d = get_url_json(div.a['href'])
            d['tags'] = div.parent.find_all('a', {'class': 'td-post-category'})[0].text
            json_dump.append(d)

    elif "positive.news":
        for div in soup.find_all('div', {'class': 'column card '})[:lim]:
            d = get_url_json(div.a['href'])
            d['tags'] = ",".join([tag.text for tag in div.div.find_all('a', {'class': 'card__category'})])
            json_dump.append(d)

    return json_dump


if __name__ == '__main__':
    json_dump = get_site_data(url="positive.news",lim=5)

    for d in json_dump:
        print(d)
        print("*" * 20)
    # json_dump = get_subreddit(lim=15)
    # # print(json_dump)
    # for d in json_dump:
    #     print(d)
    #     print("*" * 20)
