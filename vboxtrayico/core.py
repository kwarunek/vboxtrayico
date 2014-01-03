#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import subprocess
import sys
from subprocess import Popen
from PySide.QtCore import SIGNAL, QObject, QByteArray
from PySide.QtGui import QIcon,  QCursor
from PySide.QtGui import QMenu, QSystemTrayIcon, QPixmap


def get_vbox_manage_bin():
    if sys.platform == "win32":
        try:
            import _winreg as winreg
        except:
            import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 'SOFTWARE\\Oracle\\VirtualBox')
            install_dir = winreg.QueryValueEx(key, 'InstallDir')
            return ("%s\VBoxManage.exe" % (install_dir[0]))
        except:
            raise Exception('Unable to determine VirualBox install dir')
    elif sys.platform == 'darwin':
        # temp hardcoded
        return '/Applications/VirtualBox.app/Contents/MacOS/VBoxManage'
    else:
        return "vboxmanage"


class SystemTrayIcon(QSystemTrayIcon):

    i = "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" \
        "S7AAAAAElFTkSuQmCC"

    def __init__(self, parent=None):
        icon = self.loadIcon()
        QSystemTrayIcon.__init__(self, icon, parent)

        menu = QMenu(parent)
        VBoxMenu.build(menu)
        menu.addSeparator()
        menu.addAction("Exit", lambda: sys.exit(0))
        self.connect(menu, SIGNAL("aboutToShow()"), VBoxMenu.check_state)

        self.setContextMenu(menu)
        self.setToolTip("VBoxTrayIco")

        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        QObject.connect(self, SIGNAL(traySignal), self.showMenu)

    def showMenu(self, reason):
        # show menu also on left click
        self.contextMenu().exec_(QCursor.pos())

    def loadIcon(self):
        bytearr = QByteArray.fromBase64(self.i)
        pixmap = QPixmap()
        pixmap.loadFromData(bytearr)
        return QIcon(pixmap)


class VBoxMenu(QMenu):

    def __init__(self, uuid, name, parent):
        super(VBoxMenu, self).__init__(name, parent)

        self.vm_name = name
        self.uuid = uuid

        self.actions = {}
        self.actions['start'] = self.addAction("Start", lambda: self.start())
        self.actions['start_headless'] = self.addAction(
            "Start headless",
            lambda: self.start_headless()
        )
        self.actions['reset'] = self.addAction("Reset", lambda: self.reset())
        self.actions['poweroff'] = self.addAction(
            "Power off",
            lambda: self.poweroff()
        )

    def start(self):
        self.manage(['startvm', '%s' % self.uuid])

    def start_headless(self):
        self.manage(['startvm', '--type', 'headless', '%s' % self.uuid])

    def reset(self):
        self.manage(['controlvm', '%s' % self.uuid, 'reset'])

    def poweroff(self):
        self.manage(['controlvm', '%s' % self.uuid, 'poweroff'])

    @classmethod
    def build(cls, menu):
        cls.vms = {}
        for k, v in cls.get_vm_list().items():
            submenu = cls(k, v, menu)
            cls.vms[k] = submenu
            menu.addMenu(submenu)

    @classmethod
    def get_vm_list(cls, objects="vms"):
        vms = {}
        out = cls.manage(['list', objects])
        regex = re.compile(r'^"(.+)" {(.+)}')
        for l in out:
            m = regex.match(l)
            if m:
                vms[m.group(2)] = m.group(1)
        return vms

    @classmethod
    def check_state(cls):
        running_vms = cls.get_vm_list('runningvms')
        for uuid, vm in cls.vms.items():
            if uuid not in running_vms.keys():
                vm.actions['start'].setEnabled(True)
                vm.actions['start_headless'].setEnabled(True)
                vm.actions['poweroff'].setDisabled(True)
                vm.actions['reset'].setDisabled(True)
            else:
                vm.actions['start'].setDisabled(True)
                vm.actions['start_headless'].setDisabled(True)
                vm.actions['poweroff'].setEnabled(True)
                vm.actions['reset'].setEnabled(True)

    @staticmethod
    def manage(argv):
        argv.insert(0, get_vbox_manage_bin())
        proc = Popen(argv, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        return out.decode().split("\n")
