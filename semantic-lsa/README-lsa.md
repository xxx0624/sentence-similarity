#LSA

##Tips:
1. 此LSA主要针对corpus中的msr数据格式的LSA
corpus格式如下：
1/0	sentence1-id	sentence2-id	sentence1	sentence2(split by 'tab')
2. 套用其他corpus主要修改以下几处：
	2.1 get_documents中导入的是为LSA准备的corpus且只导入了每一个样例的sentence也就是一行中的sentence1和sentence2中的sentence1
	2.2 get_documents忽略了msr corpus的第一行
	2.3 lsa训练完成后，在main函数中sentence最好预处理一次

##Results
if threhold == 0.40, the precision is about 87.4386% (by msr-train)
			== 0.39, 						87.4141% (by msr-train)
			== 0.41, 						85.5598% (by msr-tarin)