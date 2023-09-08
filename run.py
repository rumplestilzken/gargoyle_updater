#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import threading

from updater import ota, flash

x = None


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)

        self.setWindowIcon(QIcon('resources/icon.jpg'))
        # set the title
        self.setWindowTitle("gargoyle GSI Updater")

        # show all the widgets
        self.show()


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        self.url_text = QLabel("Update URL:")
        self.layout.addWidget(self.url_text, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self.release = QComboBox(self)
        self.release.setFixedWidth(300)
        self.release.setFixedHeight(20)

        for entry in ota.getOTADictionary().keys():
            self.release.addItem(entry)

        self.layout.addWidget(self.release, 0, 1, Qt.AlignmentFlag.AlignRight)

        self.flash_type = QComboBox(self)
        self.flash_type.addItem("update")
        self.flash_type.addItem("flash")
        self.flash_type.addItem("full_flash")
        self.layout.addWidget(self.flash_type, 0, 2, Qt.AlignmentFlag.AlignLeft)

        self.variant_text_edit = QLabel("Variant")
        self.layout.addWidget(self.variant_text_edit, 1, 0, Qt.AlignmentFlag.AlignLeft)

        self.gsi_variant = QComboBox(self)
        self.gsi_variant.setFixedWidth(300)
        self.gsi_variant.setFixedHeight(20)
        self.gsi_variant.addItem("Titan")
        self.gsi_variant.addItem("Titan Pocket")
        self.gsi_variant.addItem("Titan Slim")
        self.gsi_variant.addItem("Jelly 2E")
        self.gsi_variant.activated.connect(self.update_ui)
        self.layout.addWidget(self.gsi_variant, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.region = QComboBox()
        self.region.addItem("TEE")
        self.region.addItem("EEA")
        self.region.setFixedWidth(80)
        self.layout.addWidget(self.region, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.qualifier = QComboBox(self)
        self.qualifier.addItem("bvn")
        self.qualifier.addItem("bgN")
        self.qualifier.addItem("bgN-vndkLite")
        self.qualifier.addItem("bvN-vndkLite")
        self.layout.addWidget(self.qualifier, 1, 3, Qt.AlignmentFlag.AlignLeft)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(390)
        self.layout.addWidget(self.progress_bar, 5, 1, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.button1 = QPushButton("Flash")
        self.layout.addWidget(self.button1, 5, 0, Qt.AlignmentFlag.AlignRight)

        self.update_message = QLabel("")
        self.update_message.setVisible(False)
        self.layout.addWidget(self.update_message, 6, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)

    def openFileDialog(self):
        file_dialog = QFileDialog()
        file_name = file_dialog.getOpenFileName(self, "Select Stock Rom Archive", "/home/")
        window.form_widget.stock_rom_edit.setText(file_name[0])

    def update_ui(self):
        window.form_widget.qualifier.clear()
        window.form_widget.region.clear()
        window.form_widget.qualifier.addItem("bvn")
        window.form_widget.region.addItem("TEE")
        window.form_widget.region.addItem("EEA")
        if "Titan" == window.form_widget.gsi_variant.currentText():
            self.qualifier.addItem("bgN-vndkLite")
            self.qualifier.addItem("bvN-vndkLite")
            window.form_widget.region.addItem("UFS")
        window.form_widget.qualifier.addItem("bgN")


app = QApplication(sys.argv)
window = Window()


def flash_click():
    url = window.form_widget.release.currentText()
    actual_url = ota.getOTADictionary()[url]
    variant = window.form_widget.gsi_variant.currentText()
    qualifier = window.form_widget.qualifier.currentText()
    region = window.form_widget.region.currentText()
    flash.process_flash(actual_url, variant, region, qualifier, window.form_widget.progress_bar)


def flash_click_event():
    global x
    window.form_widget.setEnabled(False)
    window.form_widget.progress_bar.setValue(0)
    x = threading.Thread(target=flash_click)
    x.start()
    y = threading.Thread(target=process_finished)
    y.start()


def process_finished():
    global x
    while x.is_alive():
        ""  # Do Nothing
    window.form_widget.progress_bar.setValue(100)
    window.form_widget.setEnabled(True)


def main():
    window.form_widget.button1.clicked.connect(lambda: flash_click_event())
    window.form_widget.update_ui()

    sys.exit(app.exec())
    return


if __name__ == '__main__':
    main()
