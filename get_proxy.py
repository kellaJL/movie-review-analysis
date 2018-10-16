import bs4
import requests
import csv
import re
import random

class GetKuaiDaiLiIp:

    def __init__(self,url='https://www.kuaidaili.com/free/inha/'):

        self.proxy_list=[]
        self.url=url+str(random.randint(1,3))+'/'
    def GetHTMLText(self,url,code='utf-8'):
        html = ''
        ua={'user-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

        r = requests.get(url,headers=ua,timeout=3)
        if 500 <= r.status_code < 600:
            return self.GetHTMLText(url)
        r.raise_for_status()
        r.encoding = code
        html = r.text
              # self.cache[url] = html
        return html
    def test_connection(self,protocol,ip,port):
        """
        检测代理的有效性
        :param protocol:
        :param ip:
        :param port:
        :return:
        """
        proxies = {protocol: ip + ":" + port}
        try:
           # OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
            MaskedIP = requests.get("http://icanhazip.com", timeout=3, proxies=proxies).content
            if MaskedIP!=None:
                return True
            else:
                return False
        except:
            return False

    def ParseAndGetInfo(self):

        html=self.GetHTMLText(self.url)
        #print(html[:200])
        count=0
        if html==None:
            return
        soup=bs4.BeautifulSoup(html,'html.parser')
        ip_info=soup.find('table',attrs={'class':'table table-bordered table-striped'})
        key_list=ip_info.find_all('th')
        value_list=ip_info.find_all('td')
        len_list=ip_info.find_all('tr')
        len_list_length=len(len_list)
        #print(len_list_length)
        key_len=len(key_list)
        #print(len(value_list))
        #proxies_pools=db.proxy
        for k in range(len_list_length-1):
           infoDict={}
           for i in range(key_len):
              key=key_list[i].text
              value=str(value_list[i+k*(key_len)].text)
              pat=re.compile(':')
              value1=pat.sub('-',value)
              #value.replace(':','-')
              #print(value)
              infoDict[key]=value1
           if infoDict['匿名度']=='高匿名':
               #is_working=p_p.test_connection(infoDict['类型'],infoDict['IP'],infoDict['PORT'])
               #if is_working:
                #   p_p.add_proxy(infoDict)
              #print('proxies:'+str(infoDict))
              one_p=str(infoDict['类型'])
              two_p=str(infoDict['IP'])
              three_p=str(infoDict['PORT'])
              #print(one_p)
              #print(type(one_p))
              flag=self.test_connection(one_p,two_p,three_p)##########################
              if flag==True:
                  self.proxy_list.append(infoDict)
              else:
                  continue
        return self.proxy_list
"""
proxy_list=[]
g=GetKuaiDaiLiIp()
proxy_list=g.ParseAndGetInfo()
print(proxy_list)
"""