from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.InfoBar import InfoBar
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.EventView import EventViewSimple
from Components.ActionMap import ActionMap
from Components.FileList import FileList
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Components.config import config, ConfigSubsection, ConfigText
from Tools.Directories import fileExists, pathExists
from ServiceReference import ServiceReference
from FileList import FileList as FileList
from Screens.InputBox import InputBox
from enigma import eConsoleAppContainer, eServiceReference, ePicLoad, getDesktop, eServiceCenter
from os import system as os_system
from os import stat as os_stat
from os import walk as os_walk
from os import popen as os_popen
from os import rename as os_rename
from os import mkdir as os_mkdir
from os import path as os_path
from os import listdir as os_listdir
from time import strftime as time_strftime
from time import localtime as time_localtime
import gettext
config.plugins.ExFiles = ConfigSubsection()
config.plugins.ExFiles.Execute = ConfigText(default="/")
config.plugins.ExFiles.Filtre = ConfigText(default="off")
try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Manipulate/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def main(session,**kwargs):
    try:
     	session.open(PluginStart)
    except:
        print "[ArchivesExplorer] Pluginexecution failed"

def menu(menuid, **kwargs):
	if menuid == "cam":
		return [(_("Archives Explorer"), main, "archives_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Archives Explorer"), description = _("Install your ipk.tar.gz..."), where = PluginDescriptor.WHERE_MENU, fnc = menu)

explorer_main = """<screen name="PluginStart" position="center,center" size="600,405" >
                   <widget name="myliste" itemHeight="35" position="20,10" size="580,350" font="Regular;22" scrollbarMode="showOnDemand" transparent="1" zPosition="9"/>
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/red.png" position="80,370" size="32,32" zPosition="1" alphatest="blend"/>
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/green.png" position="240,370" size="32,32" zPosition="1" alphatest="blend"/>
                    <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/blue.png" position="400,370" size="32,32" zPosition="1" alphatest="blend"/>
                   <widget name="key_red" position="110,370" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                   <widget name="key_green" position="270,370" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                    <widget name="key_blue" position="430,370" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                   </screen>"""

