from . import _
from Screens.MessageBox import MessageBox
from SDG_ActionBox import SDG_ActionBox
from SDG_SettingsList import SDG_SettingsList
import xml.etree.cElementTree
import httplib
import os
import datetime


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
						#print date[:4]
						#print date[4:6]
						#print date[-2:]
						date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
						date = date.strftime("%d %b")
						url = "http://" + SATVENUS_HOST + SATVENUS_PATH + node.get("filename")
						self.list.append([sat, date, url])
			else:
				self.session.open(MessageBox, _("Cannot download %s settings list") % ("Satvenus"), MessageBox.TYPE_ERROR)
				self.loaded = False
		except Exception, e:
			print e
			self.session.open(MessageBox, _("Cannot download %s settings list") % ("Satvenus"), MessageBox.TYPE_ERROR)
			self.loaded = False

	def load(self):
		self.session.openWithCallback(self.show, SDG_ActionBox, _("Updating %s settings list") % ("Satvenus"), _("Downloading..."), self.download)

	def show(self, ret = None):
		if self.loaded:
			self.session.open(SDG_Satvenus, self.list)


class SDG_Satvenus(SDG_SettingsList):

	def __init__(self, session, list):
		SDG_SettingsList.__init__(self, session, list)
		self.skinName = "SDG_SettingsList"
		self.title = _("List of available %s settings") % ("Satvenus")
