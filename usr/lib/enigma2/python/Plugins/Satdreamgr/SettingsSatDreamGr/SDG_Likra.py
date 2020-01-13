from . import _
from Screens.MessageBox import MessageBox
from SDG_ActionBox import SDG_ActionBox
from SDG_SettingsList import SDG_SettingsList
import xml.etree.cElementTree
import httplib
import os


Likra_HOST = "sgcpm.com"
Likra_PATH = "/enigma2/likra/"


class SDG_LikraHelper():

	def __init__(self, session):
		self.session = session

	def download(self):
		self.loaded = True
		self.list = []
		try:
			conn = httplib.HTTPConnection(Likra_HOST)
			conn.request("GET", Likra_PATH + "lista.xml")
			httpres = conn.getresponse()
			if httpres.status == 200:
				mdom = xml.etree.cElementTree.parse(httpres)
				root = mdom.getroot()
				for node in root:
					if node.tag == "MAIN":
						sat = ""
						date = ""
						url = ""
						for x in node:
							if x.tag == "SAT":
								sat = x.text
							elif x.tag == "DATE":
								date = x.text
							elif x.tag == "URL":
								url = x.text
						self.list.append([sat, date, url])
			else:
				self.session.open(MessageBox, _("Cannot download %s settings list") % ("Likra"), MessageBox.TYPE_ERROR)
				self.loaded = False
		except Exception, e:
			print e
			self.session.open(MessageBox, _("Cannot download %s settings list") % ("Likra"), MessageBox.TYPE_ERROR)
			self.loaded = False

	def load(self):
		self.session.openWithCallback(self.show, SDG_ActionBox, _("Updating %s settings list") % ("Likra"), _("Downloading..."), self.download)

	def show(self, ret = None):
		if self.loaded:
			self.session.open(SDG_Likra, self.list)


class SDG_Likra(SDG_SettingsList):

	def __init__(self, session, list):
		SDG_SettingsList.__init__(self, session, list)
		self.skinName = "SDG_SettingsList"
		self.title = _("List of available %s settings") % ("Likra")
