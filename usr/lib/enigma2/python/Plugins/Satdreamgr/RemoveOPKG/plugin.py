from . import _
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from os import listdir


def main(session,**kwargs):
	try:
		session.open(Removeopkg)
	except:
		print "[Removeopkg] Plugin execution failed"


def autostart(reason,**kwargs):
	if reason == 0:
		print "[PluginMenu] no autostart"


def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("Remove packages"), main, "removeopkg_setup", 45)]
	return []


def Plugins(**kwargs):
	return PluginDescriptor(name=_("Remove packages"), description=_("Remove packages"), where=PluginDescriptor.WHERE_MENU, fnc=menu)


class Removeopkg(Screen):

	skin = """
		<screen name="Removeopkg" position="center,center" size="500,405">
			<widget name="list" itemHeight="35" position="10,10" size="480,350" scrollbarMode="showOnDemand" font="Regular;20"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="10,372" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="165,372" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,370" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,370" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		try:
			list = listdir("/var/lib/opkg/info")
			list = [x[:-8] for x in list if x.endswith("control")]
		except:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Remove"))
		self.setup_title = _("Remove packages")
		self.setTitle(self.setup_title)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"ok": self.ExecDelete,
				"cancel": self.close,
				"red": self.close,
				"green": self.ExecDelete,
			}, -1)

	def ExecDelete(self):
			archive = self["list"].getCurrent()
			start = self.session.openWithCallback(self.remove, MessageBox, _("Do you realy want to remove the following package?\n") + archive, MessageBox.TYPE_YESNO)
			start.setTitle(_("Delete package..."))

	def remove(self, answer):
		archive = self["list"].getCurrent()
		if answer is True:
			if archive.endswith(""):
				command = "opkg remove %s" % archive
			self.session.open(Console, _("Remove"), cmdlist=[command])
			self.close(Removeopkg)
