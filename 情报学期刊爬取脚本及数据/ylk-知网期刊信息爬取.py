import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import time
import csv
#coding: UTF-8
Jname = 'QBXB'



def main():
    baseurl = 'https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=QBXB8S1.002'  #这里也要记得改
    # baseurl = 'https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=QBXB199904002'
    # URLs = getURLs(baseurl)
    URLs = getSpecURLs(baseurl)  #更改调用函数
    getData(URLs)

def getURLs(baseurl):
    filename =''
    URLs = []
    for year in range (1982,2021):
        if year <1999 and year>=1994:
            continue
        elif year >=2003 and year<=2012:
            continue
        for month in range(1,13):
            GroupURL = []
            for num in range(1,31):
                if month>=10 and num>=10:
                    filename = Jname+ str(year) + str(month) + '0' +str(num)
                elif month>=10 and num<10:
                    filename = Jname +str(year) +str(month) +'00'+str(num)
                elif month <10 and num>=10:
                    filename = Jname +str(year)+'0'+str(month)+'0'+str(num)
                else:
                    filename = Jname +str(year)+'0'+str(month)+'00'+str(num)
                GroupURL.append(baseurl.replace(baseurl[66:79],filename))
    # print(URLs)
            URLs.append(GroupURL)
    return URLs

def getSpecURLs(baseurl):
    URLs = []
    filename = ''
    mons =['01','02','03','04','05','06','S1','S2']
    years = ['4','5','6','7','8','9']
    for year in years:
        for month in mons:
            GroupURL = []
            for num in range(1,100):
                if num<10:
                    filename = Jname + year + month +'.00'+ str(num)
                else:
                    filename = Jname +year +month +'.0' +str(num)
                GroupURL.append(baseurl.replace(baseurl[66:77],filename))
            URLs.append(GroupURL)
    print(len(URLs))
    return URLs


def getData(URLs):
    counter =0
    # f = open('info.csv','a',newline='',encoding='utf-8-sig') #需要追加时候在这里改
    f = open('info.csv', 'w', newline='', encoding='utf-8-sig')
    csv_writer =csv.writer(f)
    dataList =[]
    find_title = re.compile(r'<h1>(.*?)</h1>',re.S)
    find_author = re.compile(r"TurnPageToKnetV\('au','(.*?)','\d*",re.S)
    find_authorID = re.compile(r'<input class="authorcode" type="hidden" value="(.*?)">',re.S)
    find_abstract = re.compile(r'<span id="ChDivSummary" name="ChDivSummary" class="abstract-text">(.*?)</span>',re.S)
    find_keyword = re.compile(r"TurnPageToKnetV\('kw','(.*?)','",re.S)
    find_info = re.compile(r'<p class="total-inform"><span>(.*?)</span></p>',re.S)
    for i in range(0, len(URLs)):
        for j in range(0, len(URLs[i])):
            data =[]
            html = str(askURL(URLs[i][j]))
            if(html =='none'):
                break
            author = re.findall(find_author,html)
            if len(author) == 0:
                continue
            title = re.findall(find_title,html)
            authorID = re.findall(find_authorID,html)
            abstract = re.findall(find_abstract,html)
            keyword = re.findall(find_keyword,html)
            info = re.findall(find_info,html)
            data.append(title[0])

            data.append(author)
            data.append(authorID)
            if len(abstract) == 1:
                data.append(abstract[0])
            else:
                data.append('')
            data.append(keyword)
            data.append(info)
            data.append(URLs[i][j][66:77]) #记得过一会改这里
            # data.append(URLs[i][j][66:79])
            counter = counter+1
            print(data)
            csv_writer.writerow(data)
            print(counter)
    f.close()





def askURL(url):
        head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        # 让服务器认为这是一个浏览器
        try:
            # time.sleep(0.5)
            request = urllib.request.Request(url, headers=head)  # 封装一个request，拿去一起访问
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
            htmlChecker = str(html)
            # print(html)
            if htmlChecker.find('所查找的文献不存在') >= 0:
                # print(html)
                # print(len(htmlChecker))
                # print(url)
                html = 'none'
            elif len(htmlChecker) == 54 or htmlChecker.find('对不起，服务器忙，请稍后再操作')>=0:
                print(url)
                for i in range(0, 21):
                    response = urllib.request.urlopen(request)
                    html = response.read().decode('utf-8')
                    if len(str(html)) == 54:
                        continue
                    elif str(html).find('对不起，服务器忙，请稍后再操作') >=0:
                        continue
                    elif str(html).find('所查找的文献不存在') >= 0:
                        html = 'none'
                        return html
                    else:
                        return html
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
                return 'none'
            if hasattr(e, 'reason'):
                print(e.reason)
                return 'none'
        return html



if __name__ == '__main__':
    main()