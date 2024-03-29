from . import _
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from os import listdir


class Removeopkg(Screen):

	skin = """
		<screen name="Removeopkg" position="center,center" size="500,405">
			<widget name="list" itemHeight="35" position="10,10" size="480,350" scrollbarMode="showOnDemand" font="Regular;20"/>
			<ePixmap pixmap="buttons/key_red.png" position="10,372" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="buttons/key_green.png" position="165,372" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,370" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,370" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Remove packages"))
		try:
			menulist = listdir("/var/lib/opkg/info")
			menulist = [x[:-8] for x in menulist if x.endswith("control")]
		except:
			menulist = []
		menulist.sort()
		self["list"] = MenuList(menulist)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Remove"))
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


def main(session, **kwargs):
	session.open(Removeopkg)


def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("Remove packages"), main, "removeopkg_setup", 45)]
	return []


def Plugins(**kwargs):
	return PluginDescriptor(name=_("Remove packages"), description=_("Remove packages"), where=PluginDescriptor.WHERE_MENU, fnc=menu)
