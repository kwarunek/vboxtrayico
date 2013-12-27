#!/usr/bin/env python
""" VirtualBox tray (Windows)/menubar (Mac) console
It's one of the features I missed from Microsoft's Virtual PC (not anymore)
(c) Daniel Serodio 2009
"""

#########################################################################
#VBOX_HOME = 'C:/Program Files/Sun/Virtualbox'
VBOXMANAGE_BIN = 'vboxmanage'
# VBOX_HOME = '/Applications/VirtualBox.app/Contents/MacOS'
VBOX_PNG = "./icons/vbox.jpg"
#EOL = '\r\n'
EOL = '\n'
#########################################################################


import re
import subprocess
import sys
from subprocess import Popen
try:
    from PySide.QtCore import SIGNAL, QObject
    from PySide.QtGui import QIcon, QWidget, QApplication, QMenu, QSystemTrayIcon
except ImportError:
    from PyQt4.QtCore import SIGNAL, QObject
    from PyQt4.QtGui import QIcon, QWidget, QApplication, QMenu, QSystemTrayIcon


regex = re.compile(r'^"(.+)" {(.+)}')  # "VM name" {UUID}


def icon_activated(reason):
    if reason == QSystemTrayIcon.DoubleClick:
        subprocess.call(VBOXMANAGE_BIN)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.vms = {}
        for v in list_vms():
            submenu = QMenu(v, menu)
            self.vms[v] = {}
            self.vms[v]['menu'] = submenu
            start = submenu.addAction("Start", lambda vm=v: self.start_vm(vm))
            self.vms[v]['start'] = start
            stop = submenu.addAction("Stop", lambda vm=v: self.stop_vm(vm))
            self.vms[v]['stop'] = stop
            menu.addMenu(submenu)
        self.connect(menu, SIGNAL("aboutToShow()"), self.refresh_menu)

        menu.addSeparator()
        menu.addAction("Exit", lambda: exit(0))
        self.setContextMenu(menu)
        self.setToolTip("VirtualBox Tray Console")
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        QObject.connect(self, SIGNAL(traySignal), icon_activated)

    def start_vm(self, vm):
        self.showMessage("VirtualBox", "Starting %s" % vm)
        vbox_manage(['startvm', '%s' % vm])

    def stop_vm(self, vm):
        self.showMessage("VirtualBox", "Stopping %s" % vm)
        vbox_manage(['stopvm', '%s' % vm])

    def refresh_menu(self):
        running_vms = []
        for v in list_vms('runningvms'):
            running_vms.append(v)
        for v in self.vms:
            if v not in running_vms:
                self.vms[v]['start'].setEnabled(True)
                self.vms[v]['stop'].setDisabled(True)
            else:
                self.vms[v]['start'].setDisabled(True)
                self.vms[v]['stop'].setEnabled(True)


def main():
    app = QApplication(sys.argv)

    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon(VBOX_PNG), w)

    trayIcon.show()
    sys.exit(app.exec_())


def vbox_manage(argv):
    argv.insert(0, VBOXMANAGE_BIN)
    proc = Popen(argv, stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out.split(EOL)


def list_vms(what='vms'):
    vms = []
    out = vbox_manage(['list', what])
    for l in out:
        m = regex.match(l)
        if m:
            vms.append(m.group(1))
    return vms

if __name__ == "__main__":
    main()
