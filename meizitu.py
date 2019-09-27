import urllib.request
import urllib.parse
from lxml import etree
import os
import time

def handle_request(url,page):
    if page == 1:
        url = url
    else:
        url = url + 'page/' + str(page) + '/'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.mzitu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '__guid=218785567.2613078880721368600.1562595109187.8257; monitor_count=16; Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1564920155,1564921379,1564922209,1564922624; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1564922624',
    }
    request = urllib.request.Request(url = url , headers = headers)
    return request


def parse_content(content):
    tree = etree.HTML(content)
    image_list = tree.xpath('//li/a/img/@data-original')
    for image_src in image_list:
        download_image(image_src)


def download_image(image_src):
    dirpath = 'meizitu'
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    filename = os.path.basename(image_src)
    filepath = os.path.join(dirpath,filename)
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.mzitu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '__guid=218785567.2613078880721368600.1562595109187.8257; monitor_count=16; Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1564920155,1564921379,1564922209,1564922624; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1564922624',
        }
    request = urllib.request.Request(url = image_src , headers = headers)
    response = urllib.request.urlopen(request)
    with open(filepath,'wb')as fp:
        fp.write(response.read())

def main():
    url = 'https://www.mzitu.com/xinggan/'
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(start_page,end_page+1):
        request = handle_request(url,page)
        content = urllib.request.urlopen(request).read().decode()
        parse_content(content)
        time.sleep(2)

if __name__ == '__main__':
    main()
