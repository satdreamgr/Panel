from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.config import getConfigListEntry, config
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.Button import Button
from SDG_ActionBox import SDG_ActionBox
from SDG_Deflate import SDG_Deflate
from SDG_Settings import SDG_Settings
from SDG_Common import TMP_IMPORT_PWD, TMP_SETTINGS_PWD
from urlparse import urlparse
import xml.etree.cElementTree
import httplib
import shutil
import os
import gettext
try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

class SDG_SettingsList(Screen):
	def __init__(self, session, list):
		Screen.__init__(self, session)

		self.session = session
		self.drawList = []
		self.list = list

		for entry in self.list:
			self.drawList.append(self.buildListEntry(entry[0], entry[1]))

		self["list"] = List(self.drawList)
		self["key_red"] = Button(_("Download"))
		self["key_green"] = Button("")
		self["key_yellow"] = Button("")
		self["key_blue"] = Button(_("Back"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
				{
					"ok": self.ok,
					"red": self.ok,
					#"green": self.green,
					"blue": self.quit,
					"cancel": self.quit,
				}, -2)

	def buildListEntry(self, sat, date):
		return((sat, date))

	def download(self):
		try:
			shutil.rmtree(TMP_IMPORT_PWD)
		except:
			pass

		os.mkdir(TMP_IMPORT_PWD)
		url = urlparse(self.url)
		try:
			conn = httplib.HTTPConnection(url.netloc)
			conn.request("GET", url.path)
			httpres = conn.getresponse()
			if httpres.status == 200:
				tmp = url.path.split("/")
				filename = TMP_IMPORT_PWD + "/" + tmp[len(tmp)-1]
				out = open(filename, "w")
				out.write(httpres.read())
				out.close()
				SDG_Deflate().deflate(filename)

			else:
				self.session.open(MessageBox, _("Cannot download settings (%s)") % self.url, MessageBox.TYPE_ERROR)
				return
		except Exception, e:
			print e
			self.session.open(MessageBox, _("Cannot download settings (%s)") % self.url, MessageBox.TYPE_ERROR)
			return

		settings = SDG_Settings()
		settings.apply()

		try:
			shutil.rmtree(TMP_SETTINGS_PWD)
		except Exception, e:
			print e

		try:
			shutil.rmtree(TMP_IMPORT_PWD)
		except Exception, e:
			print e

		self.session.open(MessageBox, _("Settings installed"), type = MessageBox.TYPE_INFO, timeout = 5)

	def ok(self):
		if len(self.list) == 0:
			return
		index = self["list"].getIndex()

		self.url = self.list[index][2]
		self.session.open(SDG_ActionBox, _("Downloading settings"), _("Downloading ..."), self.download)

	def quit(self):
		self.close()