class PluginStart(Screen):
	def __init__(self, session, args = None):
		self.skin = explorer_main
		Screen.__init__(self, session)
		self.sesion = session
		self.altservice = self.session.nav.getCurrentlyPlayingServiceReference()
		if pathExists(config.plugins.ExFiles.Execute.value):
			StartP = config.plugins.ExFiles.Execute.value
		else:
			StartP = None
		if (config.plugins.ExFiles.Filtre.value == "off"):
			self.Filtre = False
			self["myliste"] = FileList(StartP)
 		self["key_red"] = Label(_("Delete"))
 		self["key_green"] = Label(_("Info"))
  		self["key_blue"] = Label(_("Ok"))
		self["actions"] = ActionMap(["SetupActions", "WizardActions", "DirectionActions", "ColorActions", "MenuActions", "EPGSelectActions", "InfobarActions"],
		{
			"ok": self.ok,
			"back": self.explExit,
			"red": self.ExecDelete,
			"left": self.left,
			"right": self.right,
			"green": self.about,
			"blue": self.ok,
			"up": self.up,
			"down": self.down,
		}, -1)

	def about(self):
		self.session.open(AboutScreen)

	def up(self):
		self["myliste"].up()
		self.UpDownList()

	def down(self):
		self["myliste"].down()
		self.UpDownList()

	def left(self):
		self["myliste"].pageUp()
		self.UpDownList()

	def right(self):
		self["myliste"].pageDown()
		self.UpDownList()

	def ok(self):
		if self["myliste"].canDescent():
			self["myliste"].descent()
			self.UpDownList()
		else:
			filename = self["myliste"].getCurrentDirectory() + self["myliste"].getFilename()
			testFileName = self["myliste"].getFilename()
			testFileName = testFileName.lower()
			if filename != None:
				if testFileName.endswith(".bootlogo.tar.gz"):
					self.commando = ["mount -rw /boot -o remount", "sleep 3","tar -xzvf " + filename + " -C /", "mount -ro /boot -o remount"]
					askList = [(_("Cancel"), "NO"),(_("Install new bootlogo..."), "ExecB")]
					dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_("Bootlogo-package:\\n"+filename), list=askList)
					dei.setTitle(("."))
				elif testFileName.endswith(".tar.gz"):
					self.commando = [ "tar -xzvf " + filename + " -C /" ]
					askList = [(_("Cancel"), "NO"),(_("Install this package"), "ExecA")]
					dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_("GZ-package:\\n"+filename), list=askList)
					dei.setTitle(("."))
				elif testFileName.endswith(".tar.bz2"):
					self.commando = [ "tar -xjvf " + filename + " -C /" ]
					askList = [(_("Cancel"), "NO"),(_("Install this package"), "ExecA")]
					dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_("BZ2-package:\\n"+filename), list=askList)
					dei.setTitle(("."))
				elif testFileName.endswith(".ipk"):
					if fileExists("/usr/bin/opkg"):
						self.commando = [ "opkg install " + filename ]
					else:
						self.commando = [ "ipkg install " + filename ]
					askList = [(_("Cancel"), "NO"),(_("Install this package"), "ExecA")]
					dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_("\n"+filename), list=askList)
					dei.setTitle(("."))

				elif testFileName.endswith(".sh"):
					self.commando = [ filename ]
					self.chmodexec = [ "chmod 755 " + filename ]
					askList = [(_("Cancel"), "NO"),(_("View this shell-script"), "ExecC"),(_("Start execution"), "ExecA"),(_("Chmod 755 this file"), "Chmod")]
					self.session.openWithCallback(self.SysExecution, ChoiceBox, title= (_("Do you want to execute?\\n") +filename), list=askList)

				elif testFileName.endswith(".info")  or (testFileName.endswith(".log")) or (testFileName.endswith(".py")) or (testFileName.endswith(".xml")):
					self.commando = [ filename ]
					askList = [(_("Cancel"), "NO"),(_("View this File"), "ExecC")]
					self.session.openWithCallback(self.SysExecution, ChoiceBox, title= (_("Do you want to execute?\\n") +filename), list=askList)

				elif (testFileName.endswith(".jpg")) or (testFileName.endswith(".jpeg")) or (testFileName.endswith(".jpe")) or (testFileName.endswith(".png")) or (testFileName.endswith(".bmp")):
					if self["myliste"].getSelectionIndex()!=0:
						Pdir = self["myliste"].getCurrentDirectory()
						self.session.open(PictureExplorer, filename, Pdir)

	def SysExecution(self, answer):
		global PicPlayerAviable
		answer = answer and answer[1]
		if answer == "ExecA":
			self.session.open(Console, cmdlist = [ self.commando[0] ])
		elif answer == "ExecB":
			self.session.open(Console, cmdlist = self.commando)
		elif answer == "Chmod":
			self.session.open(Console, cmdlist = self.chmodexec)

		elif answer == "ExecC":
			yfile=os_stat(self.commando[0])
			if (yfile.st_size < 61440):
				self.session.open(TextExit, self.commando[0])

	def UpDownList(self):
		try:
			if self.Filtre:
				self.setTitle(_("[Media files] " + self["myliste"].getCurrentDirectory()))
			else:
				self.setTitle(_("[All files] " + self["myliste"].getCurrentDirectory()))
		except:
			self.setTitle(_("Archives Explorer"))

	def explExit(self):
		self.session.nav.playService(self.altservice)
		try:
			if self.Filtre:
				config.plugins.ExFiles.Filtre.value = "on"
			else:
				config.plugins.ExFiles.Filtre.value = "off"
			config.plugins.ExFiles.Filtre.save()
		except:
			pass
		self.close()

	def ExecDelete(self):
		if not(self["myliste"].canDescent()):
			DELfilename = self["myliste"].getCurrentDirectory() + self["myliste"].getFilename()
			dei = self.session.openWithCallback(self.callbackExecDelete,MessageBox, (_("Do you realy want to Delete:\n") +DELfilename), MessageBox.TYPE_YESNO)
			dei.setTitle(_("Delete file..."))

		elif (self["myliste"].getSelectionIndex()!=0) and (self["myliste"].canDescent()):
			DELDIR = self["myliste"].getSelection()[0]
			dei = self.session.openWithCallback(self.callbackDelDir,MessageBox, (_("Do you realy want to Delete:\n") +DELDIR+'\n\nYou do it at your own risk!'), MessageBox.TYPE_YESNO)
			dei.setTitle(_("Delete Directory..."))

	def callbackExecDelete(self, answer):
		if answer is True:
			DELfilename = self["myliste"].getCurrentDirectory() + self["myliste"].getFilename()
			order = 'rm -f \"' + DELfilename + '\"'
			try:
				os_system(order)
				self["myliste"].refresh()
			except:
				dei = self.session.open(MessageBox,_("%s \nFAILED!" % order), MessageBox.TYPE_ERROR)
				dei.setTitle(_("Manipulate Files"))
				self["myliste"].refresh()

	def callbackDelDir(self, answer):
		if answer is True:
			DELDIR = self["myliste"].getSelection()[0]
			order = 'rm -r \"' + DELDIR + '\"'
			try:
				os_system(order)
				self["myliste"].refresh()
			except:
				dei = self.session.open(MessageBox,_("%s \nFAILED!" % order), MessageBox.TYPE_ERROR)
				dei.setTitle(_("Manipulate Files"))
				self["myliste"].refresh()


