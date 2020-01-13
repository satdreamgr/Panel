from . import _
from Screens.Screen import Screen
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Tools.LoadPixmap import LoadPixmap
from SDG_Vhannibal import SDG_VhannibalHelper
from SDG_Morpheus import SDG_MorpheusHelper
from SDG_Satdreamgr import SDG_SatdreamgrHelper
from SDG_Satvenus import SDG_SatvenusHelper
from SDG_Likra import SDG_LikraHelper
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
import os
import sys
from enigma import *
from time import *


def main(session, **kwargs):
	try:
		session.open(SDG_Menu)
	except:
		print "[Settings] Plugin execution failed"


def autostart(reason, **kwargs):
	if reason == 0:
		print "[PluginMenu] no autostart"


def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("Enigma2 settings"), main, "settings_setup", 45)]
	return []


def Plugins(**kwargs):
	return PluginDescriptor(name=_("Enigma2 settings"), description="Morpheus, Vhannibal, Cyrus, Satvenus, Likra", where=PluginDescriptor.WHERE_MENU, fnc=menu)


class SDG_Menu(Screen):

	skin = """
		<screen name="SDG_Menu" position="center,center" size="600,405" title="Enigma2 settings">
			<widget source="list" render="Listbox" position="10,10" size="580,350" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
						MultiContentEntryPixmapAlphaBlend(pos = (12, 4), size = (32, 32), png = 0),
						MultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),
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

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.drawList = []
		self.setup_title = _("Enigma2 settings")
		self.onLayoutFinish.append(self.layoutFinished)
		self["list"] = List()
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Select"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
			"red": self.quit,
			"green": self.openSelected,
		}, -2)

		self.refresh()

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image))
		return((pixmap, description))

	def refresh(self):
		self.drawList = []
		self.drawList.append(self.buildListEntry("Morpheus883", "morphd.png"))
		self.drawList.append(self.buildListEntry("Vhannibal", "Vhannibal.png"))
		self.drawList.append(self.buildListEntry("Cyrus", "downloads.png"))
		self.drawList.append(self.buildListEntry("Satvenus", "satv.png"))
		self.drawList.append(self.buildListEntry("Likra", "likra.png"))
		self["list"].setList(self.drawList)

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			SDG_MorpheusHelper(self.session).load()
		elif index == 1:
			SDG_VhannibalHelper(self.session).load()
		elif index == 2:
			SDG_SatdreamgrHelper(self.session).load()
		elif index == 3:
			SDG_SatvenusHelper(self.session).load()
		elif index == 4:
			SDG_LikraHelper(self.session).load()

	def quit(self):
		self.close()

	def layoutFinished(self):
		self.setTitle(self.setup_title)
