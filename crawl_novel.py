import re
import requests
import os
from datetime import datetime


def date_time_str(date_time):
    date_time_format = '%y-%M-%d %H:%M:%S'
    return datetime.strftime(date_time, date_time_format)


class CrawlNovel:
    def __init__(self, url):
        self.url = url

    def query(self, url):
        print("...Loading webpage %s source code..." % url)
        return requests.get(url)

    def extract_chapter_info(self, url):
        """
        extract the information of the novel and its chapters into a dictionary
        :param url:url of the target website
        :return: a list of hyper-links and names of each chapter
        """
        home_page = self.query(url)
        print("...Finished loading...")
        home_page_content = home_page.content
        home_page_str = home_page_content.decode('gbk')
        title = re.findall("title>(.*?)\(动物农场", home_page_str)
        print("title:", title)
        abstract = re.findall("<td class=\"p10-24\"><strong>内容简介：</strong><br />　　(.*?)</td", home_page_str)[0]
        print("abstract:", abstract)
        chapter_blocks = re.findall("strong>正文</strong></td>(.*?)</tbody", home_page_str, re.S)
        chapters = re.findall("href=\"(.*?)</a", chapter_blocks[0])
        print("There are %d chapters" % (len(chapters)))
        chapter_list = {}
        for each in chapters:
            link, name = each.split("\">")
            link = url + "/" + link
            chapter_list[name] = link
            print(name + ':'+link)
        return chapter_list

    def crawl_chapter_content(self, chapter_list):
        """
        get every link of every chapter and crawl its content into a .txt file
        :param chapter_list: a dictionary contains chapters' name and their hyperlink
        :return:
        """
        for key, value in chapter_list.items():
            chapter_name = key
            chatper_content = self.query(value).content.decode('gbk')
            print(f"{chapter_name} length:{len(chatper_content)}")
            content = re.findall("p>(.*?)</p", chatper_content, re.S)
            article = content[0].replace("<br />", "\n")
            self.save(chapter_name, article)

    def save(self, chapter_name, article):
        os.makedirs('动物农场', exist_ok=True)
        with open(os.path.join('动物农场', chapter_name + '.txt'), 'w') as f:
            f.write(article)

    def exe(self):
        chapter_lists = self.extract_chapter_info(self.url)
        crawl_chapters_start = datetime.now()
        print(f"-----------crawl_chapters_start start from {date_time_str(start)}")
        self.crawl_chapter_content(chapter_lists)
        end = datetime.now()
        print(f"------------End at {date_time_str(end)}")
        print(f"------------Crawl chapters runtime: {end - crawl_chapters_start}")
        print(f"------------Total runtime: {end - start}")


if __name__ == '__main__':
    start = datetime.now()
    print(f"-----------Start from {date_time_str(start)}")
    cn = CrawlNovel("http://www.kanunu8.com/book3/6879")
    cn.exe()
