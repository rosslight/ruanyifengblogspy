#coding='utf-8'
import urllib2
import pdfkit
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def download (url,numretries=5) :
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}
    request = urllib2.Request(url ,headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        html = None
        if numretries >0:
            if hasattr(e,'code') and 500<= e.code<=600:
                return download(url,numretries-1)
    return html
    
def get_url_list(url):
    response = download(url)
    soup = BeautifulSoup(response, "lxml")
    menu_tag = soup.find_all(class_="module-content")[0]
    urls = []
    for li in menu_tag.find_all("li"):
        url = li.a.get("href")
        urls.append(url)
    return urls
    
def parse_url_to_html(url,name='1.html'):
    response = download(url)
    soup = BeautifulSoup(response, "lxml")
    body = soup.find_all(class_="asset-content entry-content")[0]
    title = soup.find('h1').get_text()
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag('h1')
    title_tag.string = title
    center_tag.insert(1, title_tag)
    body.insert(1, center_tag)

    html =str(body)
    with open(name, 'wb') as f:
        f.write(html)

def save_pdf(url):
    urls = get_url_list(url)
    htmls=[]
    print '下载ing'
    for x in urls:
        name = str(urls.index(x))+'.html'
        parse_url_to_html(x,name)
        htmls.append(name)
    
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
    print '下载结束'
    pdfkit.from_file(htmls, 'first.pdf', options=options)

        
if __name__ == '__main__':
     save_pdf('http://www.ruanyifeng.com/blog/computer/')
     
    
    