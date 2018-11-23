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
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Tools.BoundFunction import boundFunction
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
from requests.exceptions import *
from urllib2 import urlopen
import urllib2
from Screens.MessageBox import MessageBox 
import shutil
import gettext
FULLHD = False
if getDesktop(0).size().width() >= 1920:
    FULLHD = True

try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def getCameras():
	cameras = []
	with open('/usr/lib/enigma2/python/Plugins/Satdreamgr/PictureCamera/camera.txt','r') as f:
		for line in f:
			for name, url in [x.split("|") for x in line.splitlines()]:
				cameras.append((str(name), str(url)))
		return cameras

class PictureCamera(Screen):
	if FULLHD:
		skin = """
	<screen name="PictureCamera" flags="wfNoBorder" position="center,center" size="1920,1080" backgroundColor="transparent">
    <widget name="title" render="Label" position="40,30" size="1840,60" backgroundColor="#10000000" zPosition="5" font="Regular; 38" valign="center" halign="center" noWrap="1" foregroundColor="#00f47d19" />
	<widget name="menu" position="47,155" size="498,770" scrollbarMode="showOnDemand" halign="center" alphatest="on" backgroundColor="#10000000" font="Regular; 30" itemHeight="35"/>
	<eLabel name="" position="40,90" size="513,50" zPosition="-1" backgroundColor="#000064c7" />
	<eLabel name="" position="40,140" size="513,800" zPosition="-2" backgroundColor="#10000000" />
	<eLabel name="" position="40,940" size="513,50" zPosition="-1" backgroundColor="#000064c7" />
	<widget name="pic" position="557,94" size="1323,892" halign="center" alphatest="on" backgroundColor="#10000000"/>
	<eLabel name="" position="557,94" size="1323,892" zPosition="-1" backgroundColor="#10000000" />
	<eLabel name="" position="40,990" size="460,10" zPosition="2" backgroundColor="#00ff4a3c" />
    <eLabel name="" position="500,990" size="460,10" zPosition="2" backgroundColor="#00389416" />
    <eLabel name="" position="960,990" size="460,10" zPosition="2" backgroundColor="#00e5b243" />
    <eLabel name="" position="1420,990" size="460,10" zPosition="2" backgroundColor="#000064c7" />
    <eLabel text="Exit" position="40,1000" size="460,50" zPosition="5" font="Regular;32" halign="center" valign="center" transparent="0" foregroundColor="#00fefefe" backgroundColor="#10000000" />
    <eLabel text="Ok" position="500,1000" size="460,50" zPosition="5" font="Regular;32" halign="center" valign="center" transparent="0" foregroundColor="#00fefefe" backgroundColor="#10000000" />
    <widget name="download" position="960,1000" zPosition="5" size="460,50" font="Regular;32" halign="center" valign="center" transparent="0" foregroundColor="#00fefefe" backgroundColor="#10000000" />
    <eLabel text="Info" position="1420,1000" size="460,50" zPosition="5" font="Regular;32" halign="center" valign="center" transparent="0" foregroundColor="#00fefefe" backgroundColor="#10000000" />
    <eLabel name="" position="40,990" size="1840,60" zPosition="1" backgroundColor="#10000000" />
    <widget source="global.CurrentTime" render="Label" position="50,95" size="248,37" backgroundColor="#000064c7" transparent="1" font="Regular; 33" valign="center" halign="center" foregroundColor="#00fefefe" zPosition="2">
      <convert type="ClockToText">Format:%A</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="305,95" size="248,37" backgroundColor="#000064c7" transparent="1" font="Regular; 33" valign="center" halign="center" foregroundColor="#00fefefe" zPosition="2">
      <convert type="ClockToText">Format:%d-%m-%Y</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="140,940" size="165,52" backgroundColor="#000064c7" transparent="1" font="Regular; 48" halign="right" valign="center" zPosition="2" foregroundColor="#00fefefe">
      <convert type="ClockToText">Format:%-H:%M</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="300,947" size="67,30" font="Regular; 30" halign="left" valign="center" transparent="1" backgroundColor="#000064c7" foregroundColor="#00f47d19" zPosition="2">
      <convert type="ClockToText">Format: :%S</convert>
    </widget>
	 </screen>"""
	else:
		skin = """
	<screen name="PictureCamera" flags="wfNoBorder" position="center,center" size="1280,720" backgroundColor="transparent">
    <widget name="title" render="Label" position="40,30" size="1210,60" backgroundColor="#10000000" zPosition="5" font="Regular; 28" valign="center" halign="center" noWrap="1" foregroundColor="#00f47d19" />
	<widget name="menu" position="47,140" size="425,453" scrollbarMode="showOnDemand" halign="center" alphatest="on" backgroundColor="#10000000" font="Regular; 22"/>
	<eLabel name="" position="40,90" size="437,554" zPosition="-2" backgroundColor="#10000000" />
	<eLabel name="" position="40,90" size="437,35" zPosition="-1" backgroundColor="#000064c7" />
	<eLabel name="" position="40,609" size="437,35" zPosition="-1" backgroundColor="#000064c7" />
	<widget name="pic" position="480,93" size="770,548" halign="center" alphatest="on" backgroundColor="#10000000"/>
	<eLabel name="" position="480,93" size="770,548" zPosition="-1" backgroundColor="#10000000" />
	<eLabel name="" position="40,644" size="302,6" zPosition="2" backgroundColor="#00ff4a3c" />
    <eLabel name="" position="342,644" size="302,6" zPosition="2" backgroundColor="#00389416" />
    <eLabel name="" position="644,644" size="302,6" zPosition="2" backgroundColor="#00e5b243" />
    <eLabel name="" position="946,644" size="304,6" zPosition="2" backgroundColor="#000064c7" />
    <eLabel text="Exit" position="40,650" size="302,50" zPosition="5" font="Regular;22" halign="center" valign="center" transparent="1" foregroundColor="#00fefefe" backgroundColor="#10000000" />
    <eLabel text="Ok" position="342,650" size="302,50" zPosition="5" font="Regular;22" halign="center" valign="center" transparent="1" foregroundColor="#00fefefe" backgroundColor="#10000000" />
    <widget name="download" position="644,650" zPosition="5" size="302,50" font="Regular;22" halign="center" valign="center" transparent="1" foregroundColor="#00fefefe" backgroundColor="#10000000" />   
    <eLabel text="Info" position="946,650" size="302,50" zPosition="5" font="Regular;22" halign="center" valign="center" transparent="1" foregroundColor="#00fefefe" backgroundColor="#10000000" />
	 <eLabel name="" position="40,644" size="1210,60" zPosition="1" backgroundColor="#10000000" />
    <widget source="global.CurrentTime" render="Label" position="220,95" size="165,25" backgroundColor="#000064c7" transparent="1" font="Regular; 22" valign="center" halign="center" foregroundColor="#00fefefe" zPosition="2">
      <convert type="ClockToText">Format:%d-%m-%Y</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="50,95" size="165,25" backgroundColor="#000064c7" transparent="1" font="Regular; 22" valign="center" halign="center" foregroundColor="#00fefefe" zPosition="2">
      <convert type="ClockToText">Format:%A</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="140,609" size="110,35" backgroundColor="#000064c7" transparent="1" font="Regular; 32" halign="right" valign="center" zPosition="2" foregroundColor="#00fefefe">
      <convert type="ClockToText">Format:%-H:%M</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="247,614" size="45,20" font="Regular; 20" halign="left" valign="center" transparent="1" backgroundColor="#000064c7" foregroundColor="#00f47d19" zPosition="2">
      <convert type="ClockToText">Format: :%S</convert>
    </widget>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self['pic'] = Pixmap()
		self['title'] = Label(_("Picture Camera Plugin"))
		self['download'] = Label(_("Download List"))		
		self.cameraTimer = eTimer()
		self.cameraTimer.start(1)
		self.url = None
        	self["menu"] = MenuList(getCameras())
        	self["actions"] = ActionMap(["OkCancelActions", "WizardActions", "ColorActions"],{"cancel": self.close,"red": self.close,"ok": self.go,"green": self.go,"yellow": self.downloadList,"blue": self.info,}, -1)

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
		image = '/tmp/camera.jpg'
		if os.path.exists(image):
			sc = AVSwitch().getFramebufferScale()
			self.picloads = ePicLoad()
			self.picloads.PictureData.get().append(self.FinishDecode)
			self.picloads.setPara((
				self['pic'].instance.size().width(),
				self['pic'].instance.size().height(),
				sc[0], sc[1], False, 1, '#00000000'))
			self.picloads.startDecode(image)
			self.cameraTimer.start(60*1000)

	def FinishDecode(self, picInfo = None):
		ptr = self.picloads.getData()
		if ptr:
			self["pic"].instance.setPixmap(ptr.__deref__())
			del self.picloads
			os.remove('/tmp/camera.jpg')

	def downloadList(self):
		try:
			src = urllib2.urlopen('http://sgcpm.com/camera/camera.txt')
		except urllib2.HTTPError:
			self.session.open(MessageBox, _("Internet connection error !\nPlease check your internet connection !\n\n\nPress Exit... "), MessageBox.TYPE_ERROR)
			pass
		else:
			dst = open('/usr/lib/enigma2/python/Plugins/Satdreamgr/PictureCamera/camera.txt', 'w');
			shutil.copyfileobj(src, dst)
			self.session.open(MessageBox, _("Download done !\n\n\nPress Exit... "), MessageBox.TYPE_INFO)
			self.close(PictureCamera)

	def info(self):
		MyMessage = _("For Informations and Questions please refer to www.satdreamgr.com forum.\n")
		MyMessage += _("\n\n")
		MyMessage += _("PictureCamera is free.")
		self.session.open(MessageBox, MyMessage, MessageBox.TYPE_INFO)

def main(session,**kwargs):
    try:
     	session.open(PictureCamera)
    except:
        print "[Picture Camera] Pluginexecution failed"

def Plugins(**kwargs):
	return [PluginDescriptor(name=("Picture Camera"),
		description=("SatDreamGr Picture Camera Plugin"),
		icon="camera.png",
		where=PluginDescriptor.WHERE_PLUGINMENU,
		fnc=main)]
