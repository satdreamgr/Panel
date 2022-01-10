from os.path import dirname
from sys import modules

from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.LoadPixmap import LoadPixmap

from . import _

mainPanelEntries = [
	(_("Softcam setup"), "key.png"),
	(_("System panel"), "system.png"),
	(_("Plugins panel"), "plus.png")
]

systemPanelEntries = [
	(_("Archives explorer"), "Archives.png"),
	(_("System information"), "hardware.png"),
	(_("Remove packages"), "remove.png"),
	(_("Swap manager"), "swap.png"),
	(_("Hotkey"), "hotkey.png")
]

pluginsPanelEntries = [
	(_("SDG radio"), "radio.png"),
	(_("Internet radio"), "netradio.png"),
	(_("Picture camera"), "camera.png"),
	(_("GreekStreamTV"), "greekstream.png")
]


class SDGPanel(Screen):

	skin = """
	<screen name="Panel+" position="center,center" size="600,405" title="Panel +" >
		<widget source="list" render="Listbox" position="20,10" size="580,320" scrollbarMode="showOnDemand" transparent="1" >
			<convert type="TemplatedMultiContent">
				{"template": [
					MultiContentEntryPixmapAlphaBlend(pos = (12, 4), size = (32, 32), png = 0),
					MultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
					],
				"fonts": [gFont("Regular", 22)],
				"itemHeight": 40
				}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session, menuEntries):
		Screen.__init__(self, session)
		self.setTitle(_("Panel +"))
		if not isinstance(self.skinName, list):
			self.skinName = [self.skinName]
		self.skinName.append("Panel") # Support legacy skin name
		menu = []
		for (description, image) in menuEntries:
			pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (dirname(modules[__name__].__file__), image))
			menu.append((pixmap, description))
		self["list"] = List(menu)
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.close,
			"ok": self.openSelected,
		}, -2)

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			try:
				from Screens.SoftcamSetup import SoftcamSetup
				self.session.open(SoftcamSetup)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 1:
			self.session.open(SDGSystemPanel, systemPanelEntries)
		elif index == 2:
			self.session.open(SDGPluginsPanel, pluginsPanelEntries)


class SDGSystemPanel(SDGPanel):

	def __init__(self, session, menuEntries):
		SDGPanel.__init__(self, session, menuEntries=menuEntries)
		self.skinName.insert(1, "System_Panel") # Support legacy skin name
		self.skinName.insert(1, "SDGPanel")

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			try:
				from Plugins.Satdreamgr.Manipulate.plugin import PluginStart
				self.session.open(PluginStart)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 1:
			try:
				from Plugins.Satdreamgr.Hardware.plugin import HardwareInfo
				self.session.open(HardwareInfo)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 2:
			try:
				from Plugins.Satdreamgr.RemoveOPKG.plugin import Removeopkg
				self.session.open(Removeopkg)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 3:
			try:
				from Plugins.Satdreamgr.SwapManager.plugin import SystemToolsSwap
				self.session.open(SystemToolsSwap)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 4:
			try:
				from Screens.Hotkey import HotkeySetup
				self.session.open(HotkeySetup)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)


class SDGPluginsPanel(SDGPanel):

	def __init__(self, session, menuEntries):
		SDGPanel.__init__(self, session, menuEntries=menuEntries)
		self.skinName.insert(1, "Plugins_Panel") # Support legacy skin name
		self.skinName.insert(1, "SDGPanel")

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			try:
				from Plugins.Extensions.SDGRadio.plugin import SDGRadioScreen
				self.session.open(SDGRadioScreen)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 1:
			try:
				from Plugins.Extensions.GreekNetRadio.plugin import GreekNetRadio
				self.session.open(GreekNetRadio)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 2:
			try:
				from Plugins.Satdreamgr.PictureCamera.plugin import PictureCamera
				self.session.open(PictureCamera)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 3:
			try:
				from Plugins.Extensions.GreekStreamTV.plugin import GSMenu
				self.session.open(GSMenu)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)


def main(session, **kwargs):
	session.open(SDGPanel, mainPanelEntries)


def menu(menuid):
	if menuid == "mainmenu":
		return [(_("Panel +"), main, "panel_setup", 1)]
	return []


def Plugins(**kwargs):
	plugin = []
	plugin.append(PluginDescriptor(name=_("Panel +"), description=_("Panel + SatDreamGr"), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon="plugin.png", fnc=main))
	plugin.append(PluginDescriptor(where=PluginDescriptor.WHERE_MENU, fnc=menu))
	return plugin
