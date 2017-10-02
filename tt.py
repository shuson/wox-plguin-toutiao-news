# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser
import json

import requests
from wox import Wox,WoxAPI

URL = 'http://www.toutiao.com/api/pc/feed/?category='
LINK = 'http://www.toutiao.com'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):
  
    def request(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
	#get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
	    proxies = {
		"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
		"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
	    }
	    return requests.get(url,proxies = proxies, headers=headers)
	return requests.get(url, headers=headers)
			
    def query(self, param):
        if param.strip() == 'kj':
            r = self.request(URL + 'news_tech')
        elif param.strip() == 'ty':
            r = self.request(URL + 'news_sports')
        else:
            r = self.request(URL + 'news_hot')
	
	
	feed = json.loads(r.content)
        news = feed['data']
        
	result = []
	for x in range(len(news)):
            post = {
                    'Title': news[x]['title'],
                    'SubTitle': news[x]['abstract'],
                    'IcoPath': os.path.join('img', 'tt.png'),
                    'JsonRPCAction': {
                        'method': 'open_url',
                        'parameters': [LINK+news[x]['source_url']]
                    }
                }
            result.append(post)
        if not result:
            result.append({
                    'Title': 'No News Now'
                })
        
	return result
    
    def open_url(self, url):
	webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

if __name__ == '__main__':
    Main()
