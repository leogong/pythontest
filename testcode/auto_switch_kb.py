#! /usr/bin/env python
# coding: utf-8

'''
auto switch keyboard between different applications
if you want to change the app list, modify the var 'ignore_list'
一定要用系统自带的 python, 用 brew 或其他方式安装的 python 不能识别 AppKit 等模块，花了很长时间在 pyobjc 的文档中看到这样一句话：
The system version of Python (``/usr/bin/python``) includes a copy of
PyObjC starting at MacOSX 10.5 ("Leopard"). Installing other versions
of PyObjC with "/usr/bin/python" on Leopard or later is not supported
and could break your system.
相见恨晚啊！
用了 brew install python 的直接 brew uninstall python 即可，就是 python 不能使用最新版。
'''

from AppKit import NSWorkspace, NSWorkspaceDidActivateApplicationNotification, NSWorkspaceApplicationKey
from Foundation import NSObject
from PyObjCTools import AppHelper
import ctypes
import ctypes.util
import objc
import CoreFoundation

import AppKit
info = AppKit.NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"

# add your custom apps here, check the bundle id in /Application/xx.app/Contents/info.plist

ignore_list = [
    "com.googlecode.iterm2",
    "com.runningwithcrayons.Alfred-2",
    "com.runningwithcrayons.Alfred-3",
    "com.apple.Spotlight",
    "com.jetbrains.intellij.ce-EAP",
    "com.google.android.studio",
    "com.sublimetext.3",
    "com.github.atom"
]


carbon = ctypes.cdll.LoadLibrary(ctypes.util.find_library('Carbon'))

_objc = ctypes.PyDLL(objc._objc.__file__)

# PyObject *PyObjCObject_New(id objc_object, int flags, int retain)
_objc.PyObjCObject_New.restype = ctypes.py_object
_objc.PyObjCObject_New.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

def objc_object(id):
    return _objc.PyObjCObject_New(id, 0, 1)

# kTISPropertyLocalizedName
kTISPropertyUnicodeKeyLayoutData_p = ctypes.c_void_p.in_dll(carbon, 'kTISPropertyInputSourceIsEnabled')
kTISPropertyInputSourceLanguages_p = ctypes.c_void_p.in_dll(carbon, 'kTISPropertyInputSourceLanguages')
kTISPropertyInputSourceType_p = ctypes.c_void_p.in_dll(carbon, 'kTISPropertyInputSourceType')
kTISPropertyLocalizedName_p = ctypes.c_void_p.in_dll(carbon, 'kTISPropertyLocalizedName')
# kTISPropertyInputSourceLanguages_p = ctypes.c_void_p.in_dll(carbon, 'kTISPropertyInputSourceLanguages')

kTISPropertyInputSourceCategory = objc_object(ctypes.c_void_p.in_dll(carbon, 'kTISPropertyInputSourceCategory'))
kTISCategoryKeyboardInputSource = objc_object(ctypes.c_void_p.in_dll(carbon, 'kTISCategoryKeyboardInputSource'))


# TISCreateInputSourceList
carbon.TISCreateInputSourceList.restype = ctypes.c_void_p
carbon.TISCreateInputSourceList.argtypes = [ctypes.c_void_p, ctypes.c_bool]

carbon.TISSelectInputSource.restype = ctypes.c_void_p
carbon.TISSelectInputSource.argtypes = [ctypes.c_void_p]

carbon.TISGetInputSourceProperty.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p

# carbon.TISCopyCurrentKeyboardLayoutInputSource.argtypes = []
# carbon.TISCopyCurrentKeyboardLayoutInputSource.restype = ctypes.c_void_p

carbon.TISCopyInputSourceForLanguage.argtypes = [ctypes.c_void_p]
carbon.TISCopyInputSourceForLanguage.restype = ctypes.c_void_p


def get_avaliable_languages():
    single_langs = filter(lambda x: x.count() == 1, \
        map(lambda x: objc_object(carbon.TISGetInputSourceProperty(CoreFoundation.CFArrayGetValueAtIndex(objc_object(s), x).__c_void_p__(), kTISPropertyInputSourceLanguages_p)), \
            range(CoreFoundation.CFArrayGetCount(objc_object(carbon.TISCreateInputSourceList(None, 0))))))
    res = set()
    map(lambda y: res.add(y[0]), single_langs)
    return res

def select_kb(lang):
    cur = carbon.TISCopyInputSourceForLanguage(CoreFoundation.CFSTR(lang).__c_void_p__())
    carbon.TISSelectInputSource(cur)

class Observer(NSObject):
    def handle_(self, noti):
        # info = noti.userInfo().objectForKey_(NSWorkspaceApplicationKey)
        # bundleIdentifier = info.bundleIdentifier()
        # if bundleIdentifier in ignore_list:
            #print "found: %s active" % bundleIdentifier
            # select_kb(u'en')
        select_kb(u'en')


def main():
    nc = NSWorkspace.sharedWorkspace().notificationCenter()
    observer = Observer.new()
    nc.addObserver_selector_name_object_(
        observer,
        "handle:",
        NSWorkspaceDidActivateApplicationNotification,
        None
    )
    AppHelper.runConsoleEventLoop(installInterrupt=True)

main()