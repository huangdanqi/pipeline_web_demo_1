# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:53:02 2021

@author: DANQI

take a break *^ο^* 
(ToT) hard but need to find fun \^o^/

"""


#try:
#from selenium import webdriver
import pickle
import pandas as pd
import normalize
import requests
import time 
import xml.dom.minidom
import re
import wget
import tarfile
#import shutil
import os
from pathlib import Path
import argparse
#import pandas as pd
#from selenium import webdriver
#import re

#gse_list=["GSE167334","GSE167089","GSE167037"]

#gse_list=["GSE167089","GSE167037"]
# gse="GSE167089"


def download_gse(gse):
    my_file = Path("./gse")
    if my_file.exists():
        pass
    else:
        os.makedirs('./gse') if not os.path.isdir('gse') else None
        #os.makedirs('./gse') if not os.path.isdir('gse') else None

    #for gse in gse_list:
        
    path_gse_file="./gse/"+gse+"_family.xml"    
    gse_file=Path(path_gse_file)
    if gse_file.exists():
        print('\n{} exist'.format(gse))
    else:
        print('\n{} does not exist'.format(gse))
        try:
            gse_nnn=gse[:-3]
            gse_nnn=gse_nnn+"nnn"
            url="ftp://ftp.ncbi.nlm.nih.gov/geo/series/"+gse_nnn+"/"+gse+"/miniml/"+gse+"_family.xml.tgz"
    
            wget.download(url,out='gse')
            try :
                path_gse="./gse/"+gse+"_family.xml.tgz"
                data_folder = Path(path_gse)
                tar = tarfile.open(data_folder)  
                names = tar.getnames()   
                for name in names:  
                    #print(name)
                    tar.extract(name,'gse')  
                tar.close()
            except Exception :
                print('extract wrong')
            
            dirs = os.listdir('gse')
            gse_extract_file_list=[]
        #for j in gse_list:
            gse_extract_file=gse+"_family.xml"
            gse_extract_file_list.append(gse_extract_file)
                
            
            #gse_extract_file=gse+"_family.xml"
            #gse_extract_file_tgz=gse+"_family.xml.tgz"
            #print(i,gse_extract_file)
            #print(dirs)
            pattern = re.compile(r'.*_family\.xml$') 
            
            for i in dirs:    
                #print(i)
                #print(gse_extract_file_list)
                m = pattern.findall(i)
                if m :
                    #print(i)
                    pass
                else:
                    path="./gse"+"/"+i
                    data_folder = Path(path)
                    os.remove(data_folder)
        except:
            print('{},we can not download this gse.\n'.format(gse))
        
# download_gse(gse)


def query_raw(text, url="https://bern.korea.ac.kr/plain"):
    try:
        return requests.post(url, data={'sample_text': text}).json()
    except(requests.exceptions.ConnectionError,NameError):
        time.sleep(10)
        return requests.post(url, data={'sample_text': text}).json()

def bern_list(output):
    
    disease=[]
    disease_id=[]
    
    drug=[]
    drug_id=[]
    
    gene=[]
    gene_id=[]
    

    
    if output:
        try:
            
            if output['denotations']:
                
                for i in output['denotations']:
                    if i['obj'] == 'disease':
                                
                        if i['obj']:
                            n=i['span']
                            begin=n['begin']
                            end=n['end']
                            #print(n)
                            name=str(output['text'])[begin:end]
                             
                            id_list=i['id']
                            for j in id_list:
                                if str(j)=='CUI-less':
                                    break
                                else:
                                    id_need=";".join(id_list)
                                    disease_id.append(id_need)
                                    disease.append(name) 
          
                    if i['obj'] == 'drug':
                        if i['obj']:
                            n=i['span']
                            begin=n['begin']
                            end=n['end']
                            #print(n)
                            name=str(output['text'])[begin:end]
                    
                            id_list=i['id']
                            for j in id_list:
                                if str(j)=='CUI-less':
                                    break
                                else:
                                    id_need=";".join(id_list)
                                    drug_id.append(id_need)
                                    drug.append(name) 
                            #species.append(name)
                    
                    if i['obj'] == 'gene':
                        if i['obj']:
                            n=i['span']
                            begin=n['begin']
                            end=n['end']
                            #print(n)
                            name=str(output['text'])[begin:end]
                            #gene.append(name)
                            id_list=i['id']
                            for j in id_list:
                                if str(j)=='CUI-less':
                                    break
                                else:
                                    id_need=";".join(id_list)
                                    gene_id.append(id_need)
                                    gene.append(name) 
            if disease:
                disease_set=set(disease)
                disease_str='|'.join(disease_set)
                disease_id_set=set(disease_id)
                disease_id_str='|'.join(disease_id_set)
                
                # for i in disease_set:
                #     disease_str=disease_str+i+','
                #     disease_str=disease_str[:-1]    
            else:
                disease_str='null'
                disease_id_str='null'
                
            if drug:
                drug_set=set(drug)
                drug_str='|'.join(drug_set)
                drug_id=set(drug_id)
                drug_id_str='|'.join(drug_id)       
            else:
                drug_str='null'
                drug_id_str='null'
                
            if gene:
                gene_set=set(gene)
                gene_str='|'.join(gene_set)
                gene_id=set(gene_id)
                gene_id_str='|'.join(gene_id)
            else:
                gene_str='null'
                gene_id_str='null'
        except:
            disease_str=disease_id_str=drug_str=drug_id_str=gene_str=gene_id_str='null'
            
    else:
        disease_str=disease_id_str=drug_str=drug_id_str=gene_str=gene_id_str='null'
        
    return disease_str,disease_id_str,drug_str,drug_id_str,gene_str,gene_id_str 

def pipeline(gse, output='output',append='n',geo='gse'):
    path_gse_extract="./"+output    
    gse_file=Path(path_gse_extract)
    if gse_file.exists():
        pass
    else:
        
    
        with open(output,"a+",encoding='utf-8') as out:
            
        #     title=['gse','gsm','text','bern_text','cell line','organism','cell type','method','source name','tissue','treatment','disease','bern_zrb_disease','bern_zrb_disease_id','bern_zrb_drug','bern_zrb_drug_id','bern_zrb_gene','bern_zrb_gene_id'] 
            title=['gse','gsm','text','bern_text','pmid','cell line','organism','cell type','method','source name','tissue','treatment','disease','library_strategy','lstrategy_add','library_source','molecule','Sample_type','Last_Update_Date','Release_Date','Supplementary_Data','s_platform_ref','bern_disease_str','bern_disease_id_str','normolize_disease_id_name','normolize_disease_name','bern_drug_str','bern_drug_id_str','normolize_drug_id_name','normolize_drug_name','bern_gene_str','bern_gene_id_str','normolize_gene_id_name','normolize_gene_name','knock_out/knock_down','knock_in','knock','over_expression','cell_line_text_regex','cell_line_bern_text_regex','gsm_rrid_cell_line','gsm_rrid_disease']     
            # title_line="\t".join(title)
            # out.write(title_line)
            # out.write('\n')

            title_line="\t".join(title)
            out.write(title_line)
            out.write('\n')
        
        
        
    # file_list=[]
    file_list=[x for x in os.listdir('gse') if x.startswith(gse)]
    if not file_list:
        pass
        #print('\n+++ The lookup table doesn\'t have {}.' .format(gse))
        return(None)
   # print(file_list)

    for i_file in file_list:

        file_path = os.path.join(os.path.abspath('.'), 'gse')
        file_path_need = os.path.join( file_path,i_file)

        
       
        dom=xml.dom.minidom.parse(file_path_need)
        def move_break(need_list):
            
            for i in range(len(need_list)):
                need_list[i]=re.sub("\n","",need_list[i])
                need_list[i]=re.sub("\s+"," ",need_list[i])
            return need_list    
       
        #单独获取测序方法
        Platform = dom.getElementsByTagName("Platform")
        p_technology_list=[]
        for i_p in range(Platform.length):

      
            try:
                p_technology=dom.getElementsByTagName("Platform")[i_p].getElementsByTagName("Technology")[0].childNodes[0].data
                p_technology_list.append(p_technology)
               
            except:
                p_technology_list.append("null")
            

        p_technology_set=set(p_technology_list)
        p_technology_list=list(p_technology_set)
        p_technology_list=move_break(p_technology_list)
        #print(p_technology_set)
        #print(p_technology_list)        
        p_technology_all=",".join(str(x) for x in p_technology_list)        



        series = dom.getElementsByTagName("Series")
        for i in range(series.length):
            try:
                se_pmid=series[i].getElementsByTagName("Pubmed-ID")[0].childNodes[0].data
            except:
                se_pmid="null"  
        
        
        #extract sample tags
        #extract sample tags
        sample=dom.getElementsByTagName("Sample")
        #sample_list=[]
        #sample_data_list=[]
        sample_char_list=[]
        #sample_table_list=[]
        for i_s in range(sample.length):
            output_list=[]
            try:
                s_number=sample[i_s].getAttribute("iid")
                
            except:
                s_number="null"
                
            try:
                s_title=sample[i_s].getElementsByTagName("Title")[0].childNodes[0].data
            except:
                s_title=sample[i_s]="null"
            
            try:
                s_channel=sample[i_s].getElementsByTagName("Channel-Count")[0].childNodes[0].data
            except:
                s_channel="null"
            
            try:
                s_source=sample[i_s].getElementsByTagName("Source")[0].childNodes[0].data
            except:
                s_source="null"
            
            try:
                s_organism=sample[i_s].getElementsByTagName("Organism")[0].childNodes[0].data
            except:
                s_organism="null"
                
            #会出现换行符
            try:
                s_treatment=sample[i_s].getElementsByTagName("Treatment-Protocol")[0].childNodes[0].data
            except:
                s_treatment="null"
            #print(s_title)    
            #会出现换行符
            # try:
            #     s_growth=sample[i_s].getElementsByTagName("Growth-Protocol")[0].childNodes[0].data
            # except:
            #     s_growth="null"
                
            try:
                s_molecule=sample[i_s].getElementsByTagName("Molecule")[0].childNodes[0].data
            except:
                s_molecule="null"
                
            # try:
            #     s_extract=sample[i_s].getElementsByTagName("Extract-Protocol")[0].childNodes[0].data
            # except:
            #     s_extract="null"
            
            try:
                s_label=sample[i_s].getElementsByTagName("Label")[0].childNodes[0].data
            except:
                s_label="null"
            #换行符会出现在句字中，用空格代替，再将多个空格替换成一个空格    
            try:
                s_data_processing=sample[i_s].getElementsByTagName("Data-Processing")[0].childNodes[0].data
            except:
                s_data_processing="null"

            try:
                s_library_strategy=sample[i_s].getElementsByTagName("Library-Strategy")[0].childNodes[0].data
            except:
                s_library_strategy="null"
            
            try:
                s_library_source=sample[i_s].getElementsByTagName("Library-Source")[0].childNodes[0].data
            except:
                s_library_source="null"                

            # try:
            #     s_molecule=sample[i_s].getElementsByTagName("Molecule")[0].childNodes[0].data
            # except:
            #     s_molecule="null"  
 
            try:
                s_type=sample[i_s].getElementsByTagName("Type")[0].childNodes[0].data
            except:
                s_type="null"                     

            try:
                s_supplementary=sample[i_s].getElementsByTagName("Supplementary-Data")[0].childNodes[0].data
            except:
                s_supplementary="null" 
                
            try:
                s_description=sample[i_s].getElementsByTagName("Description")[0].childNodes[0].data
                try:
                    ## find libaray strategy in Description and Data Processing
                    ## this usaully happends in new techniques
                    text = s_description + s_data_processing
                    regx = re.compile(r'library strategy: .*|library-strategy: .*', re.I)
                    regx_match = re.search(regx, text)
                    ## iterate and extract libraray strategy if matched
                    lstrategy_add = regx_match.group().split(': ')[-1].strip() if regx_match else 'null'
                except:
                    lstrategy_add = 'null'
            except:
                s_description="null"
                lstrategy_add = 'null'
            
            try:
                s_platform_ref=sample[i_s].getElementsByTagName("Platform-Ref")[0].getAttribute("ref")
                
            except:
                 s_platform_ref="null"
            
            try:
                s_Last_Update_Date=sample[i_s].getElementsByTagName("Last-Update-Date")[0].childNodes[0].data
                
            except:
                 s_Last_Update_Date="null"     
            
            try:
                s_Release_Date=sample[i_s].getElementsByTagName("Release-Date")[0].childNodes[0].data
                
            except:
                s_Release_Date="null"         
                 
            #SAGE 特有的
            try:
                s_anchor=sample[i_s].getElementsByTagName("Anchor")[0].childNodes[0].data
                s_anchor="(SAGE_anchor)"+s_anchor
            except:
                s_anchor="(SAGE_anchor)null"
            
            try:
                s_type_sage=sample[i_s].getElementsByTagName("Type")[0].childNodes[0].data
                s_type_sage="(SAGE_type)"+s_type
            except:
                s_type_sage="(SAGE_type)null"
            
            try:
                s_tag_count=sample[i_s].getElementsByTagName("Tag-Count")[0].childNodes[0].data
                s_tag_count="(SAGE_count)"+s_tag_count
            except:
                s_tag_count="(SAGE_count)null"
            
            try:
                s_tag_length=sample[i_s].getElementsByTagName("Tag-Length")[0].childNodes[0].data
                s_tag_length="(SAGE_len)"+s_tag_length
            except:
                s_tag_length="(SAGE_len)null"
                
    
            
            #把characteristic放在最后，是因为characteristic对每个GSE是不同的
            chr_str=''
            try:
                s_char_array=sample[i_s].getElementsByTagName("Characteristics")
                for i in range(s_char_array.length):
                    s_char_tag=s_char_array[i].getAttribute("tag")
                    
                    #text里面有换行符
                    s_char_text=s_char_array[i].childNodes[0].data
                    if not s_char_tag:
                        s_char_tag='characteristics'
                    chr_str=chr_str+"'"+s_char_tag+"'"+":"+"'"+s_char_text+"'"+","
                    s_char="[char]({}){}".format(s_char_tag,s_char_text)
                    sample_char_list.append(s_char)
                s_char_need="*#*#*#".join(sample_char_list)   
                sample_char_list=[]
                
            except:
                s_char_need="null"
            
            chr_str=re.sub(r'\n', '', chr_str)  
            chr_str=re.sub(r'\s+', ' ', chr_str)
            output_col_1="{"+chr_str+"'organism':"+"'"+s_organism+"'"+",'source name':"+"'"+s_source+"'"+", 'title':"+"'"+s_title+"'"+", 'last update date':"+"'"+s_Last_Update_Date+"'"+", 'release date': "+"'"+s_Release_Date+"'"+", 'method': "+"'"+p_technology_all+"'"+"}"
            output_list.append(gse)
            output_list.append(s_number)
            output_list.append(output_col_1)
            
            #output_list.append(virus_name)
                    #换行符和多个空格的问题
            sample_single=s_number+"*#*#*#"+s_title+"*#*#*#"+s_channel+"*#*#*#"+s_source+"*#*#*#"+s_organism+"*#*#*#"+s_treatment+"*#*#*#"+s_molecule+"*#*#*#"+s_label+"*#*#*#"+s_data_processing+"*#*#*#"+s_library_strategy+"*#*#*#"+s_description+"*#*#*#"+s_platform_ref+"*#*#*#"+s_Last_Update_Date+"*#*#*#"+s_Release_Date+"*#*#*#"+s_anchor+"*#*#*#"+s_type_sage+"*#*#*#"+s_tag_count+"*#*#*#"+s_tag_length+"*#*#*#"+s_char_need
            sample_single_list=[sample_single]
            sample_single_list=move_break(sample_single_list)
            sample_single=sample_single_list[0]
            
            
            output_list.append(sample_single)
            #print("sample_single:{}".format(sample_single))
            
            output_list.append(se_pmid)
            #zrb_bern=query_raw(output_col_1)
            #print(sample_list_all)
            #hdq_bern=query_raw(sample_single)
            
            
            #extract characteristic alone
            # line_list=line.split('\t')
            # line_text=line_list[0]
            
            #line_dict={}
            line_text_list=output_col_1.split(',')
            line_dict={}
            match_list=['cell line','organism','cell type','method','source name','tissue','disease','treatment']
            for i in line_text_list:
                i=re.sub("'", "", i)
                i=re.sub(r"\{", "", i)
                i=re.sub(r"\}", "", i)
                i=re.sub(r'"', "", i)
                i=i.strip()
                dcit_list=i.split(':')
                #line_dict[str(dcit_list[0])]=str(dcit_list[1])
                
                dcit_list[0]=re.sub("'", "", dcit_list[0])
                dcit_list[0]=re.sub(r"\{", "", dcit_list[0])
                dcit_list[0]=re.sub(r"\}", "", dcit_list[0])
                dcit_list[0]=re.sub(r'"', "", dcit_list[0])
                dcit_list[0]=str(dcit_list[0]).strip()
                try:
                    line_dict[str(dcit_list[0])]=str(dcit_list[1])
                except:
                    line_dict[str(dcit_list[0])]='null'
            for i in match_list:
                if i in line_dict.keys():
                    line_dict[i]=str(line_dict[i]).strip()
                    output_list.append(str(line_dict[i]))
                else:
                    output_list.append('null')
    
            output_list.append(s_library_strategy)
            output_list.append(lstrategy_add)
            output_list.append(s_library_source)
            output_list.append(s_molecule)
            output_list.append(s_type)
            output_list.append(s_Last_Update_Date)
            output_list.append(s_Release_Date)
            
            output_list.append(s_supplementary)
            output_list.append(s_platform_ref)

            
        #换行符和多个空格的问题
            #sample_single=s_number+"*#*#*#"+s_title+"*#*#*#"+s_channel+"*#*#*#"+s_source+"*#*#*#"+s_organism+"*#*#*#"+s_treatment+"*#*#*#"+lstrategy_add+"*#*#*#"+s_molecule+"*#*#*#"+s_label+"*#*#*#"+s_data_processing+"*#*#*#"+s_description+"*#*#*#"+s_platform_ref+"*#*#*#"+s_Last_Update_Date+"*#*#*#"+s_Release_Date+"*#*#*#"+s_anchor+"*#*#*#"+s_type+"*#*#*#"+s_tag_count+"*#*#*#"+s_tag_length+"*#*#*#"+s_char_need
            
            #zrb_bern=query_raw(output_col_1)
            #print(sample_list_all)
            hdq_bern=query_raw(sample_single)
            #zrb_disease_str,zrb_disease_id_str,zrb_drug_str,zrb_drug_id_str,zrb_gene_str,zrb_gene_id_str=bern_list(zrb_bern)
            # zrb_bern_list=[zrb_disease_str,zrb_disease_id_str,zrb_drug_str,zrb_drug_id_str,zrb_gene_str,zrb_gene_id_str]
            # for i in zrb_bern_list:
            #     output_list.append(str(i))
            
            hdq_disease_str,hdq_disease_id_str,hdq_drug_str,hdq_drug_id_str,hdq_gene_str,hdq_gene_id_str=bern_list(hdq_bern)   
            hdq_bern_list=[hdq_disease_str,hdq_disease_id_str,hdq_drug_str,hdq_drug_id_str,hdq_gene_str,hdq_gene_id_str]

            test_disease=normalize.Normalize(hdq_disease_id_str)
            
            
            disease_output_id_disease_name_str,disease_output_disease_name_str=test_disease.disease()
            
            test_drug=normalize.Normalize(hdq_drug_id_str)
            drug_output_id_drug_name_str,drug_output_drug_name_str=test_drug.drug()
            test_gene=normalize.Normalize(hdq_gene_id_str)
            
            gene_output_id_gene_name_str,gene_output_gene_name_str=test_gene.gene()
            test_knock=normalize.Normalize(sample_single)
            
            knock_out_down,knock_in,knock,over=test_knock.knock_out()
            
            cell_line_text=normalize.Normalize(output_col_1)
            cell_line_text_str=cell_line_text.cell_line()
            
            cell_line_bern_text=normalize.Normalize(sample_single)
            cell_line_bern_text_str=cell_line_bern_text.cell_line()
            
            gsm_rrid=normalize.Normalize(s_number)
            gsm_rrid_cell_line,gsm_rrid_disease=gsm_rrid.rrid_gsm()
            
            
            hdq_bern_list=[hdq_disease_str,hdq_disease_id_str,disease_output_id_disease_name_str,disease_output_disease_name_str,hdq_drug_str,hdq_drug_id_str,drug_output_id_drug_name_str,drug_output_drug_name_str,hdq_gene_str,hdq_gene_id_str,gene_output_id_gene_name_str,gene_output_gene_name_str,knock_out_down,knock_in,knock,over,cell_line_text_str,cell_line_bern_text_str,gsm_rrid_cell_line,gsm_rrid_cell_line]
            for j in hdq_bern_list:
                output_list.append(str(j))
                #for i in output_list :
        
            
            # line='\t'.join(output_list)
            # line=line+'\n'
            # with open(output,"a",encoding='utf-8') as out:
            #     out.write(line)
            output_list=move_break(output_list)
            line='\t'.join(output_list)
            line=line+'\n'
            if append =='y':
                with open('gse_gsm_31_v2_out','a+',encoding='utf-8') as a:
                    a.write(line)            
            if geo=='gse':
                with open(output,"a",encoding='utf-8') as out:
                    out.write(line)
            #print(gse)
            

def _excutive_gse(gses, output):
    ## gses is a list containing GSE id
    num=0
    for gse in gses:
        geo=pd.read_table('gse_gsm_31_v2_out',low_memory=False,dtype=str)
        find_gse=geo[geo['gse'].isin([str(gse)])]
        find_gse_len=find_gse.shape[0]
        if find_gse_len>0:
            print("\n{} is in lookup table.".format(gse))
            if num ==0:
                find_gse.to_csv(output, sep='\t', mode='a',na_rep='null',index=False)
                num=num+1
            else:
                find_gse.to_csv(output, sep='\t', mode='a',na_rep='null',index=False,header=False)
      
        else:
                
            download_gse(gse)
            #pipeline(gse, output)
            print('\n it is going to connect to bern API.')
            pipeline(gse,output,append='y')
    
    my_file = Path("./output")
    if my_file.exists():
        os.remove('output')      
    # #删除文件夹
        # shutil.rmtree('gse') ## 不需要删除，每次下载的GSE文件可以存档以备复用。

def _excutive_gsm(gsms, output):
    ## gses is a list containing GSE id
    
    
    for gsm in gsms:
        num=0
        
        geo=pd.read_table('gse_gsm_31_v2_out',low_memory=False,dtype=str)
        find_gsm=geo[geo['gsm'].isin([str(gsm)])]
        find_gsm_len=find_gsm.shape[0]
        
        if find_gsm_len>0:
            
            print("\n{} is in lookup table.".format(gsm))
            path_gse_extract="./"+output    
            gse_file=Path(path_gse_extract)
            if gse_file.exists():
                find_gsm.to_csv(output, sep='\t', mode='a',na_rep='null',index=False,header=False)
            else:
                if num ==0:
                    find_gsm.to_csv(output, sep='\t', mode='a',na_rep='null',index=False)
                    num=num+1
                else:
                    find_gsm.to_csv(output, sep='\t', mode='a',na_rep='null',index=False,header=False)
        
        else:
            gse_gsm=normalize.Normalize(gsm)
            gse_gsm_list=gse_gsm.gsm_gse()
            #print(gse_gsm_list)
            try:
                for i in gse_gsm_list:
                    download_gse(i)
                    #pipeline(i, output)
                    print('\n it is going to connect to bern API.')
                    pipeline(i,output,append='y',geo='gsm')
                my_file = Path("./output")
                if my_file.exists():
                    #pass
                    os.remove('output')
                geo=pd.read_table('gse_gsm_31_v2_out',low_memory=False)
                find_gsm=geo[geo['gsm'].isin([str(gsm)])]
                find_gsm_len=find_gsm.shape[0]
                print("\nnow,{} is in lookup table.".format(gsm))
                path_gse_extract="./"+output    
                gse_file=Path(path_gse_extract)
                if gse_file.exists():
                    find_gsm.to_csv(output, sep='\t', mode='a',na_rep='null',index=False,header=False)
                else:
                    if find_gsm_len>0:
                        
                        if num ==0:
                            find_gsm.to_csv(output, sep='\t', mode='a',na_rep='null',index=False)
                            num=num+1
                        else:
                            find_gsm.to_csv(output, sep='\t', mode='a',na_rep='null',index=False,header=False)
                
                
                
                

            except:
                print("we can not download {} successfully".format(gsm))
            
            
            #print('gsm')
            # download_gse(gse)
            # pipeline(gse, output)

def main():
    try:
        parser = argparse.ArgumentParser(description="""parser pipeline for GEO datasets""")
        sub_parsers = parser.add_subparsers(help = "sub-command help", dest = "sub_command")
        gse_parser = sub_parsers.add_parser("gse",  help = "parse GSE samples",description = "parse new data from GEO by gse")
        gse_parser.add_argument('-ge', dest='gse_id', type=str, required = False, help='GSEid as input', action="append")
        gse_parser.add_argument('-o', dest='output', type=str, required = False, help='output file for parser result')

        gsm_parser = sub_parsers.add_parser("gsm",  help = "parse GSM sample",description = "parse new data from GEO by gsm id")
        gsm_parser.add_argument('-gm', dest='gsm_id', type=str, required = False, help='GSEid as input', action="append")
        gsm_parser.add_argument('-o', dest='output', type=str, required = False, help='output file for parser result')

        args = parser.parse_args()
        if args.sub_command == 'gse':
            gses, output = args.gse_id, args.output
            if not output:
                output = './gse_collection.txt'
            ## excute piepline
            _excutive_gse(gses = gses, output = output)
        if args.sub_command == 'gsm':
            gsms, output = args.gsm_id, args.output
            if not output:
                output = './gsm_collection.txt'
            _excutive_gsm(gsms = gsms, output = output)
        
    except KeyboardInterrupt:
        #郑荣斌师兄的代码，我这里没有，所以会报错
        sys.stderr.write("User interrupted me!\n")
        sys.exit(0)

if __name__ == '__main__':
    main()

        
#except:
#    print("bern connection breakdown")
    
