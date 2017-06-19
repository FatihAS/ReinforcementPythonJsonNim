import subprocess as sp
import json, time, random, os, sys
from copy import deepcopy
from operator import itemgetter
from random import randint


clear = lambda: os.system('cls')


def punyaAnak(data):
	punya = False;
	for i in range(0,len(data)):
		if data[i] > 2:
			punya = True
			break	
	return punya

def setChild(form,status):
	ret = []
	if status == 0:
		status = 1
	else:
		status = 0
	sibling_form = []
	for i in range(0,len(form)):
		for j in range(0,int(form[i]/2)):
			tmp_form = deepcopy(form)
			tmp_data = {}
			if tmp_form[i] - (j+1) == (j+1):
				continue
			else:
				tmp_form.append(j+1)
				tmp_form.append(tmp_form[i] - (j+1))
				del tmp_form[i]	
				tmp_form.sort(reverse=True)
				if tmp_form not in sibling_form:
					sibling_form.append(tmp_form)
					# print(tmp_form)
					if punyaAnak(tmp_form):
						tmp_data['x'] = 0.5	
					else:
						tmp_data['x'] = status
					tmp_data['form'] = deepcopy(tmp_form)
					tmp_data['child'] = setChild(tmp_form, status)
					ret.append(tmp_data)
	return ret


def createNimData(jumlah_batang):
	tmp_data = {}
	form = []
	form.append(jumlah_batang)	
	tmp_data['form'] = form
	tmp_data['x'] = 0.5
	tmp_data['child'] = setChild(form, 0);
	return tmp_data

def aiTurn(data,win_condition,explorasi,koefisien):
	index = 0
	if random.uniform(0, 1) <= explorasi:
		index = randint(0,len(data['child'])-1)
		data['x'] = data['x'] + koefisien*(data['child'][index]['x'] - data['x'])
	else:
		index_terbaik = 0
		for i in range(0,len(data['child'])):
			if i == 0:
				index_terbaik = i
			else:
				if win_condition == 1:
					if data['child'][i]['x'] > data['child'][index_terbaik]['x']:
						index_terbaik = i
				else:
					if data['child'][i]['x'] < data['child'][index_terbaik]['x']:
						index_terbaik = i

	return data['child'][index]

def userTurn(data, win_condition):
	print("biar gak error")


def play(data,explorasi,mode,jumlah_main,koefisien):
	turnPlayer = 1
	if mode == 1:
		mainke = 1
		while(jumlah_main >= mainke):
			tmp_data = data
			while(len(tmp_data["child"])>0):
				if turnPlayer == 1:
					tmp_data = aiTurn(tmp_data,1,explorasi,koefisien)
					turnPlayer = 2
				else:
					tmp_data = aiTurn(tmp_data,0,explorasi,koefisien)
					turnPlayer = 1
			mainke += 1
	else:
		return

def readFile(filename):
	file_content = "{}"
	try:
		with open(filename, 'r') as f:
			file_content = f.read()
			print ("read file " + filename)
		if not file_content:
			print ("no data in file " + filename)
	except IOError as e:
		print ("I/O error({0}): {1}".format(e.errno, e.strerror))
	except: #handle other exceptions such as attribute errors
		print ("Unexpected error:", sys.exc_info()[0])

	return file_content

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False


while True:
	clear()
	print("1. Buat baru")
	print("2. Dari file\n")
	mode_data = input('Sumber data : ')
	if mode_data in ["1","2"]:
		break
	else:
		clear()
		print("Input tidak diterima !!!\n")
filename = None
if mode_data == "2":
	while True:
		filename = input('Masukkan nama file : ')
		dataJson = readFile(filename)
		data = json.loads(dataJson)
		if len(data) < 1:
			print("data tidak valid")
		else:
			break
	# print(data['x'])
else:
	while True:
		jml_batang_s = input('Masukkan jumlah batang ( 5 <= N <= 15) : ')
		if RepresentsInt(jml_batang_s):
			jumlah_batang = int(jml_batang_s)
			if jumlah_batang < 5 or jumlah_batang > 15:
				print("Input tidak sesuai dengan batas")
			else:
				break
		else:
			print("Input harus berupa integer")
	start = time.time()
	data = createNimData(jumlah_batang)	
	end = time.time()
	print("Crate data success.\nRuntime : " + str(end - start) + " second")
	print("data : \n" + json.dumps(data))

while True:
	print("\n1. Human")
	print("2. AI\n")
	player1 = input("Masukkan jenis player 1 : ")
	if RepresentsInt(player1):
		player1 = int(player1)
		if player1 not in [1,2]:
			print("\nInput tidak sesuai")
		else:
			break
	else:
		print("\nInput harus berupa integer")

while True:
	print("\n1. Human")
	print("2. AI\n")
	player2 = input("Masukkan jenis player 2 : ")
	if RepresentsInt(player2):
		player2 = int(player2)
		if player2 not in [1,2]:
			print("\nInput tidak sesuai")
		else:
			break
	else:
		print("\nInput harus berupa integer")

if player1 == 2 and player2 == 2:
	mode = 1
	explorasi = None
	jumlah_experimen = None
	koefisien = None
	output_file = filename
	while True:
		if explorasi is None:
			explorasi = input("\nMasukkan persentase explorasi [0 - 1] : ")
			if RepresentsFloat(explorasi):
				explorasi = float(explorasi)
				if explorasi < 0 or explorasi > 1:
					print("\nInput harus berada diantara pada 0 <= N <= 1")
					explorasi = None
					continue
			else:
				explorasi = None
				print("\nInput harus berupa Float")
				continue
		if jumlah_experimen is None:
			jumlah_experimen = input("\nMasukkan jumlah experimen : ")
			if RepresentsInt(jumlah_experimen):
				jumlah_experimen = int(jumlah_experimen)
				if jumlah_experimen < 0:
					print("\nInput harus berupa bilangan positif")
					jumlah_experimen = None
					continue
			else:
				print("\nInput harus berupa integer")
				jumlah_experimen = None
				continue
		if koefisien is None:
			koefisien = input("\nMasukkan nilai koefisien [0 - 1] : ")
			if RepresentsFloat(koefisien):
				koefisien = float(koefisien)
				if koefisien < 0 or koefisien > 1:
					print("\nInput harus berada diantara pada 0 <= N <= 1")
					koefisien = None
					continue
			else:
				print("\nInput harus berupa float")
				koefisien = None
				continue
		if output_file is None:
			output_file = input("\nNama file output : ")
		if explorasi is not None and jumlah_experimen is not None and koefisien is not None is not output_file:
			break

elif player1 == 2 or player2 == 2:
	mode = 2
	jumlah_experimen = 1
	output_file = filename
	while True:
		belajar = input("\nAI tetap melakukan pembelajaran ? [y/n] : ")
		if belajar in ["y","Y"]:
			explorasi = input("Masukkan persentase explorasi [0 - 1] : ")
			if RepresentsFloat(explorasi):
				explorasi = float(explorasi)
				if explorasi < 0 or explorasi > 1:
					print("\nInput harus berada diantara pada 0 <= N <= 1")
				else:
					break
			else:
				print("\nInput harus berupa Float")
		elif belajar in ["n","N"]:
			explorasi = 0
			break
		else:
			print("\nInput harus berupa y or n")

# start = time.time()
# data = createNimData(7)	
# end = time.time()
play(data,explorasi,mode,jumlah_experimen,0.1)
if output_file is not None:
	orig_stdout = sys.stdout
	sys.stdout=open(output_file,'w')
	print(json.dumps(data))
	sys.stdout=orig_stdout
