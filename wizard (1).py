from PyQt4 import QtGui, QtCore 
import sys
import os
import smtplib 
from PyQt4.QtGui import *
import camera


class VarientWizard(QtGui.QWizard):
	def __init__(self, parent = None):
		super(VarientWizard, self).__init__(parent) 
		self.addPage(createIntroPage(self))
		self.addPage(createRegistrationPage(self))
		self.addPage(createConclusionPage(self))
		self.setWindowTitle("Apps") 
		
class createIntroPage(QtGui.QWizardPage):
	def __init__(self, parent=None):
		super(createIntroPage, self).__init__(parent)		

		self.setTitle("Virtual Apt Apps")

		self.label = QtGui.QLabel("Have Fun!")
			   
		self.label.setWordWrap(True)
		self.button = QtGui.QPushButton('Photo Booth') 
		self.button2 = QtGui.QPushButton('Minecraft') 
		self.button.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
		self.button2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')
		self.button.clicked.connect(self.handleButton) 
		self.button2.clicked.connect(self.minecraft) 
		self.button.setIcon(QtGui.QIcon('image1.jpg'))
		self.button.setIconSize(QtCore.QSize(130,130))	
		self.button2.setIcon(QtGui.QIcon('image1.jpg'))
		self.button2.setIconSize(QtCore.QSize(130,130))	
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.button) 
		layout.addWidget(self.button2)	 
		layout.addWidget(self.label)
		self.setLayout(layout)
		

	def handleButton(self): 
		global d
		d = camera.RunCamera()
		D_label = QtGui.QLabel(d) 
		D_label.hide()
		self.registerField("d", D_label)		

	def minecraft(self): 
		execfile('minecraft.py')

class createRegistrationPage(QtGui.QWizardPage): 	
	def __init__(self, parent = None):
		super(createRegistrationPage, self).__init__(parent)
	    	self.setTitle("Recieve your photo!")
	    	self.setSubTitle("Please fill both fields.")

		nameLabel = QtGui.QLabel("Name:")
		nameLineEdit = QtGui.QLineEdit()

	    	emailLabel = QtGui.QLabel("Email address:")
		emailLineEdit = QtGui.QLineEdit()
		
		self.registerField("Name*",nameLineEdit)
		self.registerField("Email*",emailLineEdit)		

		self.layout = QtGui.QGridLayout()

		self.layout.addWidget(nameLabel, 0, 0)
		self.layout.addWidget(nameLineEdit, 0, 1)
		self.layout.addWidget(emailLabel, 1, 0)
		self.layout.addWidget(emailLineEdit, 1, 1)
		self.setLayout(self.layout)

		d = self.field("d").toString()

	def initializePage(self):
		self.new_label = QLabel()
		self.pixmap = QPixmap("/home/pi/PiPictures/Image%s.jpg" % d)
		self.pixmap_resized = self.pixmap.scaled(350,350,QtCore.Qt.KeepAspectRatio)
		self.new_label.setPixmap(self.pixmap_resized)
		self.layout.addWidget(self.new_label,12,1)
		
	
class createConclusionPage(QtGui.QWizardPage):
	def __init__(self, parent = None):
		super(createConclusionPage, self).__init__(parent)
		self.setTitle("We hope you enjoy your lovely photo!")

		self.label = QtGui.QLabel("You are now successfully registered. Have a nice day!")
		self.label.setWordWrap(True)
		
		parent.button(QWizard.FinishButton).clicked.connect(self.SendMail)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.label)
		self.setLayout(layout)
		

	def SendMail(self): 

		from email.mime.image import MIMEImage
		from email.mime.text import MIMEText
		from email.mime.multipart import MIMEMultipart

		emailLineEdit = self.field("Email").toString()		
		print str(emailLineEdit)
		msg = MIMEMultipart()
		msg['Subject'] = 'Your Photo From Virtual Apt' 
		msg['From'] = 'justin.steinberg1@aol.com' 
		msg['To'] = str(emailLineEdit)

		text = MIMEText("Thank you for using the Virtual Apt Photo Booth! We Hope you had a great experience with us.") 
		msg.attach(text) 	
		img_data = open('/home/pi/PiPictures/Image%s.jpg' % d,'rb').read()
		img = MIMEImage(img_data,'jpg')
		msg.attach(img)

		s = smtplib.SMTP('smtp.gmail.com', '587')
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login('photo@virtualapt.com', 'ForJustin18')
		s.sendmail('photo@virtualapt.com', str(emailLineEdit), msg.as_string())
		s.quit()
		print "Email Successfully Send" 


if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)

	wizard = VarientWizard()
	wizard.setWindowTitle("Trivial Wizard")
	wizard.show()

	sys.exit(wizard.exec_())

