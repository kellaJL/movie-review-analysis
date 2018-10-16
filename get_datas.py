import requests
from bs4 import BeautifulSoup
import time
import random
import json
import get_proxy

def get_movie_code(movie_name):
    if(movie_name==""):
        return
    url='http://maoyan.com/query?kw='+str(movie_name)
    proxy_pool=get_proxy.GetKuaiDaiLiIp()
    random.seed(0)
    proxy_pools=proxy_pool.ParseAndGetInfo()
    proxies=random.choice(proxy_pools)

    proxy_ip = {str(proxies['类型']):str(proxies['IP']) + ":" + str(proxies['PORT'])}
    print(proxy_ip)
    ua = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    responses=requests.get(url=url,headers=ua,proxies=proxy_ip)
    print("请求代码:%d"%responses.status_code)
   
    html=BeautifulSoup(responses.text,"html.parser")
    #print(html)
    code=html.find('a',{'data-act':'movies-click','target':"_blank"})
    #print(code)
    code=(code.attrs)['href'][9:-2]
    
    return code
# 获取每一页数据
def get_one_page(url):

    proxy_pool=get_proxy.GetKuaiDaiLiIp()
    random.seed(0)
    proxy_pools=proxy_pool.ParseAndGetInfo()
    proxies=random.choice(proxy_pools)

    proxy_ip = {str(proxies['类型']):str(proxies['IP']) + ":" + str(proxies['PORT'])}
    print(proxy_ip)
    ua = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    responses=requests.get(url=url,headers=ua,proxies=proxy_ip)
    if responses.status_code==200:
       return responses.text
    return None
# 解析每一页数据


def parse_one_page(html):

    data = json.loads(html)['cmts']  # 获取评论内容
    for item in data:
        yield{
            'date': item['time'].split(' ')[0],
            'nickname': item['nickName'],
            'city': item['cityName'],
            'rate': item['score'],
            'conment': item['content']
        }

# 保存到文本文档中


def save_to_txt(movie_name):
    #movie=get_movie_code(movie_name)
    
    for i in range(500, 1001,10):
        try:
           print("开始保存第%d页" % i)
           url = 'http://m.maoyan.com/mmdb/comments/movie/1203084.json?_v_=yes&offset=' + \
                 str(i)

           html = get_one_page(url)

           for item in parse_one_page(html): 
              print(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ','+ str(item['rate']) + ',' + item['conment'] + '\n')
              try:
                with open('movie_reviews2.txt', 'a', encoding='utf-8') as f:
                       f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ','
                        + str(item['rate']) + ',' + item['conment'] + '\n')
                # time.sleep(random.randint(1,100)/20)
                #time.sleep(2)
              except Exception as e:
                f.close()
                continue
           #time.sleep(3)
        except Exception as e:
            continue

        f.close()
# 去重重复的评论内容


def delete_repeat(old, new):
    oldfile = open(old, 'r', encoding='utf-8')
    newfile = open(new, 'w', encoding='utf-8')
    content_list = oldfile.readlines()  # 获取所有评论数据集
    content_alread = []  # 存储去重后的评论数据集

    for line in content_list:
        if line not in content_alread:
            newfile.write(line + '\n')
            content_alread.append(line)

if __name__ == '__main__':
    movie_name=""
    save_to_txt(movie_name)
    delete_repeat(r'movie_reviews2.txt', r'movie_new.txt')
    
    
    #get_movie_code(movie_name)

