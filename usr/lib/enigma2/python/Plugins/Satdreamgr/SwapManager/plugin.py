
import os
from Components.Sources.List import List
from Components.Console import Console as CompConsole
from Screens.Console import Console
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
from Components.Sources.List import List
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Components.Input import Input
from Components.FileList import FileList
from Components.config import *
from Components.Harddisk import harddiskmanager, Harddisk
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.HardwareInfo import HardwareInfo
from Components.Pixmap import *
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap, HelpableActionMap
from Tools.Directories import resolveFilename, SCOPE_SYSETC, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN
from enigma import ePixmap, eTimer, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePoint
from Components.ConfigList import ConfigListScreen, ConfigList
from time import sleep
import time

import gettext

try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/SwapManager/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def main(session,**kwargs):
    try:
     	session.open(swap_manager)
    except:
        print "[Hardware] Pluginexecution failed"

def autostart(reason,**kwargs):
    if reason == 0:
        print "[PluginMenu] no autostart"


def menu(menuid, **kwargs):
	if menuid == "cam":
		return [(_("Swap Manager"), main, "Swap Manager", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Swap Manager"), description = _("Swap Manager"), where = PluginDescriptor.WHERE_MENU, fnc = menu)

class ListboxSys(MenuList):

    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 17))
        self.l.setFont(2, gFont('Regular', 15))
        self.l.setItemHeight(25)

swap_main = """<screen name="swap_manager" position="center,center" size="600,405"  >
               <widget name="list" position="10,10" size="580,60" scrollbarMode="showOnDemand" />
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/red.png" position="100,370" size="40,32" zPosition="1" alphatest="blend"/>
                   <eLabel position="150,370" size="100,32" font="Regular;22" text="Exit" transparent="1" zPosition="2"/>
                    <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/green.png" position="240,370" size="40,32" zPosition="1" alphatest="blend"/>
                    <eLabel position="290,370" size="100,32" font="Regular;22" text="Ok" transparent="1" zPosition="2"/>
               </screen>"""
swap_info = """<screen name="Swap Summary Info" position="center,center" size="800,405" >
               <eLabel text="Filename:" font="Regular;17" position="20,20" size="250,20" />
               <eLabel text="Type:" font="Regular;17" position="420,20" size="100,20" />
               <eLabel text="Size:" font="Regular;17" position="510,20" size="100,20" />
               <eLabel text="Used:" font="Regular;17" position="620,20" size="100,20"/>
               <eLabel text="Priority:" font="Regular;17" position="710,20" size="100,20" />
               <widget name="list" position="20,40" size="760,100" scrollbarMode="showOnDemand" zPosition="2"  />
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/red.png" position="100,370" size="40,32" zPosition="1" alphatest="blend"/>
                   <eLabel position="150,370" size="100,32" font="Regular;22" text="Exit" transparent="1" zPosition="2"/>
                    <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/yellow.png" position="240,370" size="40,32" zPosition="1" alphatest="blend"/>
                    <eLabel position="290,370" size="130,32" font="Regular;22" text="Delete" transparent="1" zPosition="2"/>
               </screen>"""
swap_create = """<screen name="Swap create" position="center,center" size="600,405" >
                 <widget name="config" position="10,10" size="580,50" zPosition="2" transparent="1" />
                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/red.png" position="100,370" size="40,32" zPosition="1" alphatest="blend"/>
                   <eLabel position="150,370" size="100,32" font="Regular;22" text="Exit" transparent="1" zPosition="2"/>
                    <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/green.png" position="240,370" size="40,32" zPosition="1" alphatest="blend"/>
                    <eLabel position="290,370" size="100,32" font="Regular;22" text="Create" transparent="1" zPosition="2"/>
                 </screen>"""

class swap_manager(Screen):
    def __init__(self, session):
        self.skin = swap_main
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.menuListAll = [('info', 'Swap info and delete'), ('create', 'Swap create')]
        self['list'] = ListboxSys(self.list)
        self['actions'] = ActionMap(['ColorActions',
         'SetupActions',
         'DirectionActions',
         'WizardActions'], {'green': self.selectedmenuitem,
         'red': self.close,
         'ok': self.selectedmenuitem,
         'cancel': self.close})
        self.onLayoutFinish.append(self.updatemenulist)


    def updatemenulist(self):
        self.list = []
        for x in self.menuListAll:
            item = [x[0]]
            item.append(MultiContentEntryText(pos=(25, 0), size=(260, 22), font=0, text=x[1]))
            self.list.append(item)

        self['list'].l.setList(self.list)

    def selectedmenuitem(self):
        selectedItem = self['list'].getCurrent()[0]
        if selectedItem == 'info':
            self.session.open(SwapInfo)
        elif selectedItem == 'create':
            self.session.open(SwapCreate)






