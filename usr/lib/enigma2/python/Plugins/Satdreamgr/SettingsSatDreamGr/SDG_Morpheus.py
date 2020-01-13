from . import _
from Screens.MessageBox import MessageBox
from SDG_ActionBox import SDG_ActionBox
from SDG_SettingsList import SDG_SettingsList
import xml.etree.cElementTree
import httplib
import os
import datetime


MORPHEUS_HOST = "openee.sifteam.eu"
MORPHEUS_PATH = "/settings/morph883/"


class SDG_MorpheusHelper():

	def __init__(self, session):
		self.session = session

	def download(self):
		self.loaded = True
		self.list = []
		try:
			conn = httplib.HTTPConnection(MORPHEUS_HOST)
			conn.request("GET", MORPHEUS_PATH + "morph883.xml")
			httpres = conn.getresponse()
			if httpres.status == 200:
				mdom = xml.etree.cElementTree.parse(httpres)
				root = mdom.getroot()
				for node in root:
					if node.tag == "package":
						sat = node.text
						date = node.get("date")
						#print date[:4]
						#print date[4:6]
						#print date[-2:]
						date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
						date = date.strftime("%d %b")
						url = "http://" + MORPHEUS_HOST + MORPHEUS_PATH + node.get("filename")
						self.list.append([sat, date, url])
			else:
				self.session.open(MessageBox, _("Cannot download %s settings list") % ("morpheus883"), MessageBox.TYPE_ERROR)
				self.loaded = False
		except Exception, e:
			print e
			self.session.open(MessageBox, _("Cannot download %s settings list") % ("morpheus883"), MessageBox.TYPE_ERROR)
			self.loaded = False

	def load(self):
		self.session.openWithCallback(self.show, SDG_ActionBox, _("Updating %s settings list") % ("morpheus883"), _("Downloading..."), self.download)

	def show(self, ret = None):
		if self.loaded:
			self.session.open(SDG_Morpheus, self.list)


class SDG_Morpheus(SDG_SettingsList):

	def __init__(self, session, list):
		SDG_SettingsList.__init__(self, session, list)
		self.skinName = "SDG_SettingsList"
		self.title = _("List of available %s settings") % ("morpheus883")
