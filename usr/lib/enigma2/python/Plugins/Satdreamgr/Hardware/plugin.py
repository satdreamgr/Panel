import os
import urllib
from Components.ScrollLabel import ScrollLabel
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

try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def main(session,**kwargs):
    try:
     	session.open(HardwareInfo)
    except:
        print "[Hardware] Pluginexecution failed"

def autostart(reason,**kwargs):
    if reason == 0:
        print "[PluginMenu] no autostart"


def menu(menuid, **kwargs):
	if menuid == "cam":
		return [(_("Hardware Info"), main, "harware_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Hardware Info"), description = _("Hardware Info"), where = PluginDescriptor.WHERE_MENU, fnc = menu)



hardware_main = """<screen name="HardwareInfo" position="center,center" size="600,405" >
                   <widget name="menu" itemHeight="35" position="20,10" size="580,330" scrollbarMode="showOnDemand" transparent="1" zPosition="9"/>
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/red.png" position="80,360" size="32,32" zPosition="1" alphatest="blend"/>
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/green.png" position="240,360" size="32,32" zPosition="1" alphatest="blend"/>
                   <widget name="key_red" position="110,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                   <widget name="key_green" position="270,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                   </screen>"""

class HardwareInfo(Screen):

	def __init__(self, session):
		self.skin = hardware_main
		Screen.__init__(self, session)
		self.session = session
		menu = []
		menu.append((_("System Information"),"system"))
		menu.append((_("Netstat"),"netstat"))
		menu.append((_("Ifconfig"),"ifconfig"))
		menu.append((_("Performence Internet"),"internet"))
		menu.append((_("V. SecondStage Loader"),"Second"))
		menu.append((_("ipkg list installed"),"listinstalled"))
		menu.append((_("Show All Devices"),"devices"))
		menu.append((_("Show Mounts"),"mounts"))
		menu.append((_("Remove crashlogs"),"crashlogs"))
        	self["menu"] = MenuList(menu)
        	self["key_red"] = Label(_("Exit"))
        	self["key_green"] = Label(_("Ok"))
        	self['info'] = Label()
        	self.setup_title = _("Hardware Info")
        	self.onLayoutFinish.append(self.layoutFinished)
        	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "WizardActions", "DirectionActions"],{"ok": self.go, "red": self.close, "green": self.go, "back": self.close,}, -1)
    	def go(self):
    		if self["menu"].l.getCurrentSelection() is not None:
        		choice = self["menu"].l.getCurrentSelection()[1]
			if choice == "system":
                         self.session.open(Info_Box, _(ScanSysem_mem()), MessageBox.TYPE_INFO)
			if choice == "netstat":
				self.session.open(Console, _("Netstat"),["netstat | grep tcp && netstat | grep unix"])
			if choice == "ifconfig":
				self.session.open(Console, _("Ifconfig"),["ifconfig"])
			if choice == "internet":
				self.session.open(Console, _("Performence Internet"),["ping -c 1 www.satdreamgr.com && ping -c 1 www.google.com"])
			if choice == "Second":
				self.session.open(Console, _("Your Version SecondStage Loader Installed"),["opkg list | grep second"])

			if choice == "listinstalled":
				self.session.open(Console, _("opkg list installed"),["opkg list_installed"])
			if choice == "devices":
				self.session.open(Console, _("Info All Devices"),["df -h"])
			if choice == "mounts":
				self.session.open(Console, _("Info Mounts Devices"),["mount"])
			if choice == "crashlogs":
				self.session.open(Console, _("Remove crashlogs /media/hdd"),["rm -rf /media/hdd/enigma2_crash*"])



	def layoutFinished(self):
		self.setTitle(self.setup_title)