class SwapInfo(Screen):

    def __init__(self, session):
        self.skin = swap_info
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys(self.list)
        self['actions'] = ActionMap(['ColorActions',
         'SetupActions',
         'DirectionActions',
         'WizardActions'], {'yellow': self.swapDeleteQuestion,
         'ok': self.close,
         'red': self.close,
         'cancel': self.close})
        self.onLayoutFinish.append(self.readSwapInfo)




    def readSwapInfo(self):
        self.list = []
        self['list'].show()
        filename = type = size = used = priority = ''
        try:
            f = open('/proc/swaps')
            content = f.read()
            f.close()
        except:
            content = ''

        item = []
        if content != '':
            contentInfo = content.split('\n')
            for line in contentInfo:
                if line.startswith('/'):
                    tmp = str(line).strip()
                    tmp = tmp.replace('\t', ' ')
                    while tmp.find('  ') != -1:
                        tmp = tmp.replace('  ', ' ')

                    filename = tmp.strip().split(' ')[0]
                    type = tmp.strip().split(' ')[1]
                    size = tmp.strip().split(' ')[2]
                    used = tmp.strip().split(' ')[3]
                    priority = tmp.strip().split(' ')[4]
                    item = [filename]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(380, 20), font=0, text=filename))
                    item.append(MultiContentEntryText(pos=(400, 0), size=(80, 20), font=0, text=type))
                    item.append(MultiContentEntryText(pos=(490, 0), size=(100, 20), font=0, text=size))
                    item.append(MultiContentEntryText(pos=(600, 0), size=(100, 20), font=0, text=used))
                    item.append(MultiContentEntryText(pos=(690, 0), size=(40, 20), font=0, text=priority))
                    self.list.append(item)

            self['list'].l.setList(self.list)
        else:
            item = ['No swapfile']
            item.append(MultiContentEntryText(pos=(0, 0), size=(380, 20), font=0, text='No swapfile'))
            item.append(MultiContentEntryText(pos=(400, 0), size=(80, 20), font=0, text='****'))
            item.append(MultiContentEntryText(pos=(490, 0), size=(100, 20), font=0, text='****'))
            item.append(MultiContentEntryText(pos=(600, 0), size=(100, 20), font=0, text='****'))
            item.append(MultiContentEntryText(pos=(690, 0), size=(40, 20), font=0, text='****'))
            self.list.append(item)
            self['list'].l.setList(self.list)

    def swapDeleteQuestion(self):
        selection = self['list'].getCurrent()[0]
        if str(selection) != 'No swapfile':
            self.session.openWithCallback(self.swapDelete, MessageBox, _('Really delete swap ?'))
        else:
            self.session.open(MessageBox, _('No swapfile for delete'), MessageBox.TYPE_INFO, 4)
            self.close()

    def swapDelete(self, answer):
        if answer:
            selection = self['list'].getCurrent()[0]
            if selection:
                tmp = selection
                os.system('swapoff %s' % tmp)
                os.system('rm %s' % tmp)
                info = 'Delete swap : ' + tmp
                self.deleteFstab(tmp)
                self.session.open(MessageBox, info, MessageBox.TYPE_INFO, 4)
                self.readSwapInfo()

    def deleteFstab(self, tmp):
        try:
            f = open('/etc/fstab', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content.split('\n')
        newline = ''
        if content != '':
            for line in contentInfo:
                if line.find(tmp) == -1:
                    if newline != '':
                        newline = newline + '\n' + line
                    else:
                        newline = line

        f = open('/etc/fstab', 'w')
        f.write(newline)
        f.close()



class SwapCreate(Screen):
    def __init__(self, session):
        self.skin = swap_create
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['config'] = ConfigList(self.list)
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'WizardActions'], {'left': self.keyLeft,
         'right': self.keyRight,
         'green': self.SwapCreate,
         'ok': self.SwapCreate,
         'red': self.exit,
         'cancel': self.exit}, -2)
        self.onLayoutFinish.append(self.SwapDefine)


    def keyLeft(self):
        self['config'].handleKey(KEY_LEFT)

    def keyRight(self):
        self['config'].handleKey(KEY_RIGHT)

    def mountDevices(self):
        mountPoints = []
        mountPoints.append('None')
        os.system('df -h > /tmp/tempinfo.tmp')
        if fileExists('/tmp/tempinfo.tmp'):
            f = open('/tmp/tempinfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == '/media/cf':
                    mountPoints.append('/media/cf')
                if parts[totsp] == '/media/sd':
                    mountPoints.append('/media/sd')
                if parts[totsp] == '/media/usb':
                    mountPoints.append('/media/usb')
                if parts[totsp] == '/media/ba':
                    mountPoints.append('/media/ba')
                if parts[totsp] == '/media/hdd':
                    mountPoints.append('/media/hdd')

            f.close()
            os.remove('/tmp/tempinfo.tmp')
        return mountPoints

    def SwapDefine(self):
        size = ['None',
         '32',
         '64',
         '128',
         '256',
         '512']
        selSize = ConfigSelection(default=size[0], choices=size)
        disk = self.mountDevices()
        selDisk = ConfigSelection(default=disk[0], choices=disk)
        self.list = []
        self.list.append(getConfigListEntry(_('Size: '), selSize))
        self.list.append(getConfigListEntry(_('Disk: '), selDisk))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def SwapCreate(self):
        self['config'].setCurrentIndex(0)
        swapSize = self['config'].getCurrent()[1].getText()
        self['config'].setCurrentIndex(1)
        swapPlace = self['config'].getCurrent()[1].getText()
        if swapPlace == 'None' or swapSize == 'None':
            info = 'Must set all parameters: Disk and Size'
            self.session.open(MessageBox, info, MessageBox.TYPE_INFO, 4)
            self.exit()
        else:
            ttt = str(time.time()).split('.')
            swapfileName = str(swapPlace) + '/swapfile_' + ttt[0]
            swapCommand = 'dd if=/dev/zero of=%s bs=1M count=%s' % (swapfileName, swapSize)
            os.system(swapCommand)
            os.system('mkswap %s' % swapfileName)
            os.system('swapon %s' % swapfileName)
            try:
                writeFstab('%s swap swap defaults 0 0\n' % swapfileName)
                info = 'Create swapfile : %s' % swapfileName
                self.session.open(MessageBox, info, MessageBox.TYPE_INFO, 4)
                self.exit()
            except:
                info = "Can't create swapfile : %s" % swapfileName
                self.session.open(MessageBox, info, MessageBox.TYPE_INFO, 4)
                self.exit()

    def exit(self):
        self.close()
