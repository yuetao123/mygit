import requests
from lxml import etree
import pymongo
from 项目.ip代理.config import *
import time

#需配置mongodb
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def handle_request(url,page):
    url = url + str(page)
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    }
    response = requests.get(url = url ,headers = headers)
    response.encoding = 'utf-8'
    return response

def parse_response(response):
    tree = etree.HTML(response.text)
    #获取HTTP或HTTPS
    http_list = tree.xpath('//table[@id="ip_list"]/tr/td[6]/text()')
    #获取IP
    ip_list = tree.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
    #获取端口
    port_list = tree.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
    for proxy_pool in range(0,100):   #每一页都有100个
        if http_list[proxy_pool] == 'HTTP':
            # 例如：http://120.83.104.18:9999
            http_Proxy_Server = 'http://' + ip_list[proxy_pool] + ':' + port_list[proxy_pool]
            proxies = {'http': http_Proxy_Server}
            #判断代理ip是否可用
            try:
                requests.get('http://www.baidu.com', proxies=proxies, timeout=3).status_code != 200
            except:
                print('HTTP代理连接失败')
            else:
                print('HTTP代理连接成功')
                product = {
                    'HTTP': http_list[proxy_pool],
                    'IP': ip_list[proxy_pool],
                    '端口': port_list[proxy_pool],
                }
                #把可用的存储至mongodb
                save_to_mongo(product)
        else:
            https_Proxy_Server = 'https://' + ip_list[proxy_pool] + ':' + port_list[proxy_pool]
            proxies = {'https': https_Proxy_Server}
            try:
                requests.get('http://www.baidu.com', proxies=proxies, timeout=3).status_code != 200
            except:
                print('HTTPS代理连接失败')
            else:
                print('HTTPS代理连接成功')
                product = {
                    'HTTP': http_list[proxy_pool],
                    'IP': ip_list[proxy_pool],
                    '端口': port_list[proxy_pool],
                }
                save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败', result)

def main():
    url = 'https://www.xicidaili.com/nn/'
    statr_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(statr_page,end_page+1):
        response = handle_request(url,page)
        parse_response(response)
        time.sleep(2)

if __name__ == '__main__':
    main()
