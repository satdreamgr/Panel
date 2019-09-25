import os
import urllib
from Plugins.Plugin import PluginDescriptor
from Components.Sources.List import List
from Components.Input import Input
from Components.Pixmap import Pixmap
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap, NumberActionMap
from Components.FileList import FileList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from enigma import getDesktop
from Tools import Notifications
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.Standby import *
from Screens.Console import Console
from ServiceReference import ServiceReference
from urllib2 import urlopen
from os import popen as os_popen
from os import listdir
from time import localtime as time_localtime
from time import strftime as time_strftime
import datetime
import time
import gettext
import datetime
import time

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
		return [(_("Remove additional packages"), main, "removeopkg_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Remove additional packages"), description = _("Remove additional packages"), where = PluginDescriptor.WHERE_MENU, fnc = menu)


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
		self.setup_title = _("Remove additional packages")
		self.onLayoutFinish.append(self.layoutFinished)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"ok": self.ExecDelete,
				"cancel": self.close,
				"red": self.close,
				"green": self.ExecDelete,
			}, -1)

	def layoutFinished(self):
		self.setTitle(self.setup_title)

	def ExecDelete(self):
			archive = self["list"].getCurrent()
			start = self.session.openWithCallback(self.remove,MessageBox,_(("Do you realy want to delete:\n")+archive), MessageBox.TYPE_YESNO)
			start.setTitle(_("Delete file..."))

	def remove(self, answer):
		archive = self["list"].getCurrent()
		if answer is True:
			if archive.endswith(""):
				command = "opkg remove %s" % archive
			self.session.open(Console, _("Remove"), cmdlist=[command])
			self.close(Removeopkg)
