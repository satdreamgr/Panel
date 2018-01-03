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
from Components.Label import Label
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from shutil import move, copy
import re
import gettext
try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass
#############################################################
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
#######################################################################
def main(session,**kwargs):
    try:
     	session.open(MyMenuSKIN)
    except:
        print "[Satdreamgr-HD-TranspBA] Pluginexecution failed"

def autostart(reason,**kwargs):
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
	<screen name="SatdreamgrTranspBA" position="center,center"  size="620,520" title="Configuration tool for Satdreamgr TranspBA skin" >
	<eLabel font="Regular; 22" foregroundColor="#00ffffff" backgroundColor="#20000000" halign="left" position="100,490" size="250,33" text="Exit" transparent="1" />
	<eLabel font="Regular; 22" foregroundColor="#00ffffff" backgroundColor="#20000000" halign="left" position="300,490" size="250,33" text="Ok" transparent="1" />
	<widget name="menu" position="20,20" scrollbarMode="showOnDemand" size="590,480" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		Screen.setTitle(self, _("Configuration tool for Satdreamgr TranspBA skin"))
		menu = []
		menu.append((_("Change Color"), ))
		menu.append((_("Change Color Satdreamgr-HD-TranspBA"),"skinhd"))
		menu.append((_(" "), ))		
		menu.append((_("Change Infobar"), ))
		menu.append((_("Simple Infobar Satdreamgr-HD-TranspBA"),"simple"))
		menu.append((_("Full Bottom Infobar Satdreamgr-HD-TranspBA"),"fullbottom"))
		menu.append((_("Full Infobar Satdreamgr-HD-TranspBA"),"full"))
		menu.append((_(" "), ))		
		menu.append((_("Weather in Infobar"), ))		
		menu.append((_("Weather ON in Infobar"),"weatheron"))			
		menu.append((_("Weather OFF in Infobar"),"weatheroff"))					
		self["menu"] = MenuList(menu)
		self["actions"] = ActionMap(["WizardActions", "DirectionActions"],{"ok": self.go,"back": self.close,}, -1)

    	def go(self):
    		if self["menu"].l.getCurrentSelection() is not None:
        		choice = self["menu"].l.getCurrentSelection()[1]
		if choice == "skinhd":
			               self.session.open(SatdreamgrTranspBA)
		if choice == "full":
		                   self.session.openWithCallback(self.FullInfobar, MessageBox,_("Confirm your selection ?"), MessageBox.TYPE_YESNO)
		if choice == "fullbottom":
		                   self.session.openWithCallback(self.FullBottomInfobar, MessageBox,_("Confirm your selection ?"), MessageBox.TYPE_YESNO)
		if choice == "simple":
		                   self.session.openWithCallback(self.SimpleInfobar, MessageBox,_("Confirm your selection ?"), MessageBox.TYPE_YESNO)
		if choice == "weatheron":
		                   self.session.openWithCallback(self.WeatherONInfobar, MessageBox,_("Confirm your selection ?"), MessageBox.TYPE_YESNO)	
		if choice == "weatheroff":
		                   self.session.openWithCallback(self.WeatherOFFInfobar, MessageBox,_("Confirm your selection ?"), MessageBox.TYPE_YESNO)		                   	                   
		                   
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
			
#######################################################################

class SatdreamgrTranspBA(ConfigListScreen, Screen):
	skin = """
	<screen name="SatdreamgrTranspBA" position="center,center"  size="620,520" title="Edit color">
	<eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#20000000" halign="left" position="37,460" size="250,33" text="Cancel" transparent="1" />
	<eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#20000000" halign="left" position="187,460" size="250,33" text="Save" transparent="1" />
	<eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#20000000" halign="left" position="487,460" size="250,33" text="Information" transparent="1" />
	<widget name="config" position="20,20" scrollbarMode="showOnDemand" size="590,380" transparent="1" />
	<eLabel position="470,455" size="5,40" backgroundColor="#000000ff" />
	<eLabel position="170,455" size="5,40" backgroundColor="#0000ff00" />
	<eLabel position="20,455" size="5,40" backgroundColor="#00ff0000" />
	</screen>"""

	def __init__(self, session, args = None, picPath = None):
		Screen.__init__(self, session)
		self.session = session
		Screen.setTitle(self, _("Edit color"))
		self.myskinpath = "/etc/enigma2/"
		self.SkinDefault = self.myskinpath + "skin_user_Satdreamgr-HD-TranspBA.xml"
		self.SkinDefaultTmp = self.SkinDefault + ".TMP"
		self.myskinpathout = "/etc/enigma2/"
		self.SkinFinal = self.myskinpathout + "skin_user_Satdreamgr-HD-TranspBA.xml"
		ConfigListScreen.__init__(self, [])
		self.createConfigList()
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)

	def createConfigList(self):
		list = []
		list.append(getConfigListEntry(_("Choose a color"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("   Main Color"), config.plugins.SatdreamgrTranspBA.SkinColor))

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

	def showInfo(self):
		self.session.open(MessageBox, _("  "), MessageBox.TYPE_INFO)

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
        			x[1].save()
			else:
       				pass

		try:

			skinSearchAndReplace = []
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#20000000":
				skinSearchAndReplace.append(["#20000000", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#00000000":
				skinSearchAndReplace.append(["#00000000", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#50000000":
				skinSearchAndReplace.append(["#50000000", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#00102030":
				skinSearchAndReplace.append(["#00102030", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#00002222":
				skinSearchAndReplace.append(["#00002222", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#00080022":
				skinSearchAndReplace.append(["#00080022", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
			if config.plugins.SatdreamgrTranspBA.SkinColor.value !="#00333333":
				skinSearchAndReplace.append(["#00333333", config.plugins.SatdreamgrTranspBA.SkinColor.value ])
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
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Confirm your selection ?"), MessageBox.TYPE_YESNO)
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
