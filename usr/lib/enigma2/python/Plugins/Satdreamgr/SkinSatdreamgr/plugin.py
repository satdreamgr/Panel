import os
from Tools.Profile import profile
from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from os import environ, listdir, remove, rename, system, path
from skin import parseColor
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from shutil import move, copy
import re
import gettext

try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

config.plugins.SatdreamgrTranspBA = ConfigSubsection()
config.plugins.SatdreamgrTranspBA.SkinColor = ConfigSelection(default="#20000000", choices = [
				("#20000000", _("1-Original")),
				("#00000000", _("2-Black")),
				("#50000000", _("3-Ultra Transparent")),
				("#00102030", _("4-Blue")),
				("#00002222", _("5-Green")),
				("#00080022", _("6-Navy Blue")),
				("#00333333", _("7-Grey"))
				])

def main(session, **kwargs):
	try:
		session.open(MyMenuSKIN)
	except:
		print "[Satdreamgr-HD-TranspBA] Plugin execution failed"

def autostart(reason, **kwargs):
	if reason == 0:
		print "[PluginMenu] no autostart"

def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("Satdreamgr-HD-TranspBA"), main, "configskin_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Satdreamgr-HD-TranspBA"), description = _("Configuration tool for Satdreamgr TranspBA skin"), where = PluginDescriptor.WHERE_MENU, fnc = menu)

