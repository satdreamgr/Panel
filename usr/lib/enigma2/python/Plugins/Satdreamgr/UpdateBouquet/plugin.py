from os import path, listdir
from Components.config import config
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.MenuList import MenuList
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Screens.Console import Console
import os, urllib
import gettext

url_sc = "/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/update.sh"
GSXML = "/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml"
GSBQ = "/etc/enigma2/userbouquet.greekstreamtv.tv"


try:
	cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/po', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass


def main(session,**kwargs):
    try:
     	session.open(UpdateBouquet)
    except:
        print "[UpdateBouquet] Pluginexecution failed"

def autostart(reason,**kwargs):
    if reason == 0:
        print "[UpdateBouquet] no autostart"


def menu(menuid, **kwargs):
	if menuid == "cam":
		return [(_("GreekStreamTV in Bouquets"), main, "update_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("GreekStreamTV in Bouquets"), description = _("Update Bouquet List"), where = PluginDescriptor.WHERE_MENU, fnc = menu)

class UpdateBouquet(Screen):
    skin = """
		<screen name="UpdateBouquet" position="center,center" size="600,405">
			<widget name="menu" itemHeight="35" position="10,10" size="580,140" scrollbarMode="showOnDemand" transparent="1" zPosition="9"/>
		</screen>
           """
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        menu = []
        if path.isdir("/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet"):
			menu.append((_("Create Bouquets List"), "create"))
			menu.append((_("Download & Udate Bouquets List "), "updatebq"))
			menu.append((_("About..."), "about"))
			self["menu"] = MenuList(menu)
			self["actions"] = ActionMap(["WizardActions", "DirectionActions"], {"ok": self.go,"back": self.close,}, -1)

    def go(self):
        if self["menu"].l.getCurrentSelection() is not None:
            choice = self["menu"].l.getCurrentSelection()[1]

        if choice == "about":
                tmpMessage = "For Informations and Questions please refer to www.satdreamgr.com forum.\n"
                tmpMessage += "\n\n"
                tmpMessage += "GreekStreamTV is free and source code included."
                self.session.open(MessageBox, tmpMessage, MessageBox.TYPE_INFO)

        elif choice == "create":
                self.session.openWithCallback(self.create, MessageBox,_("Confirm your selection, or exit"), MessageBox.TYPE_YESNO)

        elif choice == "updatebq":
			try:
				url = "http://sgcpm.com/livestream/stream.xml"
				f = urllib.urlopen(url)
				info = f.read()
				tmp = "/usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml"
				file = open(tmp, "w")
				file.write(info)
				file.close()
				print "[Testplugin]: download done ", url

			except IOError,e:
				print "[Testplugin]: I/O error!", e


			except IOError,e:
				print "[Testplugin]: I/O error!", e
			try:
				self.updatebq()
				from enigma import eDVBDB
				eDVBDB.getInstance().reloadBouquets()
				eDVBDB.getInstance().reloadServicelist()
				tmpMessage = "GreekStreamTV bouquet updated successfully..."
				self.session.open(MessageBox, tmpMessage, MessageBox.TYPE_INFO)
			except Exception as err:
					print "[GreekStreamTV::PluginMenu] Exception: ", str(err)
					tmpMessage = "GreekStreamTV bouquet update failed..."

					self.session.open(MessageBox, tmpMessage, MessageBox.TYPE_INFO)

    def create(self, answer):
        if answer:
            self.session.open(Console,_("Create Bouquets List"),["%s create" % url_sc])


    def updatebq(self):
        from xml.etree.cElementTree import ElementTree
        tree = ElementTree()
        tree.parse(GSXML)
        tvlist = []
        for iptv in tree.findall("iptv"):
            name = iptv.findtext("name").title()
            (protocol, serviceType, bufferSize, epgId) = iptv.findtext("type").split(":")
            uri = iptv.findtext("uri")
            if protocol in "livestreamer":
                uri = "http://127.1:88/" + uri
            uri = uri.replace(":", "%3a")
            service = "#SERVICE {s}:0:1:{e}:{e}:0:0:0:0:0:{u}:{n}\n".format(s=serviceType,e=epgId,u=uri,n=name)
            tvlist.append((name,service))

        tvlist=sorted(tvlist, key=lambda channel: channel[0]) #sort by name
        with open(GSBQ, "w") as f:
            f.write("#NAME GreekStreamTV\n")
            for (name, service) in tvlist:
                f.write(service)

	com = "cat /usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml ; rm /usr/lib/enigma2/python/Plugins/Satdreamgr/UpdateBouquet/stream.xml"
	out = os.popen(com)

        return list

