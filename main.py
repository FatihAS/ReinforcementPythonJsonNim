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

def aiTurn(data,win_condition,explorasi,koefisien,print_gak):
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

	if print_gak == 1:
		print("\n")
		for i in range(0,len(data['child'])):
			print(str(i+1)+". ",end="")
			for j in range(0,len(data["child"][i]["form"])):
				print("  " + str(data["child"][i]["form"][j]) + "  ",end="")
			print("\t"+str(data["child"][i]['x']))

		print("\nAI memilih langkah ke " + str(index_terbaik+1))
	return data['child'][index]

def playerTurn(data, win_condition,player):
	print("\n")
	for i in range(0,len(data['child'])):
		print(str(i+1)+". ",end="")
		for j in range(0,len(data["child"][i]["form"])):
			print("  " + str(data["child"][i]["form"][j]) + "  ",end="")
		print("\t"+str(data["child"][i]['x']))

	while True:
		pilihan = input("\nPlayer "+ str(player) +"\nMasukkan langkah yang anda inginkan : ")
		if RepresentsInt(pilihan):
			pilihan = int(pilihan)
			if pilihan < 1 or pilihan > len(data['child']):
				print("Input tidak sesuai")
			else:
				break
		else:
			print("Input tidak berupa integer")

	return data['child'][pilihan-1]


def play(data,explorasi,jumlah_main,koefisien,player1,player2,print_gak):
	turnPlayer = 1
	
	mainke = 1
	while(jumlah_main >= mainke):
		tmp_data = data
		while(len(tmp_data["child"])>0):
			if print_gak == 1:
				print("\nKondisi saat ini")
				for i in range(0,len(tmp_data['form'])):
					print("  " + str(tmp_data['form'][i]) + "  ", end="")
				print("")
			if turnPlayer == 1:
				if player1 == 1:
					tmp_data = playerTurn(tmp_data,1,1)
				else:
					tmp_data = aiTurn(tmp_data,1,explorasi,koefisien,print_gak)
				turnPlayer = 2
			else:
				if player2 == 1:
					tmp_data = playerTurn(tmp_data,0,2)
				else:
					tmp_data = aiTurn(tmp_data,0,explorasi,koefisien,print_gak)
				turnPlayer = 1
		mainke += 1
	
	if turnPlayer == 2:
		return 1
	else:
		return 2

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
		print(dataJson)
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

print("\nPLAYER 1 PLAY FIRST")
while True:
	print("\n1. Human")
	print("2. AI\n")
	player1 = input("Masukkan jenis player 1 : ")
	if RepresentsInt(player1):
		player1 = int(player1)
		if player1 not in [1,2]:
			print("\nInput tidak sesuai")
		else:
			if player1 == 1:
				player1s = "Human"
			else:
				player1s = "AI"
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
			if player2 == 1:
				player2s = "Human"
			else:
				player2s = "AI"
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
		if output_file is None:
			output_file = input("\nNama file output : ")
			if output_file == "":
				output_file = None
				break
		if explorasi is not None and jumlah_experimen is not None and koefisien is not None is not output_file:
			break

elif player1 == 2 or player2 == 2:
	mode = 2
	jumlah_experimen = None
	koefisien = None
	belajar_lagi = None
	belajar = None
	output_file = filename
	explorasi = None
	koefisien_awal = None
	explorasi_awal = None
	while True:
		if belajar is None:
			belajar = input("\nAI melakukan pembelajaran dulu sebelum bermain ? [y/n] : ")
			if belajar not in ["y","Y","N","n"]:
				print("Input tidak sesuai")
				belajar = None
				continue
			else:
				if belajar in ["n","N"]:
					jumlah_experimen_awal = 1
					koefisien_awal = 0
					explorasi_awal = 0
		if jumlah_experimen is None and (belajar in ['y','Y'] or belajar_lagi in ['y','Y'] ):
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
		if koefisien is None and (belajar in ['y','Y'] or belajar_lagi in ['y','Y']):
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
		if explorasi is None and (belajar in ['y','Y'] or belajar_lagi in ['y','Y']):
			explorasi = input("\nMasukkan persentase explorasi [0-1] : ")
			if RepresentsFloat(explorasi):
				explorasi = float(explorasi)
				if explorasi < 0 or explorasi > 1:
					print("\nInput harus berada diantara pada 0 <= N <= 1")
					explorasi = None
					continue
		if belajar_lagi is None:
			belajar_lagi = input("\nAI tetap melakukan pembelajaran saat melawan user? [y/n] : ")
			if belajar_lagi not in ["y","Y","N","n"]:
				print("Input tidak sesuai")
				belajar_lagi = None
				continue
		if belajar is not None and belajar_lagi is not None:
			if jumlah_experimen is None:
				jumlah_experimen = jumlah_experimen_awal
			if explorasi is None:
				explorasi = 0
			if koefisien is None:
				koefisien = koefisien_awal
			if explorasi_awal is None:
				explorasi_awal = explorasi
			if koefisien_awal is None:
				koefisien_awal = koefisien
			break
else:
	mode = 2
	jumlah_experimen = 1
	koefisien = None
	explorasi = 0
	output_file = None


# start = time.time()
# data = createNimData(7)	
# end = time.time()
if jumlah_experimen > 1 and mode ==2:
	start = time.time()
	play(data,explorasi_awal,jumlah_experimen,koefisien_awal,2,2,0)
	end = time.time()
	while True:
		print(json.dumps(data))
		print("\nCreate data success.\nRuntime : " + str(end - start) + " second")
		pemenang = play(data,0,1,koefisien,player1,player2,1)
		print("\nGAME OVER")
		if pemenang == 1:
			pemenang_s = player1s
		else:
			pemenang_s = player2s
		print("Pemenang adalah player " + str(pemenang) + " : " +pemenang_s)
		while True:
			lagi = input("\nMain lagi ? [y/n] : ")
			if lagi in ['y','Y','n','N']:
				break
			else:
				print("\nInput tidak sesuai")
		if lagi in ['y','Y']:
			continue
		else:
			break
elif mode==1:
	play(data,explorasi,jumlah_experimen,koefisien,player1,player2,0)

if output_file is not None:
	orig_stdout = sys.stdout
	sys.stdout=open(output_file,'w')
	print(json.dumps(data))
	sys.stdout=orig_stdout