class Info_Box(MessageBox):
	try:
		sz_w = getDesktop(0).size().width()
	except:
		sz_w = 720
	if (sz_w == 1280):
		skin = """
		<screen position="center,center" size="600,580" title="Info">
		<widget name="list" position="0,0" size="600,580" transparent="1" scrollbarMode="showOnDemand" zPosition="9"/>
		<widget name="text" position="20,0" size="600,580" font="Regular;20" transparent="1" zPosition="9" halign="left" valign="center" />
		</screen>"""
	else:
		skin = """
		<screen backgroundColor="#00000030" flags="wfNoBorder" position="center,center" size="600,400" title="Info">
		<widget name="list" position="0,0" size="600,380" transparent="1" scrollbarMode="showOnDemand" zPosition="9"/>
		<widget name="text" position="20,0" size="600,380" font="Regular;22" transparent="1" foregroundColor="#FFC000" zPosition="9" halign="left" valign="center" />
		</screen>"""

	def __init__(self, session, text = "", type = MessageBox.TYPE_INFO , timeout = -1, close_on_any_key = True, default = True):
		MessageBox.__init__(self, session, text, type, timeout, close_on_any_key, default)


def ScanSysem_mem():
	try:
		ret = "System information:\n"
		out_line = os_popen("uptime").readline()
		ret = ret  + "at" + out_line + "\n"
		out_lines = []
		out_lines = os_popen("cat /proc/meminfo").readlines()
		for lidx in range(len(out_lines)):
			tstLine = out_lines[lidx].split()
			if "MemTotal:" in tstLine:
				ret = ret + out_lines[lidx]
			if "MemFree:" in tstLine:
				ret = ret + out_lines[lidx]

			if "SwapTotal:" in tstLine:
				ret = ret + out_lines[lidx]

			if "SwapFree:" in tstLine:
				ret = ret + out_lines[lidx]
			if "SwapCached: " in tstLine:
				ret = ret + out_lines[lidx]

			if "Buffers:" in tstLine:
				ret = ret + out_lines[lidx]

			if "Cached:" in tstLine:
				ret = ret + out_lines[lidx]

			if "Active:" in tstLine:
				ret = ret + out_lines[lidx]

			if "Inactive:" in tstLine:
				ret = ret + out_lines[lidx]


			elif "Mapped:" in tstLine:
				ret = ret + out_lines[lidx] + "...........\n"
		out_lines = []

		out_line = os_popen("opkg list_installed | grep dvb-modules").readline() + "...........\n"
		ret = ret + out_line

		out_lines = []
		out_lines = os_popen("df -h").readlines()
		fl_da = False
		cf_da = False
		usb_da = False
		hdd_da = False
		for lidx in range(len(out_lines)-1):
			tstLine = out_lines[lidx].split()
			if (("/boot/mnt/flash" in tstLine) or ("/boot" in tstLine)) and not fl_da:
				fl_da = True
				ret = ret + "Flash  total: " + tstLine[1] + "  free: " + tstLine[3] + "  used: " + tstLine[4] + "\n"
			elif ("/media/cf" in tstLine) and not cf_da:
				cf_da = True
				ret = ret + tstLine[5] + "  total: " + tstLine[1] + "  free: " + tstLine[3] + "  used: " + tstLine[4] + "\n"
			elif ("/media/usb" in tstLine) and not usb_da:
				usb_da = True
				ret = ret + tstLine[5] + "  total: " + tstLine[1] + "  free: " + tstLine[3] + "  used: " + tstLine[4] + "\n"
			elif ("/media/hdd" in tstLine) and not hdd_da:
				hdd_da = True
				ret = ret + tstLine[5] + "  total: " + tstLine[1] + "  free: " + tstLine[3] + "  used: " + tstLine[4] + "\n"

		ret = ret + "...........\n"
		out_lines = []
		out_lines = os_popen("cat /proc/stat").readlines()
		for lidx in range(len(out_lines)-1):
			tstLine = out_lines[lidx].split()
			if "procs_running" in tstLine:
				ret = ret + "Running processes: " + tstLine[1]

		return ret
	except:
		return "N/A"

