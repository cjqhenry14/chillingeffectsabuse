#!/usr/bin/python
import json
import os
from shutil import copyfile

'''
if doc has sent year and valid description, count[year]++ 
'''
year_count_dic = {}#<year, num>

def check_descrip_islegal(dmca, dir_name, json_doc):
	works = dmca['works']
	works_size = len(works)

	if(works_size == 0):
		return False;

	doc_desp = "";
	year = dmca['date_sent'].split('-')[0]
	if not (year == "2011" or  year == "2012" or year == "2013" or year == "2014"):
		return False;

	for i in range(0, works_size):
		cur_work = works[i];
		if('description' not in cur_work or cur_work['description'] == None):
			continue;

		doc_desp += cur_work['description'] + " ";

	#print doc_desp
	if len(doc_desp) > 100:
		#write
		desp_file = json_doc.split('.')[0] + ".txt"
		try:
			f = open("year_desp/" + year + "/" +  desp_file, 'w')
			f.write(doc_desp)
			f.close()
		except ValueError, e:
			os.system("rm year_desp/" + year + '/' + desp_file)
			return False;

		return True;
	else:
		return False;


def get_year_desp(dmca, dir_name, json_doc):
	if('date_sent' not in dmca or dmca['date_sent'] == None or check_descrip_islegal(dmca, dir_name, json_doc) == False):
		return;

	year = dmca['date_sent'].split('-')[0]

	dic_append(year)



#sender_name, principal_name, recipient_name
def analyze_each_file(dir_name, json_doc):
	global dmca_num, illegal_name_num
	json_data = open(dir_name + '/' + json_doc)

	try:
		data = json.load(json_data)
	except ValueError, e:
		return;

	if 'dmca' not in data:
		return;

	dmca = data['dmca'];
	#-----------------------
	get_year_desp(dmca, dir_name, json_doc);
	
	json_data.close();


#scan work dir to check each JSON document.
def scan_dir(dir_name):
	file_num = 0;
	i = 1
	file_list = os.listdir(dir_name)
	for json_doc in file_list:
		'''if(file_num == 20):
			break;'''
		#print json_doc
		analyze_each_file(dir_name, json_doc);
		file_num += 1;
		if file_num == i * 10000:
			print file_num
			i = i + 1

#=====================
def count_dic_traverse():
	global year_count_dic;
	for key in year_count_dic:
		print key, year_count_dic[key]


def dic_append(key):
	global year_count_dic;
	if(key not in year_count_dic):
		year_count_dic[key] = 1;
	else:
		year_count_dic[key] += 1;

def clean_year_desp_dir():
	os.system("rm -r year_desp/2011")
	os.system("rm -r year_desp/2012")
	os.system("rm -r year_desp/2013")
	os.system("rm -r year_desp/2014")
	os.system("mkdir year_desp/2011")
	os.system("mkdir year_desp/2012")
	os.system("mkdir year_desp/2013")
	os.system("mkdir year_desp/2014")



if (__name__ == '__main__'):

	clean_year_desp_dir()
	#scan_dir('../CE')
	scan_dir('../CE_10w')
	count_dic_traverse()



