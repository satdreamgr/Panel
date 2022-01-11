from os import remove
from os.path import exists
import requests
from shutil import copyfileobj
try: #python3
	from urllib.error import HTTPError
	from urllib.request import urlopen
except: #python2
	from urllib2 import HTTPError, urlopen

from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from enigma import ePicLoad, eTimer
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS, resolveFilename

from . import _


def getCameras():
	cameras = []
	with open(resolveFilename(SCOPE_PLUGINS, "Satdreamgr/PictureCamera/camera.txt"), "r", encoding="UTF-8") as f:
		for line in f:
			for name, url in [x.split("|") for x in line.splitlines()]:
				cameras.append((str(name), str(url)))
		return cameras


class PictureCamera(Screen):

	skin = """
		<screen name="PictureCamera" title="Picture camera" position="center,center" size="640,480">
			<widget name="menu" position="10,10" size="190,380" font="Regular;20" scrollbarMode="showOnDemand"/>
			<widget name="pic" position="210,10" size="420,380" halign="center"/>
			<ePixmap pixmap="buttons/key_red.png" position="10,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="buttons/key_green.png" position="165,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="buttons/key_yellow.png" position="320,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="buttons/key_blue.png" position="475,442" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_yellow" position="355,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_blue" position="510,440" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
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
		print("[Camera] download")
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
		if exists(image):
			sc = AVSwitch().getFramebufferScale()
			self.picloads = ePicLoad()
			self.picloads.PictureData.get().append(self.FinishDecode)
			self.picloads.setPara((
				self["pic"].instance.size().width(),
				self["pic"].instance.size().height(),
				sc[0], sc[1], False, 1, "#00000000"))
			self.picloads.startDecode(image)
			self.cameraTimer.start(60 * 1000)

	def FinishDecode(self, picInfo=None):
		ptr = self.picloads.getData()
		if ptr:
			self["pic"].instance.setPixmap(ptr.__deref__())
			del self.picloads
			remove("/tmp/camera.jpg")

	def downloadList(self):
		try:
			src = urlopen("http://sgcpm.com/camera/camera.txt")
		except HTTPError:
			self.session.open(MessageBox, _("Internet connection error! Please check your internet connection!"), MessageBox.TYPE_ERROR)
			pass
		else:
			dst = open(resolveFilename(SCOPE_PLUGINS, "Satdreamgr/PictureCamera/camera.txt"), "w")
			copyfileobj(src, dst)
			self.session.open(MessageBox, _("Download completed!"), MessageBox.TYPE_INFO)
			self.close(PictureCamera)

	def info(self):
		MyMessage = _("For information or questions please refer to the www.satdreamgr.com forum.")
		MyMessage += "\n\n"
		MyMessage += _("Picture camera is free.")
		self.session.open(MessageBox, MyMessage, MessageBox.TYPE_INFO)


def main(session, **kwargs):
	session.open(PictureCamera)


def Plugins(**kwargs):
	return PluginDescriptor(name=_("Picture camera"), description=_("SatDreamGr picture camera plugin"), icon="camera.png", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)
