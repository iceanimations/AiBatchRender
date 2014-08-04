import site.addsitedir as asd
asd(r"r:/pipe_repo/users/qurban/utilities")
asd(r"r:/Python_Scripts")
import src._window as window
reload(window)
import sys
app = False
try:
    import PySide
except:
    from PyQt4.QtGui import QApplication
    app = True

def run():
    if app:
        app = QApplication(sys.argv)
    window.Window().show()
    if app:
        sys.exit(app.exec_())