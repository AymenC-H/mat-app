from PyQt5.QtWidgets import QApplication,QWidget
from mat_app import base

app=QApplication([])
widget=base()
widget.setWindowTitle("Applications sur les matrices")
widget.show()

app.exec()
