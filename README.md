 ### 测试代码
 
 python3 pipeline_web.py gse -ge GSE117702 -ge GSE101 -o 0406_01  ###备注：GSE117702(在查询表中) ，GSE101(不在查询表中)
 python3 pipeline_web.py gsm -gm GSM3307398 -gm GSM613385 -o 0406_02 ###备注：GSM3307398（在查询表里面，一个gsm对应一个gse) ，GSM613385（不在查询表里面，一个gsm对应两个gse）
 python3 pipeline_web.py gsm -gm GSM613385 gse -ge GSE117702 -o 0406_03 ###备注：测试一个gse，一个gsm  报错！！！
