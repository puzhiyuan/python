"""爬取建立模板
1.requests传参一定要注意不能传入列表给url
2，文件也是以二进制形式（.content）
3.模板存在付费模板，所以获取到的 href 值有出现为空的现象，直接使用会出现报错。可以通过 if 进行判断，舍去为空的值
"""


import requests
from lxml import etree
import os.path
if not os.path.exists('./模板'):
    os.mkdir('./模板')
url = 'https://sc.chinaz.com/jianli/index.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
response = requests.get(url=url, headers=headers).text
tree = etree.HTML(response)
href_list = tree.xpath('//div[@id="main"]/div/div/p//a/@href')
for href in href_list:
    #print(href)
    new_url = 'https:' + href
    #print(new_url)
    page_text = requests.get(url=new_url, headers=headers).text
    new_tree = etree.HTML(page_text)
    download_url = new_tree.xpath('//div[@class="clearfix mt20 downlist"]/ul/li[1]/a/@href')
    #print(download_url)
    if download_url:
        real_url = download_url[0]
        #print(real_url)
        data = requests.get(url=real_url,headers=headers).content
        name = real_url.split('/')[-1]
        #print(name)
        file_path = './模板/' + name
        with open(file_path, 'wb') as fp:
            fp.write(data)
        print(name + '下载完成！！！')