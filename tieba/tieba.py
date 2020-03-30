import time
import re
from urllib import request
from urllib import parse
from lxml import etree


class BaidutiebaSpider:
    """贴吧信息"""
    def __init__(self, headers, keyword, baseurl="http://tieba.baidu.com/"):
        self.headers = headers
        self.keyword = keyword
        self.baseurl = baseurl

    def get_page(self, url):
        """获取html页面"""
        req = request.Request(url=url, headers=self.headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        print("start-url---{}".format(res.geturl()))

        return html

    def parse_url_list(self):
        """获取每个帖子url"""
        url = self.baseurl + 'f?' + 'kw=' + parse.quote(self.keyword) + '&ie=utf-8&pn=0'
        html = self.get_page(url)
        p = re.compile(r'/p/\d*')
        url_list = p.findall(html)
        urls = []
        for i in url_list:
            url = self.baseurl + i
            urls.append(url)
        return urls

    def run_parse(self):
        """获取每个帖子的内容"""
        urls = self.parse_url_list()
        messages = []
        # body_list = []
        images = []
        for url in urls:
            time.sleep(0.5)
            html = self.get_page(url)
            parse_html = etree.HTML(html)
            title = parse_html.xpath('//div/h1/text()')[0]
            # author = parse_html.xpath('//li[@class="d_name"]/a[ @class="p_author_name j_user_card"]/text()')[0]
            # print(author)
            # body = parse_html.xpath('//cc/div[@class="d_post_content j_d_post_content clearfix"]/text()')[0]
            # print(body)
            image_links = parse_html.xpath('//div//img[@class="BDE_Image"]/@src')
            # for i in range(len(title)):
            #     body_list.append({"author": author[i], "body": body[i]})
            # messages.append({"title": title, "body": body_list})
            for img in image_links:
                images.append(img)
            messages.append({'title': title, 'url': url})
        try:
            self.save_image(images)
        except Exception as e:
            print("图片存储出错--{}".format(e))
        self.save(messages)

    @staticmethod
    def save_image(images):
        i = 0
        for img in images:
            i += 1
            image = request.urlopen(img).read()
            print("正在获取第{}张图".format(i))
            with open("./图片/{}.jpg".format(str(i)), "wb") as f:
                f.write(image)
                f.close()

    def save(self, messages):
        print("正在保存内容")
        message = str(messages)
        with open('{}.txt'.format(self.keyword), 'w', encoding='gb18030') as f:
            f.write(message)
            f.close()


if __name__ == "__main__":
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    word = input("请输入要查询的贴吧:")
    tb = BaidutiebaSpider(header, word)
    tb.run_parse()
