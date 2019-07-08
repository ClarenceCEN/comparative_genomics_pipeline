import json
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
from requests.exceptions import RequestException
import re
import math
import sys

def index_1st_ele(item):
    if len(item)>=1:
        return item[0]
    else:
        return ""

def generate_download_url(url):
    items = ['genomic.fna', 'protein.faa', 'cds_from_genomic.fna', 'feature_table.txt']
    pattern_genomic_fna_header = re.compile('(GC[AF]_.*)')
    if len(url)>0:
        download_header = re.findall(pattern_genomic_fna_header, url)[0]
    else:
        print(download_header)
    download_urls = []
    for item in items:
        entire_url = url + '/' + download_header + '_' + item + '.gz'
        download_urls.append(entire_url)
    #pattern_genomic_fna = re.compile('"(genomes/all/.*?_genomic.fna.gz)">')
    #genomic_fna_url = re.findall(pattern_genomic_fna, )
    yield ["wget " + download_urls[0], "wget " + download_urls[1],
           "wget " + download_urls[2], "wget " + download_urls[3], download_header]

def look_for_download_url(url):
    html = requests.get(url).text
    pattern_Ref = re.compile('(ftp://ftp.ncbi.nlm.nih.gov/genomes/all/.*?)">Download the RefSeq')
    pattern_Gen = re.compile('(ftp://ftp.ncbi.nlm.nih.gov/genomes/all/.*?)">Download the GenBank')
    print("Now looking for the link")
    Ref_url = re.findall(pattern_Ref, html)
    Gen_url = re.findall(pattern_Gen, html)
    print('Finished')
    if len(Ref_url)>0:
        result = Ref_url[0]
    elif len(Gen_url)>0:
        result = Gen_url[0]
    else:
        result = 'GCF_---'
    return result

def look_for_info(url):
    '''info_list = ['host', 'isolation','environment_feature','environment_material','strain']
    pattern_names = locals()
    for info in info_list:
        #global pattern_names['pattern_%s'%info]
        pattern_names['pattern_%s' % info]= \
            re.compile(r'<th>'+info+'</th><td>(.*?)</td>')'''
    html = requests.get(url).text
    #提取biosample中的样品信息
    pattern_geographic = re.compile('<tr>.*?geographic location.*?<td><a.*?>(.*?)<.*?>')
    #print(pattern_names.get('pattern_host'))
    pattern_host = re.compile('<th>host</th><td>(.*?)</td>')
    pattern_isolation_source = re.compile('<th>isolation source</th><td>(.*?)</td>')
    pattern_environment_feature = re.compile('<th>environment feature</th><td>(.*?)</td>')
    pattern_environment_material = re.compile('<th>environment material</th><td>(.*?)</td>')
    pattern_strain = re.compile('<th>strain</th><td>(.*?) </td>')
    results_geographic = re.findall(pattern_geographic, html)
    results_host = re.findall(pattern_host, html)
    results_isolation_source = re.findall(pattern_isolation_source, html)
    results_environment_feature = re.findall(pattern_environment_feature, html)
    results_environment_material = re.findall(pattern_environment_material, html)
    results_strain = re.findall(pattern_strain, html)

    geographic_location = index_1st_ele(results_geographic)
    geographic_location = geographic_location.replace(',', ' ')
    #yield {
    #    'geographic' : results_geographic,
    #    'host' : results_host,
    #    'isolation_source' : results_isolation_source,
    #    'environment_feature' : results_environment_feature,
    #    'environment_material': results_environment_material
    #}
    if (len(index_1st_ele(results_host))!=0 or
                                        len(index_1st_ele(results_isolation_source))!=0 or
                                        len(index_1st_ele(results_environment_feature))!=0 or
                                        len(index_1st_ele(results_environment_material))!=0):
        yield [index_1st_ele(results_strain),
               geographic_location, index_1st_ele(results_host),
               index_1st_ele(results_isolation_source), index_1st_ele(results_environment_feature),
               index_1st_ele(results_environment_material)]
    else:
        return ""

