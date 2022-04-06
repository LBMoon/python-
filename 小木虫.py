import requests
from lxml import etree
import xlsxwriter as xw

class Get_page:
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }
    def __init__(self,url):
        self.url = url

    def get_page(self):
        self.response = requests.get(self.url,headers=Get_page.headers).text
        return self.response

def parseSchool(url):
    res = Get_page(url).get_page()
    tree = etree.HTML(res)
    titles = tree.xpath('//div[@class = "forum_body xmc_line_lr"]/table//tbody/tr/th[@class="thread-name"]/a/text()')
    school_hrefs = tree.xpath('//div[@class = "forum_body xmc_line_lr"]/table//tbody/tr/th[@class="thread-name"]/a/@href')
    school_urls = ["http://muchong.com" + href for href in school_hrefs]
    return school_urls,titles

def parseSchoolInfo(school_url):
    res = Get_page(school_url).get_page()
    tree = etree.HTML(res)
    infos = {}
    infos["学校"] = ' '.join(tree.xpath('//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tr[2]/td[2]/text()')).replace('\r\n','')
    infos["专业"] = ' '.join(tree.xpath('//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tr[3]/td[2]/text()')).replace(' ','').replace('\r\n','')
    infos["年级"] = ' '.join(tree.xpath('//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tr[4]/td[2]/text()')).replace('\r\n','')
    infos["招生人数"] = ' '.join(tree.xpath('//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tr[5]/td[2]/text()')).replace('\r\n','')
    infos["招生状态"] = ' '.join(tree.xpath('//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tr[6]/td[2]/text()')).replace('\r\n','')
    # 联系网页端没有显示

    # 对补充内容做一下整理
    infos["补充内容"]  = ' '.join(tree.xpath('//tbody[@id="pid1"]/tr/td[@class="plc_mind"]/div[@class = "plc_Con"]/div[@class = "t_fsz"]/table/tr/td/text()'))
    return infos

def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['学校', '专业', '年级','招生人数','招生状态','补充内容']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insertData = [data[j]["学校"], data[j]["专业"],data[j]["年级"],data[j]["招生人数"],data[j]["招生状态"],data[j]["补充内容"]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表

def main():
    url_base = "http://muchong.com/f-430-{}-order-tid"
    # 这里可以更改爬取的页数 测试用，只爬第一页
    url_list = [url_base.format(i) for i in range(1,2)]
    total_infos = []
    for url in url_list:
        print(url)
        sch_urls,titles = parseSchool(url)
        num = 0
        for sch_url in sch_urls:
            print(f"正在爬取第{num}个学校")
            res_dic = parseSchoolInfo(sch_url)
            total_infos.append(res_dic)
            num += 1

            # 先爬10个
            if num == 10:
                break
    xw_toExcel(total_infos, "调剂信息.xlsx") 

if __name__ == "__main__":
    main()
