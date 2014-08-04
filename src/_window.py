'''
Created on Aug 4, 2014

@author: Qurban Ali
'''
try:
    import shiboken as uic
except:
    from PyQt4 import uic
try:
    import qtify_maya_window as qtfy
    mayaWin = qtfy.getMayaWindow()
except: mayaWin = None
import os.path as osp

rootPath = osp.dirname(osp.dirname(__file__))

Form, Base = uic.loadUiType("%s/ui/main.ui"%rootPath)
class Window(Form, Base):
    def __init__(self, parent=mayaWin):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.show()