##
## Picture Camera Plugin
## SatDreamGr Team
## www.satdreamgr.com
##
import os, urllib
import requests
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from enigma import ePicLoad, eTimer, getDesktop
from Components.AVSwitch import AVSwitch
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Tools.BoundFunction import boundFunction
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
from requests.exceptions import *
from urllib2 import urlopen
import urllib2
import shutil
import gettext

try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def main(session, **kwargs):
	try:
		session.open(PictureCamera)
	except:
		print "[Picture Camera] Plugin execution failed"

def Plugins(**kwargs):
	return [PluginDescriptor(name=("Picture camera"),
		description=("SatDreamGr picture camera plugin"),
		icon="camera.png",
		where=PluginDescriptor.WHERE_PLUGINMENU,
		fnc=main)]

def getCameras():
	cameras = []
	with open('/usr/lib/enigma2/python/Plugins/Satdreamgr/PictureCamera/camera.txt','r') as f:
		for line in f:
			for name, url in [x.split("|") for x in line.splitlines()]:
				cameras.append((str(name), str(url)))
		return cameras

class PictureCamera(Screen):

	skin = """
		<screen name="PictureCamera" title="Picture camera" position="center,center" size="640,480">
			<widget name="menu" position="10,10" size="190,380" font="Regular;20" scrollbarMode="showOnDemand"/>
			<widget name="pic" position="210,10" size="420,380" halign="center"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="10,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="165,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/yellow.png" position="320,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/blue.png" position="475,442" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_yellow" position="355,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_blue" position="510,440" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("Picture camera"))
		self.cameraTimer = eTimer()
		self.cameraTimer.start(1)
		self.url = None
		self["menu"] = MenuList(getCameras())
		self["pic"] = Pixmap()
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Select"))
		self["key_yellow"] = Label(_("Refresh list"))
		self["key_blue"] = Label(_("Info"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.close,
				"red": self.close,
				"ok": self.go,
				"green": self.go,
				"yellow": self.downloadList,
				"blue": self.info,
			}, -1)

	def go(self):
		if self["menu"].l.getCurrentSelection():
			self.url = self["menu"].l.getCurrentSelection()[1]
		self.download()

	def download(self):
		self.cameraTimer.timeout.callback.append(self.download)
		print "[Camera] download"
		self.cameraTimer.stop()
		if not self.url:
			return
		try:
			r = requests.get(self.url, timeout=30)
			if r.status_code == 200:
				open("/tmp/camera.jpg", "wb").write(r.content)
				self.downloadFinished(None)
		except:
			pass

	def downloadFinished(self, result):
		image = "/tmp/camera.jpg"
		if os.path.exists(image):
			sc = AVSwitch().getFramebufferScale()
			self.picloads = ePicLoad()
			self.picloads.PictureData.get().append(self.FinishDecode)
			self.picloads.setPara((
				self["pic"].instance.size().width(),
				self["pic"].instance.size().height(),
				sc[0], sc[1], False, 1, "#00000000"))
			self.picloads.startDecode(image)
			self.cameraTimer.start(60*1000)

	def FinishDecode(self, picInfo = None):
		ptr = self.picloads.getData()
		if ptr:
			self["pic"].instance.setPixmap(ptr.__deref__())
			del self.picloads
			os.remove("/tmp/camera.jpg")

	def downloadList(self):
		try:
			src = urllib2.urlopen("http://sgcpm.com/camera/camera.txt")
		except urllib2.HTTPError:
			self.session.open(MessageBox, _("Internet connection error!\nPlease check your internet connection!\n\nPress exit..."), MessageBox.TYPE_ERROR)
			pass
		else:
			dst = open("/usr/lib/enigma2/python/Plugins/Satdreamgr/PictureCamera/camera.txt", "w");
			shutil.copyfileobj(src, dst)
			self.session.open(MessageBox, _("Download completed!\n\nPress exit..."), MessageBox.TYPE_INFO)
			self.close(PictureCamera)

	def info(self):
		MyMessage = _("For information or questions please refer to www.satdreamgr.com forum.")
		MyMessage += "\n\n"
		MyMessage += _("Picture camera is free.")
		self.session.open(MessageBox, MyMessage, MessageBox.TYPE_INFO)
