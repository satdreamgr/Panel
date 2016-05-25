import os
import sys
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.config import config
from Components.Sources.List import List
from Components.PluginComponent import plugins
from Plugins.Satdreamgr.Manipulate.plugin import PluginStart
from Plugins.Satdreamgr.Hardware.plugin import HardwareInfo
from Plugins.Satdreamgr.RemoveOPKG.plugin import Removeopkg
from Plugins.Satdreamgr.SDGBackup.plugin import SDGBackup
from Plugins.Satdreamgr.SettingsSatDreamGr.plugin import SDG_Menu
from Plugins.Satdreamgr.SwapManager.plugin import SystemToolsSwap
from Plugins.Satdreamgr.UpdateBouquet.plugin import UpdateBouquet
from Plugins.Extensions.GreekStreamTV.plugin import GSMenu
from Plugins.Satdreamgr.SkinSatdreamgr.plugin import MyMenuSKIN
from Plugins.Satdreamgr.PictureCamera.plugin import PictureCamera
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.LoadPixmap import LoadPixmap
import gettext
try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass
def main(session,**kwargs):
    try:
     	session.open(Panel)
    except:
        print "[Panel +] Pluginexecution failed"

def autostart(reason,**kwargs):
    if reason == 0:
        print "[PluginMenu] no autostart"

def menu(menuid):
	if menuid == "mainmenu":
		return [(_("Panel +"), main, "panel_setup", 1)]
	return []

def Plugins(**kwargs):
	list = []
	list.append(PluginDescriptor(name=_("Panel +"),description=_("Panel + SatDreamGr"),where=PluginDescriptor.WHERE_EXTENSIONSMENU,icon="plugin.png", fnc=main))
	list.append(PluginDescriptor(where=PluginDescriptor.WHERE_MENU, fnc=menu))
	return list

panel_main = """<screen name="Panel+" position="center,center" size="600,405" title="Panel +" >
		<widget source="list" render="Listbox" position="20,10" size="580,320" scrollbarMode="showOnDemand" transparent="1" >
		<convert type="TemplatedMultiContent">
		{"template": [
		MultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),
				MultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
						],
						"fonts": [gFont("Regular", 22)],
						"itemHeight": 40
					}
				</convert>
			</widget>
                   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/key_exit.png" position="80,360" size="40,32" zPosition="1" alphatest="blend"/>
                   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/key_ok.png" position="240,360" size="40,32" zPosition="1" alphatest="blend"/>
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
		self.drawList.append(self.buildListEntry(_("Archives Explorer"), "Archives.png"))
		self.drawList.append(self.buildListEntry(_("Hardware Info"), "hardware.png"))
		self.drawList.append(self.buildListEntry(_("Change Color TranspBA Skin"), "eye.png"))
		self.drawList.append(self.buildListEntry(_("GreekStreamTV"), "greekstream.png"))
		self.drawList.append(self.buildListEntry(_("GreekStreamTV in Bouquets"), "greekstreamb.png"))
		self.drawList.append(self.buildListEntry(_("Settings E2"), "settings.png"))
		self.drawList.append(self.buildListEntry(_("SDGBackup Dreambox Enigma2"), "backup.png"))
		self.drawList.append(self.buildListEntry(_("Remove Additional Packages"), "remove.png"))
		self.drawList.append(self.buildListEntry(_("Swap Manager"), "swap.png"))
		self.drawList.append(self.buildListEntry(_("PictureCamera"), "camera.png"))		

		self["list"].setList(self.drawList)

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
					try:
						from Plugins.PLi.SoftcamSetup.plugin import main
						main(self.session)
					except:
						self.session.open(MessageBox, _("Sorry Plugin is not installed!"), MessageBox.TYPE_INFO)
		elif index == 1:
			self.session.open(PluginStart)
		elif index == 2:
			self.session.open(HardwareInfo)
		elif index == 3:
			self.session.open(MyMenuSKIN)
		elif index == 4:
			self.session.open(GSMenu)
		elif index == 5:
			self.session.open(UpdateBouquet)
		elif index == 6:
			self.session.open(SDG_Menu)
		elif index == 7:
			self.session.open(SDGBackup)
		elif index == 8:
			self.session.open(Removeopkg)
		elif index == 9:
			self.session.open(SystemToolsSwap)
		elif index == 10:
			self.session.open(PictureCamera)			
	def quit(self):
		self.close()

	def layoutFinished(self):
		self.setTitle(self.setup_title)
