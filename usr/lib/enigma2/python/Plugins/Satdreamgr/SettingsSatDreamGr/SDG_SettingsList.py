from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.config import config
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.Button import Button
from SDG_ActionBox import SDG_ActionBox
from SDG_Deflate import SDG_Deflate
from SDG_Settings import SDG_Settings
from SDG_Common import TMP_IMPORT_PWD, TMP_SETTINGS_PWD
from urlparse import urlparse
import httplib
import shutil
import os
import gettext


try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass


class SDG_SettingsList(Screen):

	skin = """
		<screen name="SDG_SettingsList" position="center,center" size="600,405">
			<widget source="list" render="Listbox" position="10,10" size="580,350" scrollbarMode="showOnDemand" transparent="1">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryText(pos = (10, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 0),
						MultiContentEntryText(pos = (450, 5), size = (120, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						],
						"fonts": [gFont("Regular", 20)],
						"itemHeight": 35
					}
				</convert>
			</widget>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="10,372" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="165,372" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,370" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,370" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session, list):
		Screen.__init__(self, session)

		self.session = session
		self.drawList = []
		self.list = list

		for entry in self.list:
			self.drawList.append(self.buildListEntry(entry[0], entry[1]))

		self["list"] = List(self.drawList)
		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Download"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
				{
					"ok": self.ok,
					"cancel": self.quit,
					"red": self.quit,
					"green": self.ok,
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
				filename = TMP_IMPORT_PWD + "/" + tmp[len(tmp) - 1]
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

		self.session.open(MessageBox, _("Settings list installed successfully"), type=MessageBox.TYPE_INFO, timeout=5)

	def ok(self):
		if len(self.list) == 0:
			return
		index = self["list"].getIndex()

		self.url = self.list[index][2]
		self.session.open(SDG_ActionBox, _("Updating settings list"), _("Downloading..."), self.download)

	def quit(self):
		self.close()
