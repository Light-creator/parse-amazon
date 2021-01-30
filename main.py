import sys, requests, csv, json
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from PyQt5 import QtCore, QtGui, QtWidgets
from parse import Ui_MainWindow

# Create
app = QtWidgets.QApplication(sys.argv)

# Init
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

#Logic
def write_csv(title, price, img):
	filename = ui.lineEdit_2.text() + ".csv"
	with open(filename, 'a', newline = '', encoding="utf-8") as f:
		wr = csv.writer(f, delimiter=';')
		wr.writerow([title, price, img])


def download_photo(url, path, name):
	try:
		urllib.request.urlretrieve(url, path + '/' + name)
		print("Скачивание файла: " + name)
	except:
		print("Скачивание файла не удалось: " + name)
	

def get_html(url):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x935')
	driver = webdriver.Chrome(chrome_options=options)
	driver.get(url)
	html = driver.page_source
	return html


def parse(html):
	path = 'D:/Python/parse-amazon/img'

	soup = bs(html, 'html.parser')
	blocks = soup.find("div", {'class':'s-main-slot'}).find_all('div', {'class':'s-result-item'})
	for block in blocks:
		try:
			title = block.find('h2', {'class':'a-size-mini'}).text
			title = title.replace('\n', '')
		except:
			title = ''
		try:
			price = block.find('span', {'class':'a-offscreen'}).text
		except:
			price = ''
		try: 
			img = block.find('img', {'class':'s-image'})['src']
			img_title = img.split('/')[-1]
		except:
			img = ''
			img_title = ''
		download_photo(img, path, img_title)
		write_csv(title, price, img_title)


def get_pages(html, url):
	soup = bs(html, 'html.parser')
	last_page = soup.find_all('li', {'class':'a-disabled'})[-1].text
	
	for i in range(2, int(last_page)+1):
		new_url = url + "&ref=sr_pg_" + str(i) 
		parse(get_html(new_url))


def main():

	filename = ui.lineEdit_2.text() + ".csv"
	with open(filename, 'w', newline = '', encoding="utf-8") as f:
		wr = csv.writer(f, delimiter=';')
		wr.writerow(['Title', 'Price', 'Img'])
	

	search = ui.lineEdit_2.text().split()
	string = ''

	for i in range(len(search)):
		if i != 0:
			string += '+' + search[i]
		else:
			string += search[i]

	url = 'https://www.amazon.com/s?k='+ string +'&crid=32IBWVIU2STIC&qid=1612018193&sprefix=phone+s%2Caps%2C253'
	
	get_pages(get_html(url), url)


ui.pushButton.clicked.connect(main)
sys.exit(app.exec_())