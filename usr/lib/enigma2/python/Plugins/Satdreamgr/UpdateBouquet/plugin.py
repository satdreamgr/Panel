from . import _
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
#from os import path
import os, urllib


url_sc = "/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/update.sh"
GSXML = "/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml"
GSBQ = "/etc/enigma2/userbouquet.greekstreamtv.tv"


def main(session, **kwargs):
	try:
		session.open(UpdateBouquet)
	except:
		print "[UpdateBouquet] Plugin execution failed"


def autostart(reason, **kwargs):
	if reason == 0:
		print "[UpdateBouquet] no autostart"


def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("GreekStreamTV in bouquets"), main, "update_setup", 45)]
	return []


def Plugins(**kwargs):
	return PluginDescriptor(name = _("GreekStreamTV in bouquets"), description = _("Update bouquet list"), where = PluginDescriptor.WHERE_MENU, fnc = menu)


class UpdateBouquet(Screen):

	skin = """
		<screen name="UpdateBouquet" title="GreekStreamTV in bouquets" position="center,center" size="600,405">
			<widget name="menu" itemHeight="35" position="10,10" size="580,300" scrollbarMode="showOnDemand"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="10,372" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="165,372" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/blue.png" position="320,372" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,370" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,370" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_blue" position="355,370" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("GreekStreamTV in bouquets"))
		menu = []

		if os.path.isdir("/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet"):
			menu.append((_("Create bouquets list"), "create"))
			menu.append((_("Download & update bouquets list"), "updatebq"))
			self["menu"] = MenuList(menu)

			self["key_red"] = Label(_("Exit"))
			self["key_green"] = Label(_("Select"))
			self["key_blue"] = Label(_("Info"))
			self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"ok": self.go,
				"cancel": self.close,
				"red": self.close,
				"green": self.go,
				"blue": self.showInfo,
			}, -1)

	def go(self):
		if self["menu"].l.getCurrentSelection() is not None:
			choice = self["menu"].l.getCurrentSelection()[1]

		if choice == "create":
			self.session.openWithCallback(self.create, MessageBox, _("Confirm your selection?"), MessageBox.TYPE_YESNO)

		elif choice == "updatebq":
			try:
				url = "http://sgcpm.com/livestream/stream.xml"
				f = urllib.urlopen(url)
				info = f.read()
				tmp = "/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml"
				file = open(tmp, "w")
				file.write(info)
				file.close()
				print "[Testplugin]: download done ", url
			except IOError,e:
				print "[Testplugin]: I/O error!", e
			except IOError,e:
				print "[Testplugin]: I/O error!", e

			try:
				self.updatebq()
				from enigma import eDVBDB
				eDVBDB.getInstance().reloadBouquets()
				eDVBDB.getInstance().reloadServicelist()
				tmpMessage = _("GreekStreamTV bouquet updated successfully...")
				self.session.open(MessageBox, tmpMessage, MessageBox.TYPE_INFO)
			except Exception as err:
				print "[GreekStreamTV::PluginMenu] Exception: ", str(err)
				tmpMessage = _("GreekStreamTV bouquet update failed...")
				self.session.open(MessageBox, tmpMessage, MessageBox.TYPE_INFO)

	def create(self, answer):
		if answer:
			self.session.open(Console,_("Create bouquets list"),["%s create" % url_sc])

	def showInfo(self):
		tmpMessage = _("For information or questions please refer to the www.satdreamgr.com forum.")
		tmpMessage += "\n\n"
		tmpMessage += _("GreekStreamTV is free.")
		self.session.open(MessageBox, tmpMessage, MessageBox.TYPE_INFO)

	def updatebq(self):
		from xml.etree.cElementTree import ElementTree
		tree = ElementTree()
		tree.parse(GSXML)
		tvlist = []
		for iptv in tree.findall("iptv"):
			name = iptv.findtext("name").title()
			(protocol, serviceType, bufferSize, epgId) = iptv.findtext("type").split(":")
			uri = iptv.findtext("uri")
			if protocol in "livestreamer":
				uri = "http://localhost:88/" + uri
			uri = uri.replace(":", "%3a")
			service = "#SERVICE {s}:0:1:{e}:{e}:0:0:0:0:0:{u}:{n}\n".format(s=serviceType,e=epgId,u=uri,n=name)
			tvlist.append((name,service))

		tvlist = sorted(tvlist, key=lambda channel: channel[0]) #sort by name
		with open(GSBQ, "w") as f:
			f.write("#NAME GreekStreamTV\n")
			for (name, service) in tvlist:
				f.write(service)

		com = "cat /usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml ; rm /usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml"
		out = os.popen(com)

		return list
