import time
import getpass
from tqdm.auto import tqdm
import sqlite3
import pyzbar.pyzbar as pyzbar
import pyqrcode
import cv2
import os
import numpy
import colorama
from colorama import Back, Style
colorama.init(autoreset=True)
#------ScanningFromWebCamera---------------------
def scan():
	i = 0
	cap = cv2.VideoCapture(0)
	font = cv2.FONT_HERSHEY_PLAIN
	while i<1:
		ret,frame=cap.read()
		decode = pyzbar.decode(frame)
		for obj in decode:
			name=obj.data
			name2= name.decode()
			nn,ii,pp,dd = name2.split(' ')
			db = sqlite3.connect('StudentDatabase.db')
			c = db.cursor()
			c.execute('''CREATE TABLE IF NOT EXISTS Record(name TEXT, iid TEXT,phone_no TEXT, dept TEXT, TimeofMArk TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
			c.execute("INSERT INTO Record(name, iid, phone_no, dept) VALUES (?,?,?,?)", (nn,ii,pp,dd))
			db.commit()

#database portions--------------------------------
			i=i+1
		cv2.imshow("QRCode",frame)
		cv2.waitKey(2)
		cv2.destroyAllWindows

#------CreateDatabaseForeStudent------------------
def database():
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS all_record(student_name TEXT, student_id TEXT, student_contact, student_department TEXT)")
	conn.commit()
	conn.close()
database()

#------AddingNewStudent---------------------
def add_User():
	Li = []
	S_name=str(input("Please Enter Student Name\n"))
	S_id=str(input("Please Enter Student Id\n"))
	S_contac= input("Please enter Student Contact No\n")
	S_dept= input("Please enter Student Department\n")
	Li.extend((S_name,S_id,S_contac,S_dept))
#-----using List Compression to convert a list to str--------------
	listToStr = ' '.join([str(elem) for elem in Li])
	#print(listToStr)
	print(Back.YELLOW + "Please Verify the Information")
	print("Student Name       = "+ S_name)
	print("Student ID         = "+ S_id)
	print("Student Contact    = "+ S_contac)
	print("Student Department = "+ S_dept)
	input("Press Enter to continue or CTRL+C to Break Operation")
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("INSERT INTO all_record(student_name, student_id, student_contact, student_department) VALUES (?,?,?,?)", (S_name,S_id,S_contac,S_dept))
	conn.commit()
	conn.close()
	qr= pyqrcode.create(listToStr)
	if not os.path.exists('./QrCodes'):
		os.makedirs('./QRCodes')
	qr.png("./QRCodes/" +S_name+ ".png",scale=8)
#--------------ViewDatabase------------------------
def viewdata():
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Record")
	rows = c.fetchall()
	for row in rows:
		print(row)
	conn.close()
#----------AdminScreen-----------------------
def afterlogin():
	print("+------------------------------+")
	print("|  1- Add New Students         |")
	print("|  2- Veiw Record              |")
	print("+------------------------------+")
	user_input = input("")
	if user_input == '1':
		add_User()
	if user_input == '2':
		viewdata()

#Login--------------------------------------
def login():
	print(Back.GREEN+ 'Please Enter Password :')
	print(Back.GREEN+"QR Code Attendace System")
	password = getpass.getpass()
	if password =='password':
		for i in tqdm(range(4000)):
			print("",end='\r')
		print("------------------------------------------------------------------------------------------------------------------------")
		print(Back.CYAN+"QR Code Attendace System")
		afterlogin()
	if password != 'password':
		print("Invalid Password")
		login()



#-------MainPage----------------------------
def markattendance():
	print("+------------------------------+")
	print("|  1- Mark Attendance          |")
	print("|  2- Admin Login              |")
	print("+------------------------------+")
	user_input2 = input("")
	if user_input2== '1':
		scan()
	if user_input2 == '2':
		login()
markattendance()