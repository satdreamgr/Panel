###### By ATHOIK #########
from Screens.Screen import Screen
from Screens.Console import Console
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.config import config
import gettext
try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

menu_s = "/usr/lib/enigma2/python/Plugins/Satdreamgr/SDGBackup/dreambox-fullbackup.sh"

###########################################################################

def main(session, **kwargs):
	try:
		session.open(SDGBackup)
	except:
		print "[SDGBackup] Plugin execution failed"

def autostart(reason, **kwargs):
	if reason == 0:
		print "[PluginMenu] no autostart"

def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("SDGBackup Dreambox Enigma2"), main, "sdgbackup_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("SDGBackup Dreambox Enigma2"), description = _("SDGBackup Dreambox Enigma2"), where = PluginDescriptor.WHERE_MENU, fnc = menu)

###########################################################################

class SDGBackup(Screen):
	skin = """
		<screen position="center,center" size="460,400" title="SDGBackup Dreambox Enigma2">
			<widget name="menu" position="10,10" size="420,380" scrollbarMode="showOnDemand"/>
			<widget name="key_red" position="10,320" size="100,40" backgroundColor="red" valign="center" halign="center" zPosition="2" foregroundColor="white" font="Regular;20"/>
			<widget name="key_green" position="120,320" size="100,40" backgroundColor="green" valign="center" halign="center" zPosition="2" foregroundColor="white" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.location = ""
		menu = []
		menu.append((_("Start SDGBackup on USB"), "/media/usb"))
		menu.append((_("Start SDGBackup on HDD"), "/media/hdd"))
		self["key_red"] = self["myRedBtn"] = Label(_("Cancel")) # keep old button name for compatibility with skins
		self["key_green"] = self["myGreenBtn"] = Label(_("OK")) # keep old button name for compatibility with skins
		self["menu"] = MenuList(menu)
		self["actions"] = ActionMap(["OkCancelActions", "SetupActions", "ColorActions", "WizardActions", "DirectionActions"], {"ok": self.go, "green": self.go, "cancel": self.close}, -1)

	def go(self):
		returnValue = self["menu"].l.getCurrentSelection()[1]
		if returnValue:
			self.location = returnValue
			self.session.openWithCallback(self.greek,MessageBox,_("You are about to create a backup to the selected location.\nDo you really want to proceed?"), MessageBox.TYPE_YESNO)

	def greek(self, answer):
		if answer:
			self.session.open(Console,_("Backup is running..."),["%s %s" % (menu_s, self.location)])
