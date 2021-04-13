import os
from . import _
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import configfile
from Components.MenuList import MenuList
from Screens.Console import Console
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Tools.Directories import resolveFilename, SCOPE_PLUGINS


def main(session,**kwargs):
	try:
		session.open(HardwareInfo)
	except:
		print "[Hardware] Plugin execution failed"


def autostart(reason,**kwargs):
	if reason == 0:
		print "[PluginMenu] no autostart"


def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("System information"), main, "harware_setup", 45)]
	return []


def Plugins(**kwargs):
	return PluginDescriptor(name=_("System information"), description=_("System information"), where=PluginDescriptor.WHERE_MENU, fnc=menu)


class HardwareInfo(Screen):

	skin = """
		<screen name="System information" position="center,center" size="600,405" >
			<widget name="menu" itemHeight="35" position="20,10" size="580,330" scrollbarMode="showOnDemand" transparent="1" zPosition="9"/>
			<ePixmap pixmap="buttons/key_red.png" position="80,360" size="32,32" zPosition="1" alphatest="blend"/>
			<ePixmap pixmap="buttons/key_green.png" position="240,360" size="32,32" zPosition="1" alphatest="blend"/>
			<widget name="key_red" position="110,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
			<widget name="key_green" position="270,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		menu = []
		menu.append((_("Hardware info"), "system"))
		menu.append((_("DVB modules"), "modules"))
		menu.append((_("Netstat"), "netstat"))
		menu.append((_("Ifconfig"), "ifconfig"))
		menu.append((_("Internet connectivity test"), "internet"))
		menu.append((_("Second stage loader version"), "Second"))
		menu.append((_("Show installed packages"), "listinstalled"))
		menu.append((_("Show devices"), "devices"))
		menu.append((_("Show mounts"), "mounts"))
		menu.append((_("Delete crash logs"), "crashlogs"))
		menu.append((_("Create debug log"), "debuglog"))
		self["menu"] = MenuList(menu)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Select"))
		self.setup_title = _("System information")
		self.setTitle(self.setup_title)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "WizardActions", "DirectionActions"],{"ok": self.go, "red": self.close, "green": self.go, "back": self.close,}, -1)

	def go(self):
		if self["menu"].l.getCurrentSelection() is not None:
			choice = self["menu"].l.getCurrentSelection()[1]
		if choice == "system":
			self.session.open(system_info)
		if choice == "modules":
			self.session.open(Console, _("DVB modules"), ["opkg list_installed | grep dvb-modules"], showStartStopText=False)
		if choice == "netstat":
			self.session.open(Console, _("Netstat"), ["netstat | grep tcp && netstat | grep unix"], showStartStopText=False)
		if choice == "ifconfig":
			self.session.open(Console, _("Ifconfig"), ["ifconfig"], showStartStopText=False)
		if choice == "internet":
			self.session.open(Console, _("Internet connectivity test"), ["ping -c 1 www.satdreamgr.com && ping -c 1 www.google.com"], showStartStopText=False)
		if choice == "Second":
			self.session.open(Console, _("Second stage loader installed version"), ["opkg list | grep second"], showStartStopText=False)
		if choice == "listinstalled":
			self.session.open(Console, _("Show installed packages"), ["opkg list_installed"], showStartStopText=False)
		if choice == "devices":
			self.session.open(Console, _("Device info"), ["df -h"], showStartStopText=False)
		if choice == "mounts":
			self.session.open(Console, _("Mounts info"), ["mount"], showStartStopText=False)
		if choice == "crashlogs":
			self.session.openWithCallback(self.removeCRASH, MessageBox, _("Do you really want to delete all existing crash logs?"), MessageBox.TYPE_YESNO)
		if choice == "debuglog":
			self.session.openWithCallback(self.debugLOG, MessageBox, _("Do you really want to create a new debug log?"), MessageBox.TYPE_YESNO)

	def debugLOG(self, answer):
		if answer is True:
			os.system("dmesg > /tmp/sdg.debug.log && lsusb >> /tmp/sdg.debug.log && lsmod >> /tmp/sdg.debug.log && cat /proc/bus/nim_sockets >> /tmp/sdg.debug.log")
			configfile.save()
			self.session.open(MessageBox, _("Execution finished!"), MessageBox.TYPE_INFO, timeout=5)

	def removeCRASH(self, answer):
		if answer is True:
			os.system("rm -rf /media/hdd/enigma2_crash*")
			configfile.save()
			self.session.open(MessageBox, _("Execution finished!"), MessageBox.TYPE_INFO, timeout=5)


class system_info(Screen):

	skin = """
	<screen name="Hardware info" position="center,center" size="640,480">
		<ePixmap position="20,30" zPosition="5" size="50,50" pixmap="~/icons/ram.png" alphatest="blend" />
		<widget source="session.Event_Now" render="Progress" pixmap="~/icons/bar.png" position="90,30" size="515,20" transparent="1" zPosition="6">
			<convert type="PanelSpaceInfo">MemTotal</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" zPosition="6" position="90,56" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
			<convert type="PanelSpaceInfo">MemTotal,Full</convert>
		</widget>
		<ePixmap position="20,110" zPosition="1" size="50,50" pixmap="~/icons/swap.png" alphatest="blend" />
		<widget source="session.Event_Now" render="Progress" pixmap="~/icons/bar.png" position="90,110" size="515,20" transparent="1" zPosition="6">
			<convert type="PanelSpaceInfo">SwapTotal</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" zPosition="6" position="90,134" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
			<convert type="PanelSpaceInfo">SwapTotal,Full</convert>
		</widget>
		<ePixmap position="20,190" zPosition="1" size="50,50" pixmap="~/icons/flash.png" alphatest="blend" />
		<widget source="session.Event_Now" render="Progress" pixmap="~/icons/bar.png" position="90,190" size="515,20" transparent="1" zPosition="6">
			<convert type="PanelSpaceInfo">FleshInfo</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" zPosition="6" position="90,213" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
			<convert type="PanelSpaceInfo">Flesh,Full</convert>
		</widget>
		<ePixmap position="20,270" zPosition="1" size="50,50" pixmap="~/icons/hdd.png" alphatest="blend" />
		<widget source="session.Event_Now" render="Progress" pixmap="~/icons/bar.png" position="90,270" size="515,20" transparent="1" zPosition="6">
			<convert type="PanelSpaceInfo">HddInfo</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" zPosition="6" position="90,293" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
			<convert type="PanelSpaceInfo">HddInfo,Full</convert>
		</widget>
		<ePixmap position="20,350" zPosition="1" size="50,50" pixmap="~/icons/usb.png" alphatest="blend" />
		<widget source="session.Event_Now" render="Progress" pixmap="~/icons/bar.png" position="90,350" size="515,20" transparent="1" zPosition="6">
			<convert type="PanelSpaceInfo">UsbInfo</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" zPosition="6" position="90,378" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
			<convert type="PanelSpaceInfo">UsbInfo,Full</convert>
		</widget>
		<widget backgroundColor="#000015" font="Regular; 23" foregroundColor="green" halign="center" position="20,440" render="Label" size="120,23" source="session.CurrentService" transparent="1" zPosition="1" valign="center">
			<convert type="PanelCpuUsage">Total</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Hardware info"))
		self.skin_path = resolveFilename(SCOPE_PLUGINS, "Satdreamgr/Hardware")

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "WizardActions", "DirectionActions"],
		{
			"ok": self.close,
			"back": self.close,
		}, -1)
