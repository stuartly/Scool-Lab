from selenium import webdriver
from time import sleep
import re
import csv
import sys
from builtins import str

output_file = sys.argv[1]

def open_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(1)
    #选择年份索引页面
    year_lis = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@class='page-list']/a")
    #判断是否多页
    if year_lis:
        for j in range(len(year_lis)-2):
            #选择年份
            year = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl/dt")
            sleep(0.5)
            for n in range(len(year)):
                driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl/dt")[n].click()
                sleep(0.5)
                #选取期号
                #period = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl[@id='2020_Year_Issue']/dd/a")
                a = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl/dt")[n].text
                xpath_url = "/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl[@id='" + a + "_Year_Issue']/dd/a"
                period = driver.find_elements_by_xpath(xpath_url)
                sleep(0.5)
                for m in range(len(period)):
                    driver.find_elements_by_xpath(xpath_url)[m].click()
                    sleep(1)
                    titles = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl/dd/span/a")
                    #选择作者
                    #authors = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl[@id='CataLogContent']/dd/span[@class='author']")
                    #选择页码
                    #pages = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl[@id='CataLogContent']/dd/span[@class='company']")
                    for i in range(len(titles)):
                        #titles = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl/dd/span/a")
                        title = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl/dd/span/a")[i].text
                        #pages = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl[@id='CataLogContent']/dd/span[@class='company']")[i].text
                        #点击进入每个期刊的子界面
                        driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl[@id='CataLogContent']/dd/span[@class='name']/a")[i].click()
                        driver.switch_to.window(driver.window_handles[1])
                        sleep(1.5)
                        url_str = driver.current_url
                        obj = re.match(r'(.*)filename=(.*?)&dbname.*', url_str)
                        filename = obj.group(2)
                        #作者
                        try:
                            author_list = driver.find_elements_by_xpath(
                                "/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='brief']/div[@class='wx-tit']/h3[@id='authorpart']/span/a")
                            author_list_total = []
                            for g in range(len(author_list)):
                                g = g + 1
                                url_1 = "/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='brief']/div[@class='wx-tit']/h3[@id='authorpart']/span" + "[" + repr(
                                    g) + "]" + "/a"
                                a = driver.find_element_by_xpath(url_1).get_attribute("onclick")
                                a = repr(a)
                                obj = re.search(r'\d{8}', a)
                                author_1 = author_list[g - 1].text
                                author_list_total.append(author_1 + ":" + obj.group() )
                            str = '|'
                            authors = str.join(author_list_total)
                        except Exception as e:
                            authors = ' '
                        #页码
                        try:
                            basic_info = driver.find_element_by_xpath("/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@id='DownLoadParts']/div[@class='operate-left']/div[@class='opts-down']/div[@class='fl info']").text
                            pattern = re.compile(r'\n页数：(\d*)\n')
                            page = pattern.findall(basic_info)
                            page = page[0]
                        except Exception as e:
                            page = ' '
                        try:
                            keywords = driver.find_element_by_xpath("/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='row'][2]/p[@class='keywords']").text
                        except Exception as e:
                            keywords = ' '
                        try:
                            abstract = driver.find_element_by_xpath("/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='row'][1]/span[@id='ChDivSummary']").text
                        except Exception as e:
                            abstract = ' '
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        with open(output_file,'a',newline='',encoding='utf-8') as csv_out_file:
                            filewriter = csv.writer(csv_out_file)
                            filewriter.writerow([title,authors,page,keywords,abstract,filename])
            driver.find_element_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@class='page-list']/a[@class='next']").click()
    else:
        # 选择年份
        year = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl/dt")
        sleep(1)
        #17
        for n in range(8,9):
            driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl/dt")[n].click()
            sleep(0.5)
            # 选取期号
            a = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl/dt")[n].text
            xpath_url = "/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='leftYearTree']/div[@class='lArea']/div[@id='YearIssueTree']/div[@id='page1']/div[@id='yearissue+0']/dl[@id='" + a + "_Year_Issue']/dd/a"
            period = driver.find_elements_by_xpath(xpath_url)
            sleep(0.5)
            for m in range(10,len(period)):
                driver.find_elements_by_xpath(xpath_url)[m].click()
                sleep(1)
                titles = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl/dd/span/a")
                for i in range(len(titles)):
                    #titles = driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl/dd/span/a")
                    title = titles[i].text
                    driver.find_elements_by_xpath("/html/body/div[@id='qk']/div[@class='bodymain']/div[@id='contentPanel']/div[@id='rightCatalog']/div[@id='originalCatalogview']/div[@id='rightCataloglist']/dl[@id='CataLogContent']/dd/span[@class='name']/a")[i].click()
                    driver.switch_to.window(driver.window_handles[1])
                    sleep(1)
                    url_str = driver.current_url
                    obj = re.match(r'(.*)filename=(.*?)&dbname.*', url_str)
                    filename = obj.group(2)
                    try:
                        author_list = driver.find_elements_by_xpath("/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='brief']/div[@class='wx-tit']/h3[@id='authorpart']/span/a")
                        author_list_total = []
                        for g in range(len(author_list)):
                            g = g + 1
                            url_1 = "/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='brief']/div[@class='wx-tit']/h3[@id='authorpart']/span" + "[" + repr(g) + "]" + "/a"
                            a = driver.find_element_by_xpath(url_1).get_attribute("onclick")
                            a = repr(a)
                            obj = re.search(r'\d{8}', a)
                            author_1 = author_list[g - 1].text
                            author_list_total.append(author_1 + ":" + obj.group())
                        str = '|'
                        authors = str.join(author_list_total)
                    except Exception as e:
                        authors = ' '
                    try:
                        basic_info = driver.find_element_by_xpath(
                            "/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@id='DownLoadParts']/div[@class='operate-left']/div[@class='opts-down']/div[@class='fl info']").text
                        pattern = re.compile(r'\n页数：(\d*)\n')
                        page = pattern.findall(basic_info)
                        page = page[0]
                    except Exception as e:
                        page = ' '
                    try:
                        abstract = driver.find_element_by_xpath(
                            "/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='row'][1]/span[@id='ChDivSummary']").text
                    except Exception as e:
                        abstract = ' '
                    try:
                        keywords = driver.find_element_by_xpath(
                            "/html/body/div[@class='wrapper']/div[@class='main']/div[@class='container']/div[@class='doc']/div[@class='doc-top']/div[@class='row'][2]/p[@class='keywords']").text
                    except Exception as e:
                        keywords = ' '
                    driver.close()
                    sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    with open(output_file, 'a', newline='',encoding='utf-8') as csv_out_file:
                        filewriter = csv.writer(csv_out_file)
                        filewriter.writerow([title,authors,page,keywords,abstract,filename])
                    #print(journal+'  '+year_col+'  '+title + '  ' + authors + '  ' + industry + '  ' + page + '  ' + abstract + '  ' + keywords+'  '+filename)
    return
def main():
    print("请输入期刊cnki中对应的url：")
    url = input()
    open_url(url)
    return
if __name__ == '__main__':
    main()