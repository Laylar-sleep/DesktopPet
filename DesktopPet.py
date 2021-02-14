'''
Reference:
	Charles
'''
import os
import cfg
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
from PyQt5 import QtWidgets, QtGui


class DesktopPet(QWidget):
	def __init__(self, parent=None, **kwargs):
		super(DesktopPet, self).__init__(parent)
		# initialize
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
		self.setAutoFillBackground(False)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.repaint()
		self.pet_images, iconpath = self.LoadPetImages()
		# quit
		quit_action = QAction('退出', self, triggered=self.quit)
		quit_action.setIcon(QIcon(iconpath))
		self.tray_icon_menu = QMenu(self)
		self.tray_icon_menu.addAction(quit_action)
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(QIcon(iconpath))
		self.tray_icon.setContextMenu(self.tray_icon_menu)
		self.tray_icon.show()
		# initial image
		self.image = QLabel(self)
		self.setImage(self.pet_images[0][0])
		self.is_follow_mouse = False
		# right click
		self.is_right_click = False
		# mouse position when moving
		self.mouse_drag_pos = self.pos()
		# display
		self.resize(128, 128)
		self.randomPosition()
		self.show()
		# initalize attributes
		self.is_running_action = False
		self.action_images = []
		self.action_pointer = 0
		self.action_max_len = 0
		# timeout replay
		# self.timer = QTimer()
		# self.timer.timeout.connect(self.randomAct)
		# self.timer.start(500)

	'''random pet action'''
	def randomAct(self):
		if not self.is_running_action:
			self.is_running_action = True
			self.action_images = random.choice(self.pet_images)
			self.action_max_len = len(self.action_images)
			self.action_pointer = 0
		for i in range(0,self.action_max_len+1):
			if self.action_pointer == self.action_max_len:
				self.is_running_action = False
				self.action_pointer = 0
				self.action_max_len = 0
				self.setImage(self.pet_images[0][0])

			self.setImage(self.action_images[self.action_pointer])
			self.action_pointer += 1
			time.sleep(0.2)
			print(i,self.action_max_len)

	'''set current image'''
	def setImage(self, image):
		self.image.setPixmap(QPixmap.fromImage(image))

	'''load all the pics'''
	def LoadPetImages(self):
		# pet_name = cfg.PET_ACTIONS_MAP.keys()
		actions = cfg.ACTION_DISTRIBUTION
		pet_images = []
		for action in actions:
			pet_images.append([self.loadImage(os.path.join(cfg.ROOT_DIR, 'pet_39', 'shime'+item+'.png')) for item in action])
		iconpath = os.path.join(cfg.ROOT_DIR, 'pet_39', 'shime1.png')
		return pet_images, iconpath

	'''bind mouse and pet position '''
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.is_follow_mouse = True
			self.mouse_drag_pos = event.globalPos() - self.pos()
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))
		elif event.button() == Qt.RightButton:
			self.loadAct()
			event.accept()

	'''sync mouse position and pet position'''
	def mouseMoveEvent(self, event):
		if Qt.LeftButton and self.is_follow_mouse:
			self.move(event.globalPos() - self.mouse_drag_pos)
			event.accept()

	'''left release, unbind'''
	def mouseReleaseEvent(self, event):
		self.is_follow_mouse = False
		self.setCursor(QCursor(Qt.ArrowCursor))

	'''Right Click, run an action'''
	def loadAct(self):
		self.is_running_action = True
		self.action_images = random.choice(self.pet_images)
		self.action_max_len = len(self.action_images)
		self.action_pointer = 0

		for i in range(0, self.action_max_len + 1):
			if self.action_pointer == self.action_max_len:
				self.is_running_action = False
				self.action_pointer = 0
				self.action_max_len = 0
				self.setImage(self.pet_images[0][0])

			self.setImage(self.action_images[self.action_pointer])
			self.action_pointer += 1
			time.sleep(0.2)


	'''load image'''
	def loadImage(self, imagepath):
		image = QImage()
		image.load(imagepath)
		return image

	'''initialize the position'''
	def randomPosition(self):
		screen_geo = QDesktopWidget().screenGeometry()
		pet_geo = self.geometry()
		width = (screen_geo.width() - pet_geo.width()) * random.random()
		height = (screen_geo.height() - pet_geo.height()) * random.random()
		self.move(width, height)

	'''exit'''
	def quit(self):
		self.close()
		sys.exit()


'''run'''
if __name__ == '__main__':
	app = QApplication(sys.argv)
	pet = DesktopPet()
	sys.exit(app.exec_())