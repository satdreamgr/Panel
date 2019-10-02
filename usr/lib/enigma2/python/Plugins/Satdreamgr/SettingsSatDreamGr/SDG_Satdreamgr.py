from Screens.MessageBox import MessageBox
from Components.config import config
from SDG_ActionBox import SDG_ActionBox
from SDG_Settings import SDG_Settings
from SDG_SettingsList import SDG_SettingsList
import xml.etree.cElementTree
import httplib
import os
import datetime
import gettext


try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass


SATDREAMGR_HOST = "sgcpm.com"
SATDREAMGR_PATH = "/enigma2/settings/"


class SDG_SatdreamgrHelper():

	def __init__(self, session):
		self.session = session

	def download(self):
		self.loaded = True
		self.list = []
		try:
			conn = httplib.HTTPConnection(SATDREAMGR_HOST)
			conn.request("GET", SATDREAMGR_PATH + "satdreamgr.xml")
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
						url = "http://" + SATDREAMGR_HOST + SATDREAMGR_PATH + node.get("filename")
						self.list.append([sat, date, url])
			else:
				self.session.open(MessageBox, _("Cannot download Cyrus list"), MessageBox.TYPE_ERROR)
				self.loaded = False
		except Exception, e:
			print e
			self.session.open(MessageBox, _("Cannot download Cyrus list"), MessageBox.TYPE_ERROR)
			self.loaded = False

	def load(self):
		self.session.openWithCallback(self.show, SDG_ActionBox, _("Downloading Cyrus list"), _("Downloading..."), self.download)

	def show(self, ret = None):
		if self.loaded:
			self.session.open(SDG_Satdreamgr, self.list)


class SDG_Satdreamgr(SDG_SettingsList):

	def __init__(self, session, list):
		SDG_SettingsList.__init__(self, session, list)
		self.skinName = "SDG_SettingsList"
		self.title = _("Cyrus settings")
