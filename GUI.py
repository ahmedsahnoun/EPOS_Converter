from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QAction
from PyQt5.uic import loadUi
from OPI_ZVT_Converter import OPI_ZVT_Converter
from xml.etree import ElementTree as ET
from pyperclip import copy
import socket
import threading
import sys

class GUI():

	protocols = {}
	serverState = "off"
	converter = OPI_ZVT_Converter()
	app = QtWidgets.QApplication([])
	call = loadUi("./resources/g.ui")

	def __init__(self):
		self.initProtocols()
		self.setTheme("Light")
		
		tree = ET.parse('./resources/Lang.xml')
		root = tree.getroot()

		for child in root:
			language = QAction(child.tag,self.call)
			language.setIcon(QIcon(f'./resources/{child.tag}.png'))
			language.triggered.connect(lambda x, text = child.tag : self.setLanguage(text))
			self.call.menuLanguage.addAction(language)
		
		self.call.Host_IN.setPlainText(socket.gethostbyname("localhost"))
		self.call.Port_IN.setPlainText("1234")
		self.call.Host_OUT.setPlainText(socket.gethostbyname("localhost"))
		self.call.Port_OUT.setPlainText("1235")
		
		self.call.actionDark.triggered.connect(lambda x : self.setTheme("Dark"))
		self.call.actionLight.triggered.connect(lambda x : self.setTheme("Light"))
		self.call.ConvertButton.clicked.connect(self.convertText)
		self.call.BrowseButton.clicked.connect(self.getFile)
		self.call.ExportButton.clicked.connect(self.exportFile)
		self.call.CopyButton.clicked.connect(self.copy)
		self.call.LaunchButton.clicked.connect(self.convertSocket)
		self.call.Protocol_IN.currentTextChanged.connect(self.setProtocols)
		self.call.Protocol_OUT.currentTextChanged.connect(self.setConverter)
		self.app.aboutToQuit.connect(self.closing)

	def initProtocols(self):
		self.protocols = {
			"OPI" : ["ZVT","test2"],
			"test1" : ["test1","test2"],
		}
		keys = list(self.protocols.keys())
		self.call.Protocol_IN.addItems(keys)
		self.setProtocols()

	def setProtocols(self):
		self.call.Protocol_OUT.clear()
		self.call.Protocol_OUT.addItems(self.protocols[self.call.Protocol_IN.currentText()])
		self.setConverter()

	def setConverter(self):
		if self.call.Protocol_IN.currentText() == "OPI":
			if self.call.Protocol_OUT.currentText() == "ZVT":
				self.converter = OPI_ZVT_Converter()
			else:
				self.converter = None
		else:
			self.converter = None

	
	def convertText(self):
		data = self.call.input.toPlainText()
		self.call.output.setPlainText(self.converter.convert(data))

	def client(self, data):
		try:
			s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s2.connect((self.call.Host_OUT.toPlainText(),int(self.call.Port_OUT.toPlainText())))
			s2.send(data.encode("utf-8"))
		except socket.error as msg:
			print('Erreur: ',msg)
		finally:
			sys.exit()

	def server(self):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind((self.call.Host_IN.toPlainText(),int(self.call.Port_IN.toPlainText())))
		s.listen()
		while True:
			data = None
			clientScoket, address = s.accept()
			data = clientScoket.recv(1024).decode("utf-8")
			if data == "killsrv" and self.serverState == "off": 
				clientScoket.close()
				break
			if data != None:
				data = self.converter.convert(data)
				x2 = threading.Thread(target=self.client, args=(data,))
				x2.start()
		clientScoket.close()
		sys.exit()


	def convertSocket(self):
		if self.serverState == "off":
			self.serverState = "on"
			self.call.Led.setPixmap(QPixmap("./resources/on.png"))
			self.call.Host_IN.setDisabled(True)
			self.call.Port_IN.setDisabled(True)
			self.call.Host_OUT.setDisabled(True)
			self.call.Port_OUT.setDisabled(True)
			self.call.Protocol_IN.setDisabled(True)
			self.call.Protocol_OUT.setDisabled(True)
			x = threading.Thread(target=self.server)
			x.start()
		else:
			self.serverState = "off"
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((self.call.Host_IN.toPlainText(),int(self.call.Port_IN.toPlainText())))
			data = "killsrv"
			s.send(data.encode("utf-8"))
			self.call.Host_IN.setDisabled(False)
			self.call.Port_IN.setDisabled(False)
			self.call.Host_OUT.setDisabled(False)
			self.call.Port_OUT.setDisabled(False)
			self.call.Protocol_IN.setDisabled(False)
			self.call.Protocol_OUT.setDisabled(False)
			self.call.Led.setPixmap(QPixmap("./resources/off.png"))

	def getFile(self):
		filepath = QFileDialog.getOpenFileName()
		if filepath[0]:
			file = open(filepath[0],'r')
			v = file.read()
			self.call.input.setPlainText(v)
			file.close()

	def exportFile(self):
		filepath = QFileDialog.getSaveFileName()
		print(filepath[0])
		if filepath[0]:
			file = open(filepath[0],'w')
			text = self.call.output.toPlainText()
			file.write(text)
			file.close()

	def copy(self):
		text = self.call.output.toPlainText()
		copy(text)

	def setLanguage(self, language = "english"):
		tree = ET.parse('./resources/Lang.xml')
		root = tree.getroot().find(language)

		self.call.BrowseButton.setText(root.find('Browse').text)
		self.call.ConvertButton.setText(root.find('Convert').text)
		self.call.ExportButton.setText(root.find('Export').text)
		self.call.CopyButton.setText(root.find('Copy').text)
		self.call.menuLanguage.setTitle(root.find('Language').text)
		self.call.actionDark.setText(root.find('actionDark').text)
		self.call.actionLight.setText(root.find('actionLight').text)
		self.call.menuTheme.setTitle(root.find('menuTheme').text)
		self.call.TextConversion.setTitle(root.find('TextConversion').text)
		self.call.SocketConversion.setTitle(root.find('SocketConversion').text)
		self.call.LaunchButton.setText(root.find('LaunchButton').text)
		self.call.HostLabel_IN.setText(root.find('HostLabel').text)
		self.call.PortLabel_IN.setText(root.find('PortLabel').text)
		self.call.HostLabel_OUT.setText(root.find('HostLabel').text)
		self.call.PortLabel_OUT.setText(root.find('PortLabel').text)
		self.call.InputLabel.setText(root.find('InputLabel').text)
		self.call.OutputLabel.setText(root.find('OutputLabel').text)

	def setTheme(self,theme):
		sh=f"resources/{theme}.qss"
		with open(sh,"r") as f:
			self.call.setStyleSheet(f.read())
		f.close()

	def closing(self):
		if self.serverState == "on":
			self.convertSocket()

	def launchApp(self):
		self.call.show()
		self.app.exec()