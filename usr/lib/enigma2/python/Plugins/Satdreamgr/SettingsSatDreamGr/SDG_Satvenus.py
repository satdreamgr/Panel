from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.config import getConfigListEntry, config
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from SDG_ActionBox import SDG_ActionBox
from SDG_Deflate import SDG_Deflate
from SDG_Settings import SDG_Settings
from SDG_SettingsList import SDG_SettingsList
from SDG_Common import TMP_IMPORT_PWD, TMP_SETTINGS_PWD
from urlparse import urlparse
import xml.etree.cElementTree
import httplib
import shutil
import os
import datetime
import gettext
try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

SATVENUS_HOST = "venuscs.net"
SATVENUS_PATH = "/SatDreamGr/milenko61/"

class SDG_SatvenusHelper():
	def __init__(self, session):
		self.session = session

	def download(self):
		self.loaded = True
		self.list = []
		try:
			conn = httplib.HTTPConnection(SATVENUS_HOST)
			conn.request("GET", SATVENUS_PATH + "milenko61.xml")
			httpres = conn.getresponse()
			if httpres.status == 200:
				mdom = xml.etree.cElementTree.parse(httpres)
				root = mdom.getroot()
				for node in root:
					if node.tag == "package":
						sat = node.text
						date = node.get("date")
						print date[:4]
						print date[4:6]
						print date[-2:]
						date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
						date = date.strftime("%d %b")
						url = "http://" + SATVENUS_HOST + SATVENUS_PATH + node.get("filename")
						self.list.append([sat, date, url])
			else:
				self.session.open(MessageBox, _("Cannot download Satvenus list"), MessageBox.TYPE_ERROR)
				self.loaded = False
		except Exception, e:
			print e
			self.session.open(MessageBox, _("Cannot download Satvenus list"), MessageBox.TYPE_ERROR)
			self.loaded = False

	def load(self):
		self.session.openWithCallback(self.show, SDG_ActionBox, _("Downloading Satvenus list"), _("Downloading ..."), self.download)

	def show(self, ret = None):
		if self.loaded:
			self.session.open(SDG_Satvenus, self.list)

Satvenus_main = """<screen name="SDG_Satvenus" position="center,center" size="600,405" title="Satvenus list" >
			<widget source="list" render="Listbox" position="10,10" size="580,330" scrollbarMode="showOnDemand" transparent="1" >
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryText(pos = (10, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 0),
						MultiContentEntryText(pos = (450, 5), size = (120, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						],
						"fonts": [gFont("Regular", 22)],
						"itemHeight": 40
					}
				</convert>
			</widget>	
                   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/key_exit.png" position="80,360" size="40,32" zPosition="1" alphatest="blend"/>
                   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/key_ok.png" position="240,360" size="40,32" zPosition="1" alphatest="blend"/>                   
                   </screen>""" 

class SDG_Satvenus(SDG_SettingsList):
	def __init__(self, session, list):
		SDG_SettingsList.__init__(self, session, list)
		self.skin = Satvenus_main	
