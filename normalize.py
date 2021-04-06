# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 20:31:13 2021

@author: DANQI
"""
import re
import pickle
from selenium import webdriver
import pandas as pd


#upload chebi_dict,上传chebi的字典
pkl_file = open('chebi_dict', 'rb')
chebi_dict = pickle.load(pkl_file)

#upload gene data,上传基因数据库
f = open("hgnc.txt",encoding="utf-8")
hgnc=pd.read_table(f,low_memory=False)
hgnc=hgnc.iloc[:,0:2]

f2 = open("mim_ens.txt",encoding="utf-8")
mim_ens=pd.read_table(f2,low_memory=False)

#upload rrid_gsm data  上传RRID数据
f = open("all_gsm_match_cell_line.txt",encoding="utf-8")
rrid=pd.read_table(f,low_memory=False)
rrid.fillna('null',inplace = True)
rrid=rrid.iloc[:,[0,4,5]]


class Normalize:
    def __init__(self,name):
        self.name=name
        
    def disease(self):
        if self.name != 'null' and self.name !='bern_zrb_disease_id' :
            #in case of the fisrt id is bern id
            #防止第一个id只有bern id，会使得开头出现“|”
            if re.match(r"BERN:\d", self.name):
                disease_list=self.name.split('|')[1:]
                if len(disease_list)==1:
                    return 'null'
                else:
                    pass
            else:
                
                disease_list=self.name.split('|')
            
            disease_output_id_disease_name_list=[]
            disease_output_disease_name_list=[]
            disease_output_id_disease_name=""
            disease_output_disease_name=""
            mesh_id_disease_name=""
            mesh_disease_name=""
            omim_disease_name=""
            omim_id_disease_name=""
            for i in disease_list:
                #print(chebi_id_drug_name)
                semicolon_list=i.split(';')
                for j in semicolon_list:
                    disease_database=j.split(':')[0]
                    disease_id=j.split(':')[1]
                    if disease_database =='MESH':
                        #print('MESH',j)
                        #设置浏览器不弹出
                        try:
                            option = webdriver.ChromeOptions()
                            option.add_argument('headless')
                            option.add_experimental_option('excludeSwitches', ['enable-logging'])
                            browser = webdriver.Chrome(options=option)
                            url='https://www.ncbi.nlm.nih.gov/mesh/?term={}'.format(disease_id)
                            browser.get(url)
                            source=browser.page_source
                            need=re.compile(r'<title>(.*)</title>')
                            out=need.findall(source)
                            mesh_name=out[0]
                            mesh_name=mesh_name.replace(' - MeSH - NCBI','')
                            #print(mesh_name)
                            mesh_name=mesh_name.strip()
                            #print(mesh_name)
                            mesh_id_disease_name=j+"=>"+mesh_name
                            mesh_disease_name=mesh_name
                            #print(mesh_id_disease_name)
                        except:
                            mesh_id_disease_name=j+"=>"+'null'
                            mesh_disease_name='null'                    
                    if disease_database =='OMIM':
                        #print('MESH',j)
                        #设置浏览器不弹出
                        try:
                            #print(j)
                            option = webdriver.ChromeOptions()
                            
                            option.add_argument('headless')
                            option.add_experimental_option('excludeSwitches', ['enable-logging'])
                            browser = webdriver.Chrome(options=option)
                            url='https://omim.org/entry/{}?search={}&highlight={}'.format(disease_id,disease_id,disease_id)
                            browser.get(url)
                            #input_text =        browser.find_element_by_xpath("html/head/title").text
                            source=browser.page_source
                            #匹配换行符
                            need=re.compile(r'<title>(.*)</title>',re.DOTALL)
                            out=need.findall(source)
                            #print(out)
                            omim_name=out[0]
                            omim_name=re.sub(r"\n", "",omim_name)
                            #print(omim_name)
                            omim_name=omim_name.split(' -')[2]
                            omim_name=re.sub(r"\n", "",omim_name)
                            omim_name=re.sub(r";", ":",omim_name)
                            omim_name=omim_name.strip()
                            #print(omim_name)
                            #print(mesh_name)
                            omim_id_disease_name=j+"=>"+omim_name
                            omim_disease_name=omim_name
                            
                        except:
                            omim_id_disease_name=j+"=>"+'null'
                            omim_disease_name='null' 
                #print(chebi_id_drug_name,mesh_id_drug_name)
                if mesh_id_disease_name and omim_disease_name:
                    disease_output_id_disease_name=omim_id_disease_name+";"+mesh_id_disease_name
                    disease_output_disease_name=omim_disease_name+";"+mesh_disease_name
                    
                else:
                    if mesh_id_disease_name:
                        disease_output_id_disease_name=mesh_id_disease_name
                        disease_output_disease_name=mesh_disease_name
                    if omim_disease_name:
                        disease_output_id_disease_name=omim_id_disease_name
                        disease_output_disease_name=omim_disease_name
                        
            
    ##########################################################################                        
                #print(disease_output_id_disease_name)
                disease_output_id_disease_name_list.append(disease_output_id_disease_name)
                disease_output_disease_name_2=disease_output_disease_name.split(';')
                # disease_output_disease_name_2_set=set(disease_output_disease_name_2)
                # disease_output_disease_name_2=list(disease_output_disease_name_2_set)
                # disease_output_disease_name=";".join(disease_output_disease_name_2)
                disease_output_disease_name_list=disease_output_disease_name_list+disease_output_disease_name_2
            
            #除去声明变量的空白变量
            #remove blank variable
            #disease_output_id_disease_name_list=disease_output_id_disease_name_list[1:]
            #disease_output_disease_name_list=disease_output_disease_name_list[1:]
            disease_output_id_disease_name_str="|".join(disease_output_id_disease_name_list)
            disease_output_disease_name_set=set(disease_output_disease_name_list)
            disease_output_disease_name_list=list(disease_output_disease_name_set)
            disease_output_disease_name_str="|".join( disease_output_disease_name_list)
            #print(disease_output_id_disease_name_str)
            #print(disease_output_disease_name_str)
            return disease_output_id_disease_name_str,disease_output_disease_name_str

        else:
            return 'null','null'

    
    def drug(self):
        
        if self.name != 'null' and self.name !='bern_zrb_drug_id' :
            if re.match(r"BERN:\d", self.name):
                drug_list=self.name.split('|')[1:]
                if len(drug_list)==1:
                    return 'null'
                else:
                    pass
            else:
                drug_list=self.name.split('|')
                
            #drug_list=self.name.split('|')
            drug_output_id_drug_name_list=[]
            drug_output_drug_name_list=[]
            drug_output_id_drug_name=""
            drug_output_drug_name=""
            mesh_id_drug_name=""
            mesh_drug_name=""
            chebi_drug_name=""
            chebi_id_drug_name=""
            #print(chebi_id_drug_name)
            for i in drug_list:
                #print(chebi_id_drug_name)
                semicolon_list=i.split(';')
                for j in semicolon_list:
                    # chebi_id_drug_name=''
                    # chebi_drug_name=''
                    # mesh_id_drug_name=''
                    # mesh_drug_name=''
                    #print(j)
                    drug_database=j.split(':')[0]
                    drug_id=j.split(':')[1]
                    #print(j)
                    if drug_database == 'CHEBI':
                        #print(j)
                        id_drug_name=j
                        if j in chebi_dict.keys():
                            #print(chebi_dict[j])
                            chebi_drug_name=chebi_dict[j]
                           
                            chebi_id_drug_name=id_drug_name+"=>"+chebi_dict[j]
                            #print(chebi_id_drug_name)
                        else:
                            chebi_drug_name=id_drug_name+"=>"+'null'
                            chebi_id_drug_name='null'
                            
                    if drug_database =='MESH':
                        #print('MESH',j)
                        #设置浏览器不弹出
                        try:
                            option = webdriver.ChromeOptions()
                            option.add_argument('headless')
                            option.add_experimental_option('excludeSwitches', ['enable-logging'])
                            browser = webdriver.Chrome(options=option)
                            url='https://www.ncbi.nlm.nih.gov/mesh/?term={}'.format(drug_id)
                            browser.get(url)
                            source=browser.page_source
                            need=re.compile(r'<title>(.*)</title>')
                            out=need.findall(source)
                            mesh_name=out[0]
                            mesh_name=mesh_name.replace(' - MeSH - NCBI','')
                            mesh_name=mesh_name.strip()
                            #print(mesh_name)
                            mesh_id_drug_name=j+"=>"+mesh_name
                            mesh_drug_name=mesh_name
                            #print(mesh_id_drug_name)
                        except:
                            mesh_id_drug_name=j+"=>"+'null'
                            mesh_drug_name='null'
                
                
                #print(chebi_id_drug_name,mesh_id_drug_name)
                if mesh_id_drug_name and chebi_drug_name:
                    drug_output_id_drug_name=chebi_id_drug_name+";"+mesh_id_drug_name
                    drug_output_drug_name=chebi_drug_name+";"+mesh_drug_name
                    #print(drug_output_id_drug_name)
                else:
                    if mesh_id_drug_name:
                        drug_output_id_drug_name=mesh_id_drug_name
                        drug_output_drug_name=mesh_drug_name
                    if chebi_drug_name:
                        drug_output_id_drug_name=chebi_id_drug_name
                        drug_output_drug_name=chebi_drug_name
    ##########################################################################                        
                drug_output_id_drug_name_list.append(drug_output_id_drug_name)
                drug_output_drug_name_2=drug_output_drug_name.split(';')
                # drug_output_drug_name_2_set=set(drug_output_drug_name_2)
                # drug_output_drug_name_2=list(drug_output_drug_name_2_set)
                # drug_output_drug_name=";".join(drug_output_drug_name_2)
                drug_output_drug_name_list=drug_output_drug_name_list+drug_output_drug_name_2
            
            #除去第一个刚好只有bern id的问题
            #remove blank variable
            #drug_output_id_drug_name_list=drug_output_id_drug_name_list[1:]
            #drug_output_drug_name_list=drug_output_drug_name_list[1:]
            drug_output_id_drug_name_str="|".join(drug_output_id_drug_name_list)
            drug_output_drug_name_set=set(drug_output_drug_name_list)
            drug_output_drug_name_list=list(drug_output_drug_name_set)
            drug_output_drug_name_str="|".join( drug_output_drug_name_list)
            #print(drug_output_id_drug_name_str)
            #print(drug_output_drug_name_str)
            return drug_output_id_drug_name_str,drug_output_drug_name_str            

                    
        else:
            return 'null','null'
        
    def gene (self):
        if self.name != 'null' and self.name !='bern_zrb_gene_id' :
            if re.match(r"BERN:\d", self.name):
                gene_list=self.name.split('|')[1:]
                if len(gene_list)==1:
                    return 'null'
                else:
                    pass
            else:
                gene_list=self.name.split('|')            
            gene_output_id_gene_name_list=[]
            gene_output_gene_name_list=[]
            gene_output_id_gene_name=""
            gene_output_gene_name=""
            mim_id_gene_name=""
            mim_gene_name=""
            hgnc_gene_name=""
            hgnc_id_gene_name=""
            ens_gene_name=""
            ens_id_gene_name=""            
            for i in gene_list:
                #print(chebi_id_drug_name)
                semicolon_list=i.split(';')
                for j in semicolon_list:
                    gene_database=j.split(':')[0]
                    gene_id=j.split(':')[1]
                    if gene_database =='MIM':
                        #print(j,gene_id)
                        try:
                            #exists = gene_id in mim_ens.MIM Number
                            #if 
                            #print(mim_name)
                            find_mim=mim_ens[mim_ens['MIM'].isin([int(gene_id)])]
                            #print(find_mim)
                            fine_min_len=find_mim.shape[0]
                            if fine_min_len > 0:
                                mim_name=find_mim.iloc[0,3]
                                mim_id_gene_name=j+"=>"+mim_name
                                mim_gene_name=mim_name  
                                #print(mim_id_gene_name,mim_gene_name)
                            else:
                                mim_id_gene_name=j+"=>"+'null'
                                mim_gene_name='null'                                
                            #print(mim_id_gene_name)
                        except:
                            mim_id_gene_name=j+"=>"+'null'
                            mim_gene_name='null'             
                    if gene_database =='Ensembl':
                        #print(j,gene_id)
                        try:
                            #exists = gene_id in ens_ens.ens Number
                            #if 
                            #print(ens_name)
                            #print(j)
                            find_ens=mim_ens[mim_ens['Ensembl'].isin([gene_id])]
                            #print(find_ens)
                            fine_min_len=find_ens.shape[0]
                            if fine_min_len > 0:
                                ens_name=find_ens.iloc[0,3]
                                ens_id_gene_name=j+"=>"+ens_name
                                ens_gene_name=ens_name  
                                #print(ens_id_gene_name,ens_gene_name)
                            else:
                                ens_id_gene_name=j+"=>"+'null'
                                ens_gene_name='null'                                
                            #print(ens_id_gene_name)
                        except:
                            ens_id_gene_name=j+"=>"+'null'
                            ens_gene_name='null'                        
                    if gene_database =='HGNC':
                        #print(j,gene_id)
                        try:
                            #exists = gene_id in hgnc_hgnc.hgnc Number
                            #if 
                            #print(hgnc_name)
                            #print(j)
                            find_hgnc= hgnc[hgnc['hgnc_id'].isin([j])]
                            #print(find_hgnc)
                            fine_min_len=find_hgnc.shape[0]
                            if fine_min_len > 0:
                                hgnc_name=find_hgnc.iloc[0,1]
                                hgnc_id_gene_name=j+"=>"+hgnc_name
                                hgnc_gene_name=hgnc_name  
                                #print(hgnc_id_gene_name,hgnc_gene_name)
                            else:
                                hgnc_id_gene_name=j+"=>"+'null'
                                hgnc_gene_name='null'                                
                            #print(hgnc_id_gene_name)
                        except:
                            hgnc_id_gene_name=j+"=>"+'null'
                            hgnc_gene_name='null'  

                
                ###try new method
                all_gene_name_list=[hgnc_gene_name,ens_gene_name,mim_gene_name]

                all_gene_name_id_list=[hgnc_id_gene_name,ens_id_gene_name,mim_id_gene_name]
                for n in range(len(all_gene_name_list)):
                    
                    if all_gene_name_list[n] :
                        gene_output_id_gene_name=gene_output_id_gene_name+";"+all_gene_name_id_list[n]
                        gene_output_gene_name=gene_output_gene_name+";"+all_gene_name_list[n]
                    else:
                        pass
                #remove the first ";", becasue ";HGNC:6001=>IL2" will be displayed in new method    
                gene_output_id_gene_name=gene_output_id_gene_name[1:]
                gene_output_gene_name=gene_output_gene_name[1:]
                gene_output_id_gene_name_list.append(gene_output_id_gene_name)                    
                gene_output_gene_name_2=gene_output_gene_name.split(';')
                # gene_output_gene_name_2_set=set(gene_output_gene_name_2)
                # gene_output_gene_name_2=list(gene_output_gene_name_2_set)
                # gene_output_gene_name=";".join(gene_output_gene_name_2)
                gene_output_gene_name_list=gene_output_gene_name_list+gene_output_gene_name_2
                gene_output_id_gene_name=''
                gene_output_gene_name=''
                
            gene_output_id_gene_name_str="|".join(gene_output_id_gene_name_list)
            
            #gene_output_id_gene_name_str=gene_output_id_gene_name_str[1:]
            gene_output_gene_name_set=set(gene_output_gene_name_list)
            gene_output_gene_name_list=list(gene_output_gene_name_set)
            gene_output_gene_name_str="|".join( gene_output_gene_name_list)
            #gene_output_gene_name_str=gene_output_gene_name_str[1:]
            #print(gene_output_id_gene_name_str)
            #print(gene_output_gene_name_str)
            return gene_output_id_gene_name_str,gene_output_gene_name_str                   
        else:
            return 'null','null'
    
    def knock_out(self):
        p1 = re.compile(r"[Kk]nock[ -]?[Oo]ut|[Kk]nock[ -]?[Dd]own")
        p2 = re.compile(r"[Kk]nock[ -]?[Ii]n")
        p3 = re.compile(r"[Kk]nock[ -]?/b")
        p4 = re.compile(r"[Oo]ver[ -]?[Ee]xpressio?ng?")
        if p1.findall(self.name):
            knock_out_down='y'
        else:
            knock_out_down='null'
        
        if p2.findall(self.name):
            knock_in='y'
        else:
            knock_in='null'
        
        if p3.findall(self.name):
            knock='y'
        else:
            knock='null'
        if p4.findall(self.name):
            over='y'
        else:
            over='null'
        return knock_out_down,knock_in,knock,over
        #print(knock_out_down,knock_in,knock,over)
    def cell_line(self):
        cell_line_list=[]
        #cell_line_set=()
        with open('only_gsm_cell_line.txt','r',encoding='utf-8') as cl:
            while True:
                cell_line=cl.readline()
                cell_line=cell_line.strip()
                cell_line=str(cell_line)
                #cell_line="'"+cell_line+"'"
                cell_line=cell_line.replace('[','\[')
                cell_line=cell_line.replace(']','\]')
                cell_line=cell_line.replace('.','\.')
                cell_line=cell_line.replace('(','\(')
                cell_line=cell_line.replace(')','\)')
                cell_line=cell_line.replace('-','\-')
                cell_line=cell_line.replace('$','\$')
                cell_line=cell_line.replace('|','\|')
                
                
                "-", "_", "--", "/"

                if cell_line:
                    #print(cell_line)
                    need=re.compile(r'\b{}\b'.format(cell_line))
                    out=need.findall(str(self.name))
                    
                    need2=re.compile(r'[\-\_\-\-\/\\]')
                    cell_line_2=need2.findall(cell_line)
                    if cell_line_2:
                        cell_line_3=need2.sub(r'',cell_line)
                        #print(cell_line_3)
                        need_2=re.compile(r'\b{}\b'.format(cell_line_3))
                        
                        out_2=need_2.findall(str(self.name))
                        #print(out_2)
                    else:
                        out_2=['']
                        
                    out=out+out_2
                    while '' in out:
                        out.remove('')
                    
                    if len(out)>0:
                        for j in out:                            
                            cell_line_list.append(j)
                    else:
                        pass
                
                else:
                    break
        
        if len(cell_line_list)>0:
            
            #cell_line_set=set(cell_line_list)
            #cell_line_list=list(cell_line_set)
            cell_line_list=[str(v) for v in cell_line_list]
            cell_line_set=set(cell_line_list)
            cell_line_list=list(cell_line_set)
            cell_line_str="|".join(cell_line_list)
            #print(cell_line_str)
        else:
            cell_line_str='null'
        return cell_line_str
            
    def rrid_gsm(self):
        try:
            find_gsm=rrid[rrid['GSM'].isin([self.name])]
            find_gsm_len=find_gsm.shape[0]
            if find_gsm_len>0:
                find_cell_line=find_gsm.iloc[0,0]
                find_disease=find_gsm.iloc[0,1]
            else:
                find_cell_line='null'
                find_disease='null'
                
        except:
            find_cell_line='null'
            find_disease='null'
        
        return find_cell_line,find_disease
        
    def gsm_gse(self):
        #print(self.name)
        gsm_gse=[]
        #try:
        #driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe')
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        
        ##based on your own chromedriver path
        browser = webdriver.Chrome(options=option)
        
        url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={}'.format(self.name)
        browser.get(url)
        source=browser.page_source
        #print(source)
        need=re.compile(r'<a href="/geo/query/acc.cgi\?acc=.*" onmouseout="onLinkOut\(\'HelpMessage\' , geo_empty_help\)" onmouseover="onLinkOver\(\'HelpMessage\' , geoaxema_recenter\)">(.*)</a>')
        out=need.findall(source)
        #print(out)
        for i in out:
            #print(i)
            if re.match('GSE',i):
                #print()
                i=i.strip()
                gsm_gse.append(i)
                #download_gse(i)
                #pipeline(i, output)
        return gsm_gse
        #except:
            #print("we can not download {} successfully".format(self.name))

# gse_gsm=Normalize('GSM613385')
# gse_gsm_list=gse_gsm.gsm_gse()
# print(gse_gsm_list)

# with open('gse_test.txt','r',encoding='UTF-8') as f:
#     while True:
#         line=f.readline()
#         if line:
#             #去除第一行标题
#             #remove title line
#             if re.match(r'GSE',line):
#                 line=line.strip()
#                 line_list=line.split('\t')
                
# #                 disease_id=line_list[13]
# # ###############################################################
# #                 #调用规范化疾病名称
# #                 #call the function to normalize disease name                
# #                 test_disease=Normalize(disease_id)
# #                 disease_output_id_disease_name_str,disease_output_disease_name_str=test_disease.disease()
# #                 print('disease_id',disease_output_id_disease_name_str,disease_output_disease_name_str)
# #                 drug_id=line_list[15]
                
# # ###############################################################
# #                 #调用规范化药物名称
# #                 #call the function to normalize drug name
# #                 test=Normalize(drug_id)
# #                 id_drug_name,drug_name=test.drug()
                
# #                 #print(id_s)
# #                 print('drug_id', id_drug_name,drug_name)
# #                 gene_id=line_list[17]
# #                 test_gene=Normalize(gene_id)
# #                 gene_output_id_gene_name_str,gene_output_gene_name_str=test_gene.gene()
# #                 print('gene_id',gene_output_id_gene_name_str,gene_output_gene_name_str)
# #####################################################
#                 # knock_line=line_list[3]
#                 # test_knock=Normalize(knock_line)
#                 # test_knock.knock_out()
#                 # print(knock_line)
#                 # print('gene_id',gene_id)
# #####################################################
#                 gsm_id=line_list[1]
#                 # test_gsm_rrid=Normalize(gsm_id)
#                 # cell_line,cell_line_disease=test_gsm_rrid.rrid_gsm()
#                 # print(gsm_id,"test_gsm_rrid",cell_line,cell_line_disease)
                
                
#                 gse_text=line_list[2]
#                 test_regex=Normalize(gse_text)
#                 text_regex_cell_line=test_regex.cell_line()
#                 print(gsm_id,'text_regex_cell_line',text_regex_cell_line)
                
#                 gse_bern_test=line_list[3]
#                 bern_test_regex=Normalize(gse_bern_test)
#                 bern_text_regex_cell_line=bern_test_regex.cell_line()
#                 print(gsm_id,'bern_text_regex_cell_line',bern_text_regex_cell_line)
                
#         else:
#             break
    