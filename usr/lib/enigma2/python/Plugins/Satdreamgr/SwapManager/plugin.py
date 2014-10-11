from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.TextBox import TextBox
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigInteger, ConfigYesNo, ConfigText, ConfigElement
from Components.ConfigList import ConfigList
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, pathExists
from Components.MultiContent import MultiContentEntryText
import os
from SystemToolsText import SystemToolsTextBox, SystemToolsTextBox2, SystemToolsTextBoxEcm
from enigma import eTimer, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, gFont, gRGB, eListboxPythonMultiContent
#global vars#################################################################
entrylist = []
lengthList = [0,0,0,0]
###########################################################################
import gettext

try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/SwapManager/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def main(session,**kwargs):
    try:
     	session.open(SystemToolsSwap)
    except:
        print "[Hardware] Pluginexecution failed"

def autostart(reason,**kwargs):
    if reason == 0:
        print "[PluginMenu] no autostart"


def menu(menuid, **kwargs):
	if menuid == "cam":
		return [(_("Swap Manager"), main, "swapmanager_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Swap Manager"), description = _("Swap Manager"), where = PluginDescriptor.WHERE_MENU, fnc = menu)

class SystemToolsSwap(Screen):
	skin = """
	<screen name="Swap Manager" position="center,center" size="670,522" title="Swap files Manager">
		<widget name="entries" position="10,10" size="650,466" itemHeight="45" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="130,482" size="140,40" alphatest="on" />
		<widget name="key_red" position="130,482" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="400,482" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="400,482" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""

	def __init__(self, session):
		self.skin = SystemToolsSwap.skin
		Screen.__init__(self, session)
		self.list = []
		
		self.name = "Swap Files Manager"
		self.onShown.append(self.setWindowTitle)
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))
				
		self["actions"] = ActionMap(["OkCancelActions", "WizardActions", "ColorActions"],
		{
			"ok": self.go,
			"cancel": self.cancel,
			"red": self.cancel,			
			"green": self.go,
		}, -1)
		
		self.list.append((_("Info Swap "), "com_swapone"))
		self.list.append((_("Deactivating Swap"), "com_swapten"))
		self.list.append((_("Creating swap file on hdd"), "com_swaptwo"))
		self.list.append((_("Activate swap on HDD"), "com_swapsix"))
		self.list.append((_("Creating swap file on usb"), "com_swapfour"))
		self.list.append((_("Activate swap on USB"), "com_swapeight"))
		self.list.append((_("Creating swap file on cf"), "com_swaptree"))
		self.list.append((_("Activate swap on CF"), "com_swapseven"))
		self.list.append((_("Exit"), "exit"))
		self["entries"] = MenuList(self.list)

	def go(self):
		returnValue = self["entries"].l.getCurrentSelection()[1]
		print "\n[SystemToolsSwap] returnValue: " + returnValue + "\n"
		
		if returnValue is not None:
			if returnValue is "com_swapone":
				title = _("Info Swap")
				msg = self.aktswapscreen()
				self.session.open(SystemToolsTextBox, msg, title)
				
			elif returnValue is "com_swaptwo":
				msg = _("Please wait : Creating swap File on hdd")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.createswaphdd)				
				self.activityTimer.start(100, False)

			elif returnValue is "com_swaptree":
				msg = _("Please wait : Creating swap File on cf")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.createswapcf)				
				self.activityTimer.start(100, False)
				
			elif returnValue is "com_swapfour":
				msg = _("Please wait : Creating swap File on usb")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.activityTimer = eTimer()
				self.activityTimer.timeout.get().append(self.createswapusb)				
				self.activityTimer.start(100, False)

			elif returnValue is "com_swapsix":
				self.activateswaphdd()
				
			elif returnValue is "com_swapseven":
				self.activateswapcf()
				
			elif returnValue is "com_swapeight":
				self.activateswapusb()
				
			elif returnValue is "com_swapten":
				msg = _("Swap is Deactivated")
				self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab")
					
			else:
				print "\n[SystemToolsSwap] cancel\n"
				self.close(None)

	def readFile(self, filename):
		mounts = open(filename)
		msg = mounts.read().strip()
		mounts.close()
		return msg

	def aktswapscreen(self):
		swapentrylist = []
		if fileExists("/proc/swaps"):
			aktifswapfile = open("/proc/swaps", "r")
			counter = 0
			for line in aktifswapfile:
					if line[0] != "\n":
						entry = line.split()
						global lenghtList
						if len(entry[0]) > lengthList[0]:
							lengthList[0] = len(entry[0])
						if len(entry[1]) > lengthList[1]:
							lengthList[1] = len(entry[1])
						if len(entry[2]) > lengthList[2]:
							lengthList[2] = len(entry[2])					
						if len(entry[3]) > lengthList[3]:
							lengthList[3] = len(entry[3])
						counter = counter+1
						if counter >= 2:
							swapentrylist.append(' '.join(["Filename:", entry[0]]))
							swapentrylist.append(' '.join(["Type    :", entry[1]]))
							swapentrylist.append(' '.join(["Size    :", entry[2]]))
							swapentrylist.append(' '.join(["Used    :", entry[3]]))
			if swapentrylist != []:
				return '\n'.join(swapentrylist)
			else:
				return _("Swapfile is Not Activated !")
		else:
			return "SwapFile is Not Activated ! or /proc/swaps is missing"		
	
	def createswapcf(self):
		self.activityTimer.stop()
		del self.activityTimer
		if fileExists("/media/cf/swapfile"):
			msg = _("Swap File was already created ! You can activate the SWAP on CF if not done yet")
			self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			self.mbox.close()
		else:
			if pathExists("/media/cf"):
				os.system('sleep 1')
				os.system('dd if=/dev/zero of=/media/cf/swapfile bs=1048576 count=128; mkswap /media/cf/swapfile')
				os.system('sleep 1')
				msg = _("Done! You can now activate the SWAP on CF")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()
			else:
				msg = _("No compact flash mounted on /media/cf")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()

	def createswaphdd(self):
		self.activityTimer.stop()
		del self.activityTimer
		if fileExists("/media/hdd/swapfile"):
			msg = _("Swap File was already created ! You can activate the SWAP on HDD if not done yet")
			self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			self.mbox.close()
		else:
			if pathExists("/media/hdd"):
				os.system('sleep 1')
				os.system('dd if=/dev/zero of=/media/hdd/swapfile bs=1048576 count=128; mkswap /media/hdd/swapfile')
				os.system('sleep 1')
				msg = _("Done! You can now activate the SWAP on HDD")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()
			else:
				msg = _("No hard drive mounted on /media/hdd")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()				

	def createswapusb(self):
		self.activityTimer.stop()
		del self.activityTimer
		if fileExists("/media/usb/swapfile"):
			msg = _("Swap File was already created ! You can activate the SWAP on USB if not done yet")
			self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			self.mbox.close()
		else:
			if pathExists("/media/usb"):
				os.system('sleep 1')
				os.system('dd if=/dev/zero of=/media/usb/swapfile bs=1048576 count=128; mkswap /media/usb/swapfile')
				os.system('sleep 1')
				msg = _("Done! You can now activate the SWAP on USB")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()
			else:
				msg = _("No usb stick mounted on /media/usb")
				self.mbox2 = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
				self.mbox.close()

	def activateswaphdd(self):
		if fileExists("/media/hdd/swapfile"):
			os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab; swapon /media/hdd/swapfile")
			os.system("sed -i '/hdd\/swapfile/d' /etc/fstab; echo -e '/media/hdd/swapfile swap swap defaults 0 0' >> /etc/fstab")
			msg = _("Swap is activated on HDD")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else:
			msg = (_("There is no swap file found on HDD. Create it first"))
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)

	def activateswapcf(self):
		if fileExists("/media/cf/swapfile"):
			os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab; swapon /media/cf/swapfile")
			os.system("sed -i '/cf\/swapfile/d' /etc/fstab; echo -e '/media/cf/swapfile swap swap defaults 0 0' >> /etc/fstab")
			msg = _("Swap is activated on CF")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else:
			msg = (_("There is no swap file found on CF. Create it first"))
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			
	def activateswapusb(self):
		if fileExists("/media/usb/swapfile"):
			os.system("swapoff -a; sed -i '\/swapfile/d' /etc/fstab; swapon /media/usb/swapfile")
			os.system("sed -i '/usb\/swapfile/d' /etc/fstab; echo -e '/media/usb/swapfile swap swap defaults 0 0' >> /etc/fstab")
			msg = _("Swap is activated on USB")
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else:
			msg = (_("There is no swap file found on USB. Create it first"))
			self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
			
	def prombt(self, com):
		self.session.open(Console,_("start shell com: %s") % (com), ["%s" % com])

	def prombtbox(self, com):	
		self.session.open(ConsoleBox,_("start shell com: %s") % (com), ["%s" % com])

	
	def setWindowTitle(self):
		self.setTitle(self.name)
	
	def cancel(self):
		print "\n[SystemToolsSwap] cancel\n"
		self.close()

###########################################################################
