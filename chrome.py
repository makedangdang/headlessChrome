import bs4
import urllib3
import requests
import lxml
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
urllib3.disable_warnings()

'''
无头浏览器demo
by mkdd@kpy
'''

class AutoHack(object):

    def __init__(self):
        self.opt = Options()
        self.opt.add_argument('lang=zh_CN.UTF-8')
        self.opt.add_argument('--no-sandbox')
        self.opt.add_argument('--headless')
        # 可以代理到burp
        # self.opt.add_argument('--proxy-server=127.0.0.1:8080')
        self.driver = webdriver.Chrome(options=self.opt)
        
    def set_cookie(self,cookies):
        self.driver.delete_cookie(cookies['name'])
        self.driver.add_cookie(cookies)
    
    def get_url_and_source(self,url):
        self.driver.get(url)
        return (self.driver.current_url,self.driver.page_source)
    
    # 关掉chrome,回收内存
    def close_them(self):
        self.driver.close()
        self.driver.quit()
        
    def get_info_from_source(self,url_and_source):
        url=url_and_source[0]
        source=url_and_source[1]
        def print_info(url):
            if (not url.startswith("j")):
                print(url)
        def request_url(url):
            if (not url.startswith("j")):
                self.get_url_and_source(url)
        soup=bs4.BeautifulSoup(source,'lxml')
        soup_a_href=soup.find_all('a')
        soup_script_src=soup.find_all('script')
        soup_img_src=soup.find_all('img')
        soup_link_rel=soup.find_all('link')
        soup_form_action=soup.find_all('form')
        soup_iframe_src=soup.find_all('iframe')
        [print_info(parse.urljoin(url,a.get('href'))) for a in soup_a_href]
        [request_url(parse.urljoin(url,a.get('href'))) for a in soup_a_href]
        [print_info(parse.urljoin(url,script.get('src'))) for script in soup_script_src]
        [print_info(parse.urljoin(url,img.get('src'))) for img in soup_img_src]
        [print_info(parse.urljoin(url,link.get('href'))) for link in soup_link_rel]
        [print_info(parse.urljoin(url,form.get('action'))) for form in soup_form_action]
        [print_info(parse.urljoin(url,iframe.get('src'))) for iframe in soup_iframe_src]


cookies={
            'domain': '.suning.com', 
            'path': '/', 
            'name': 'authId',
            'value': 'xxx'
        }




x=AutoHack()
x.get_url_and_source("https://www.suning.com/")
x.set_cookie(cookies)
x.close_them()