class MyMenuSKIN(Screen):
	skin = """
		<screen name="MyMenuSKIN" position="center,center" size="600,480" title="TranspBA skin configuration">
			<widget name="menu" position="10,10" size="580,420" font="Regular;20" scrollbarMode="showOnDemand"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="10,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="165,442" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,440" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		Screen.setTitle(self, _("TranspBA skin configuration"))
		menu = []
		menu.append((_("Change color"), ))
		menu.append((_("Change color Satdreamgr-HD-TranspBA"),"skinhd"))
		menu.append(("", ))
		menu.append((_("Change infobar"), ))
		menu.append((_("Simple infobar Satdreamgr-HD-TranspBA"),"simple"))
		menu.append((_("Full bottom infobar Satdreamgr-HD-TranspBA"),"fullbottom"))
		menu.append((_("Full infobar Satdreamgr-HD-TranspBA"),"full"))
		menu.append(("", ))
		menu.append((_("Weather in infobar"), ))
		menu.append((_("Weather ON in infobar"),"weatheron"))
		menu.append((_("Weather OFF in infobar"),"weatheroff"))

		self["menu"] = MenuList(menu)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Select"))

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"ok": self.go,
				"cancel": self.close,
				"red": self.close,
				"green": self.go,
			}, -1)

	def go(self):
		if self["menu"].l.getCurrentSelection() is not None:
			choice = self["menu"].l.getCurrentSelection()[1]
			if choice == "skinhd":
				self.session.open(SatdreamgrTranspBA)
			if choice == "full":
				self.session.openWithCallback(self.FullInfobar, MessageBox,_("Confirm your selection?"), MessageBox.TYPE_YESNO)
			if choice == "fullbottom":
				self.session.openWithCallback(self.FullBottomInfobar, MessageBox,_("Confirm your selection?"), MessageBox.TYPE_YESNO)
			if choice == "simple":
				self.session.openWithCallback(self.SimpleInfobar, MessageBox,_("Confirm your selection?"), MessageBox.TYPE_YESNO)
			if choice == "weatheron":
				self.session.openWithCallback(self.WeatherONInfobar, MessageBox,_("Confirm your selection?"), MessageBox.TYPE_YESNO)
			if choice == "weatheroff":
				self.session.openWithCallback(self.WeatherOFFInfobar, MessageBox,_("Confirm your selection?"), MessageBox.TYPE_YESNO)

	def SimpleInfobar(self, answer):
		if answer is True:
			f = file("/etc/enigma2/skin_user_Satdreamgr-HD-TranspBA.xml","r")
			chaine = f.read()
			f.close()
			result=chaine.replace("infobar_b.xml", "infobar_a.xml").replace("infobar_c.xml", "infobar_a.xml")
			f = file("/etc/enigma2/skin_user_Satdreamgr-HD-TranspBA.xml","w")
			f.write(result)
			configfile.save()
			self.session.open(TryQuitMainloop, 3)

	def FullBottomInfobar(self, answer):
		if answer is True:
			f = file("/etc/enigma2/skin_user_Satdreamgr-HD-TranspBA.xml","r")
			chaine = f.read()
			f.close()
			result=chaine.replace("infobar_a.xml", "infobar_c.xml").replace("infobar_b.xml", "infobar_c.xml")
			f = file("/etc/enigma2/skin_user_Satdreamgr-HD-TranspBA.xml","w")
			f.write(result)
			configfile.save()
			self.session.open(TryQuitMainloop, 3)

	def FullInfobar(self, answer):
		if answer is True:
			f = file("/etc/enigma2/skin_user_Satdreamgr-HD-TranspBA.xml","r")
			chaine = f.read()
			f.close()
			result=chaine.replace("infobar_a.xml", "infobar_b.xml").replace("infobar_c.xml", "infobar_b.xml")
			f = file("/etc/enigma2/skin_user_Satdreamgr-HD-TranspBA.xml","w")
			f.write(result)
			configfile.save()
			self.session.open(TryQuitMainloop, 3)

	def WeatherONInfobar(self, answer):
		if answer is True:
			f = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_a.xml","r")
			chaine = f.read()
			f.close()
			result=chaine.replace("<!--<eLabel /> ", "<ePixmap />")
			f = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_a.xml","w")
			f.write(result)
			configfile.save()
			a = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_b.xml","r")
			chaine = a.read()
			a.close()
			result=chaine.replace("<!--<eLabel /> ", "<ePixmap />")
			a = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_b.xml","w")
			a.write(result)
			configfile.save()
			b = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_c.xml","r")
			chaine = b.read()
			b.close()
			result=chaine.replace("<!--<eLabel /> ", "<ePixmap />")
			b = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_c.xml","w")
			b.write(result)
			configfile.save()
			self.session.open(TryQuitMainloop, 3)

	def WeatherOFFInfobar(self, answer):
		if answer is True:
			f = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_a.xml","r")
			chaine = f.read()
			f.close()
			result=chaine.replace("<ePixmap />", "<!--<eLabel /> ")
			f = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_a.xml","w")
			f.write(result)
			configfile.save()
			a = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_b.xml","r")
			chaine = a.read()
			a.close()
			result=chaine.replace("<ePixmap />", "<!--<eLabel /> ")
			a = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_b.xml","w")
			a.write(result)
			configfile.save()
			b = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_c.xml","r")
			chaine = b.read()
			b.close()
			result=chaine.replace("<ePixmap />", "<!--<eLabel /> ")
			b = file("/usr/share/enigma2/Satdreamgr-HD-TranspBA/infobar_c.xml","w")
			b.write(result)
			configfile.save()
			self.session.open(TryQuitMainloop, 3)

class SatdreamgrTranspBA(ConfigListScreen, Screen):
	skin = """
		<screen name="SatdreamgrTranspBA" position="center,center" size="600,480" title="Change color">
			<widget name="config" position="10,10" scrollbarMode="showOnDemand" size="580,420" font="Regular;20"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="10,442" size="32,32" alphatest="blend"/>
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="165,442" size="32,32" alphatest="blend"/>
			<widget name="key_red" position="45,440" size="120,32" valign="center" font="Regular;20"/>
			<widget name="key_green" position="200,440" size="120,32" valign="center" font="Regular;20"/>
		</screen>"""

	def __init__(self, session, args = None, picPath = None):
		Screen.__init__(self, session)
		self.session = session
		Screen.setTitle(self, _("Change color"))
		self.myskinpath = "/etc/enigma2/"
		self.SkinDefault = self.myskinpath + "skin_user_Satdreamgr-HD-TranspBA.xml"
		self.SkinDefaultTmp = self.SkinDefault + ".TMP"
		self.myskinpathout = "/etc/enigma2/"
		self.SkinFinal = self.myskinpathout + "skin_user_Satdreamgr-HD-TranspBA.xml"
		ConfigListScreen.__init__(self, [])
		self.createConfigList()

		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Save"))
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"],
			{
				"ok": self.save,
				"cancel": self.exit,
				"left": self.keyLeft,
				"right": self.keyRight,
				"down": self.keyDown,
				"up": self.keyUp,
				"red": self.exit,
				"green": self.save,
			}, -1)

	def createConfigList(self):
		list = []
		list.append(getConfigListEntry(_("Skin color"), config.plugins.SatdreamgrTranspBA.SkinColor))
		self["config"].list = list
		self["config"].l.setList(list)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.createConfigList()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createConfigList()

	def keyDown(self):
		#print "key down"
		self["config"].instance.moveSelection(self["config"].instance.moveDown)

	def keyUp(self):
		#print "key up"
		self["config"].instance.moveSelection(self["config"].instance.moveUp)

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
			else:
				pass

		try:
			skinSearchAndReplace = []
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#20000000":
				skinSearchAndReplace.append(["#20000000", config.plugins.SatdreamgrTranspBA.SkinColor.value])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00000000":
				skinSearchAndReplace.append(["#00000000", config.plugins.SatdreamgrTranspBA.SkinColor.value])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#50000000":
				skinSearchAndReplace.append(["#50000000", config.plugins.SatdreamgrTranspBA.SkinColor.value])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00102030":
				skinSearchAndReplace.append(["#00102030", config.plugins.SatdreamgrTranspBA.SkinColor.value])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00002222":
				skinSearchAndReplace.append(["#00002222", config.plugins.SatdreamgrTranspBA.SkinColor.value])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00080022":
				skinSearchAndReplace.append(["#00080022", config.plugins.SatdreamgrTranspBA.SkinColor.value])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00333333":
				skinSearchAndReplace.append(["#00333333", config.plugins.SatdreamgrTranspBA.SkinColor.value])

			SkinDefaultFile = open(self.SkinDefault, "r")
			SkinDefaultLines = SkinDefaultFile.readlines()
			SkinDefaultFile.close()

			PimpedLines = []
			for Line in SkinDefaultLines:
				for item in skinSearchAndReplace:
					Line = Line.replace(item[0], item[1])
				PimpedLines.append(Line)

			TmpFile = open(self.SkinDefaultTmp, "w")
			for Lines in PimpedLines:
				TmpFile.writelines(Lines)
			TmpFile.close()
			move(self.SkinDefaultTmp, self.SkinFinal)

			TmpFile = open(self.SkinDefaultTmp, "w")
			for Lines in PimpedLines:
				TmpFile.writelines(Lines)
			TmpFile.close()
			move(self.SkinDefaultTmp, self.SkinFinal)

		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)
		config.skin.primary_skin.setValue("Satdreamgr-HD-TranspBA/skin.xml")
		config.skin.save()
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Confirm your selection?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def restartGUI(self, answer):
		if answer is True:
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].cancel()
			else:
				pass
		self.close()
