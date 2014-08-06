'''
Created on Aug 4, 2014

@author: Qurban Ali
'''
import site
site.addsitedir(r"R:\Pipe_Repo\Users\Qurban\utilities")
site.addsitedir(r"r:/Python_Scripts")
try:
    import shiboken as uic
    from PySide.QtGui import QFileDialog
    from PySide.QtGui import qApp
    import uiLoader
    uic.loadUiType = uiLoader.loadUiType
except:
    from PyQt4 import uic
    from PyQt4.QtGui import QFileDialog
    from PyQt4.QtGui import qApp
import os
import _render as ren
reload(ren)
import _sysinfo as si
reload(si)
import pymel.core as pc

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
        
        self.renderButton.clicked.connect(self.render)
        self.usernameBox.setText(os.environ.get("USERNAME"))
        self.passwordBox.setFocus()
        self.browseButton.clicked.connect(self.browse)
        
    def closeEvent(self, event):
        self.deleteLater()
    
    def hideEvent(self, event):
        self.close()
        
    def browse(self):
        filename = QFileDialog.getExistingDirectory(self, "Project Folder", '')
        if filename:
            self.projectBox.setText(filename)
        
    def render(self):

        username = str(self.usernameBox.text())
        password = str(self.passwordBox.text())
        project = str(self.projectBox.text())
        if not osp.exists(project):
            pc.warning("project path does not exist")
            return
        if not username:
            pc.warning("username not specified")
            return
        if not password:
            pc.warning("password not specified")
            return
        if not ren.find_live_nodes(username, password):
            pc.warning("No remote computer ready to render")
            return
        nodes = ren.find_live_nodes(username, password)
        if not nodes:
            pc.warning("No machine ready to render")
        else:
            self.statusBar.showMessage((str(len(nodes))+" nodes ready"), 2000)
            qApp.processEvents()
            
        ren.ai_render(username, password, project, nodes)