def write_to_file_for_sample(content, bac_name): #需要改文件名称！
    name_for_file = bac_name.replace(" ", "_")
    print(json.dumps(content))
    result_dict = json.dumps(content)
    with open('info_'+name_for_file+'.csv', 'a') as f:
        f.write(result_dict+'\n')
        f.close()

def write_to_file_for_links(url, bac_name): #需要改文件名称！
    name_for_file = bac_name.replace(" ", "_")
    print(json.dumps(url))
    result_dict = json.dumps(url)
    with open('links_'+name_for_file+'.csv', 'a') as f:
        f.write(result_dict + '\n')
        f.close()

def parse_one_page(html, bac_name): #需要改菌株名称！
    print("Now parsing the page")
    #解析biosample页面
    pattern_sample = re.compile(r'<td>.*?target="_blank">(.*?)</a>.*?href="(/biosample.*?)"',
                                re.S)
    results_sample = re.findall(pattern_sample, html)
    sample_urls = []
    for result in results_sample:
        sample_urls.append("https://www.ncbi.nlm.nih.gov"+result[1])
    #解析assembly页面
    pattern_assembly = re.compile('<td><a href="(/assembly/.*?)".*?>(GC.*?)</a>', re.S)
    result_assembly = re.findall(pattern_assembly, html)
    assembly_urls = []
    for result in result_assembly:
        assembly_urls.append("https://www.ncbi.nlm.nih.gov"+result[0])
    return [sample_urls, assembly_urls]

def js2html(url, bac_name):
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    #browser.implicitly_wait(10)
    browser.get(url)
    total_item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#maincontent > div > div.MainBody > div.page_nav > span > b")))
    total_item = int(total_item.text)
    page = math.ceil(total_item/100)
    for i in range(0,page):
        try:
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ui-ui-ncbigrid-paged-countItems-1 > span.ui-ncbigrid-paged-startRow"), str(i*100+1)))
            html = browser.page_source
            if i == 1:
                with open("html_source.txt", 'w') as f:
                    f.write(json.dumps(html))
            write_informations(html, bac_name)
            next_page = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="maincontent"]/div/div[2]/div[3]/div[1]/div[2]/a[3]'))
            )
            next_page.click()
            sleep(5)
            if i == page-1:
                browser.close()
        except TimeoutException:
            print("time out!")

def generate_urls(bac_name):
    name_split = bac_name.split()
    page_one_url = 'https://www.ncbi.nlm.nih.gov/genome/?term=' + name_split[0] + '%20' + \
                   name_split[1]
    browser = webdriver.Chrome()
    browser.get(page_one_url)
    html = browser.page_source
    pattern = re.compile('<a class="page_nav" href="(.*?)">.*?'
                         'Genome Assembly and Annotation report', re.S)
    result = re.findall(pattern, html)
    browser.close()
    #print(result)
    genome_url = 'https://www.ncbi.nlm.nih.gov' + result[0]
    #print(genome_page)
    return genome_url

def write_informations(html, bac_name):
    sample_urls = parse_one_page(html, bac_name)[0]
    assembly_urls = parse_one_page(html, bac_name)[1]
    print(assembly_urls)
    no_info = []
    index_of_sample = 0
    if len(assembly_urls)==len(sample_urls):
        print(len(assembly_urls),'items.')
        print('It worked!')
        for sample_url in sample_urls:
            for item in look_for_info(sample_url):
                no_info.append(index_of_sample)
                #print(json.dumps(item))
                write_to_file_for_sample(item, bac_name)
            index_of_sample += 1
        index_of_url = 0
        for assembly_url in assembly_urls:
            for download_url in generate_download_url(look_for_download_url(assembly_url)):
                if index_of_url in no_info:
                    write_to_file_for_links(download_url, bac_name)
            index_of_url += 1
    else:
        print('Something is wrong!')

def main(bac_name): #需要改菌株链接！
    genome_url = generate_urls(bac_name)
    js2html(genome_url, bac_name)






if __name__ == '__main__':
    main(sys.argv[1])