class TextExit(Screen):
	try:
		sz_w = getDesktop(0).size().width()
	except:
		sz_w = 720
	if (sz_w == 1280):
			skin = """
			<screen position="center,77" size="900,450" >
			<widget name="filedata" position="2,0" size="896,450" itemHeight="25"/>
			</screen>"""
	else:
		skin = """
		<screen position="center,77" size="620,450" >
		<widget name="filedata" position="0,0" size="620,450" itemHeight="25"/>
		</screen>"""

	def __init__(self, session, file):
		self.skin = TextExit.skin
		Screen.__init__(self, session)
		self.session = session
		self.file_name = file
		self.list = []
  		self.setup_title = _("Info")
  		self.onLayoutFinish.append(self.layoutFinished)
		self["filedata"] = MenuList(self.list)
		self["actions"] = ActionMap(["WizardActions"],
		{
            "back": self.close,
            "ok": self.close
		}, -1)
		self.GetFileData(file)

	def layoutFinished(self):
		self.setTitle(self.setup_title)


	def GetFileData(self, fx):
		try:
			flines = open(fx, "r")
			for line in flines:
				self.list.append(line)
			flines.close()
			self.setTitle(fx)
		except:
			pass
			self.close()

class PictureExplorer(Screen):
	try:
		sz_w = getDesktop(0).size().width()
	except:
		sz_w = 720
	if (sz_w == 1280):
			skin="""
				<screen flags="wfNoBorder" position="0,0" size="1280,720" title="Picture-Explorer" backgroundColor="#00121214">
				<widget name="Picture" position="0,0" size="1280,720" zPosition="1" alphatest="on" />
				<widget name="State" font="Regular;20" halign="center" position="0,650" size="1280,70" backgroundColor="#01080911" foregroundColor="#fcc000" transparent="0" zPosition="9"/>
				</screen>"""

	else:
		skin="""
			<screen flags="wfNoBorder" position="0,0" size="720,576" title="Picture-Explorer" backgroundColor="#00121214">
			<widget name="Picture" position="0,0" size="720,576" zPosition="1" alphatest="on" />
			<widget name="State" font="Regular;20" halign="center" position="0,506" size="720,70" backgroundColor="#01080911" foregroundColor="#fcc000" transparent="0" zPosition="9"/>
			</screen>"""

	def __init__(self, session, whatPic = None, whatDir = None):
		self.skin = PictureExplorer.skin
		Screen.__init__(self, session)
		self.session = session
		self.whatPic = whatPic
		self.whatDir = whatDir
		self.picList = []
		self.Pindex = 0
		self.EXscale = (AVSwitch().getFramebufferScale())
		self.EXpicload = ePicLoad()
		self["Picture"] = Pixmap()
		self["State"] = Label(_('loading... '+self.whatPic))
		self["actions"] = ActionMap(["WizardActions", "DirectionActions"],
		{
			"ok": self.info,
			"back": self.close,
			"up": self.info,
			"down": self.close,
			"left": self.Pleft,
			"right": self.Pright
		}, -1)
		self.EXpicload.PictureData.get().append(self.DecodeAction)
		self.onLayoutFinish.append(self.Show_Picture)

	def Show_Picture(self):
		if self.whatPic is not None:
			self.EXpicload.setPara([self["Picture"].instance.size().width(), self["Picture"].instance.size().height(), self.EXscale[0], self.EXscale[1], 0, 1, "#002C2C39"])
			self.EXpicload.startDecode(self.whatPic)
		if self.whatDir is not None:
			pidx = 0
			for root, dirs, files in os_walk(self.whatDir ):
				for name in files:
					if name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".Jpg") or name.endswith(".Jpeg") or name.endswith(".JPG") or name.endswith(".JPEG"):
						self.picList.append(name)
						if name in self.whatPic:
							self.Pindex = pidx
						pidx = pidx + 1
			files.sort()

	def DecodeAction(self, pictureInfo=""):
		if self.whatPic is not None:
			self["State"].setText(_("ready..."))
			self["State"].visible = False
			ptr = self.EXpicload.getData()
			self["Picture"].instance.setPixmap(ptr)

	def Pright(self):
		if len(self.picList)>2:
			if self.Pindex<(len(self.picList)-1):
				self.Pindex = self.Pindex + 1
				self.whatPic = self.whatDir + str(self.picList[self.Pindex])
				self["State"].visible = True
				self["State"].setText(_('loading... '+self.whatPic))
				self.EXpicload.startDecode(self.whatPic)
			else:
				self["State"].setText(_("wait..."))
				self["State"].visible = False
				self.session.open(MessageBox,_('No more picture-files.'), MessageBox.TYPE_INFO)

	def Pleft(self):
		if len(self.picList)>2:
			if self.Pindex>0:
				self.Pindex = self.Pindex - 1
				self.whatPic = self.whatDir + str(self.picList[self.Pindex])
				self["State"].visible = True
				self["State"].setText(_('loading... '+self.whatPic))
				self.EXpicload.startDecode(self.whatPic)
			else:
				self["State"].setText(_("wait..."))
				self["State"].visible = False
				self.session.open(MessageBox,_('No more picture-files.'), MessageBox.TYPE_INFO)

	def info(self):
		if self["State"].visible:
			self["State"].setText(_("wait..."))
			self["State"].visible = False
		else:
			self["State"].visible = True
			self["State"].setText(_(self.whatPic))


class AboutScreen(Screen):
	try:
		sz_w = getDesktop(0).size().width()
	except:
		sz_w = 720
	if (sz_w == 1280):
		skin = """
		<screen position="0,0" size="1280,720" title="About" >
		<widget name="text" position="100,140" size="520,420" font="Regular;24" transparent="1"/>
		</screen>"""
	else:
		skin = """
		<screen position="center,center" size="550,320" title="About" >
		<widget name="text" position="0,10" size="550,320" font="Regular;24" />
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		info=(_("Informations \n\n Delete your file \n Install Your Files .tar.gz--tar.bz2 --.ipk \n View your .png.jpg.jpeg Images \n View and execute your script shell .sh \n Permissions 755 for your script .sh \n Install your bootlogo (bootlogo.tar.gz)  \n ---------------------------  \n By SatDreamGR\n\n http://www.satdreamgr.com\n ---------------------------"))
		self["text"] = ScrollLabel(info)
		self["actions"] = ActionMap(["SetupActions"],
			{
				"ok": self.close,
				"cancel": self.close,

			}, -1)
