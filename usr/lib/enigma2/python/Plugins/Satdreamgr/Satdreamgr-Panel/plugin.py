import os
import sys
from . import _
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List


def main(session,**kwargs):
	try:
		session.open(Panel)
	except:
		print "[Panel +] Plugin execution failed"


def autostart(reason,**kwargs):
	if reason == 0:
		print "[PluginMenu] no autostart"


def menu(menuid):
	if menuid == "mainmenu":
		return [(_("Panel +"), main, "panel_setup", 1)]
	return []


def Plugins(**kwargs):
	list = []
	list.append(PluginDescriptor(name=_("Panel +"), description=_("Panel + SatDreamGr"), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon="plugin.png", fnc=main))
	list.append(PluginDescriptor(where=PluginDescriptor.WHERE_MENU, fnc=menu))
	return list


panel_main = """<screen name="Panel+" position="center,center" size="600,405" title="Panel +" >
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


class Panel(Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = panel_main
		self.session = session
		self.drawList = []
		self.setup_title = _("Panel +")
		self.onLayoutFinish.append(self.layoutFinished)
		self["list"] = List()
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.refresh()

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def refresh(self):
		self.drawList = []
		self.drawList.append(self.buildListEntry(_("Softcam setup"), "key.png"))
		self.drawList.append(self.buildListEntry(_("System panel"), "system.png"))
		self.drawList.append(self.buildListEntry(_("Plugins panel"), "plus.png"))

		self["list"].setList(self.drawList)

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			try:
				from Screens.SoftcamSetup import SoftcamSetup
				self.session.open(SoftcamSetup)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 1:
			self.session.open(System_Panel)
		elif index == 2:
			self.session.open(Plugins_Panel)

	def quit(self):
		self.close()

	def layoutFinished(self):
		self.setTitle(self.setup_title)


class System_Panel(Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = panel_main
		self.session = session
		self.drawList = []
		self.setup_title = _("Panel +")
		self.onLayoutFinish.append(self.layoutFinished)
		self["list"] = List()
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.refresh()

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def refresh(self):
		self.drawList = []
		self.drawList.append(self.buildListEntry(_("Archives explorer"), "Archives.png"))
		self.drawList.append(self.buildListEntry(_("System information"), "hardware.png"))
		self.drawList.append(self.buildListEntry(_("TranspBA skin setup"), "eye.png")) # this has been removed - just display an information message
		self.drawList.append(self.buildListEntry(_("Enigma2 settings"), "settings.png"))
		self.drawList.append(self.buildListEntry(_("Remove packages"), "remove.png"))
		self.drawList.append(self.buildListEntry(_("Swap manager"), "swap.png"))
		self.drawList.append(self.buildListEntry(_("Hotkey"), "hotkey.png"))
		self["list"].setList(self.drawList)

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
			self.session.open(MessageBox, _("Plugin has been moved under the 'GUI settings' menu."), MessageBox.TYPE_INFO)
		elif index == 3:
			try:
				from Plugins.Satdreamgr.SettingsSatDreamGr.plugin import SDG_Menu
				self.session.open(SDG_Menu)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 4:
			try:
				from Plugins.Satdreamgr.RemoveOPKG.plugin import Removeopkg
				self.session.open(Removeopkg)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 5:
			try:
				from Plugins.Satdreamgr.SwapManager.plugin import SystemToolsSwap
				self.session.open(SystemToolsSwap)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 6:
			try:
				from Screens.Hotkey import HotkeySetup
				self.session.open(HotkeySetup)
			except:
				self.session.open(MessageBox, _("Sorry, plugin is not installed!"), MessageBox.TYPE_INFO)

	def quit(self):
		self.close()

	def layoutFinished(self):
		self.setTitle(self.setup_title)


class Plugins_Panel(Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = panel_main
		self.session = session
		self.drawList = []
		self.setup_title = _("Panel +")
		self.onLayoutFinish.append(self.layoutFinished)
		self["list"] = List()
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.refresh()

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def refresh(self):
		self.drawList = []
		self.drawList.append(self.buildListEntry(_("SDG radio"), "radio.png"))
		self.drawList.append(self.buildListEntry(_("Internet radio"), "netradio.png"))
		self.drawList.append(self.buildListEntry(_("Picture camera"), "camera.png"))
		self.drawList.append(self.buildListEntry(_("GreekStreamTV"), "greekstream.png"))
		self.drawList.append(self.buildListEntry(_("GreekStreamTV in bouquets"), "greekstreamb.png"))
		self["list"].setList(self.drawList)

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
		elif index == 4:
			self.session.open(MessageBox, _("This functionality has been moved into the GreekStreamTV plugin."), MessageBox.TYPE_INFO)

	def quit(self):
		self.close()

	def layoutFinished(self):
		self.setTitle(self.setup_title)
