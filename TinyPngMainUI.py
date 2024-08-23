import os
import sys

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

from TinyPngCompressor import TinyPngCompressor


class FileEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(FileEdit, self).__init__()
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            print(urls[0].path())
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()


class TinyPngDialog(QtWidgets.QWidget):
    def __init__(self, title):
        super(TinyPngDialog, self).__init__()
        self.setWindowTitle(title)
        self.setMinimumWidth(600)
        self.setMinimumHeight(200)
        self.create_widgets()
        self.create_layout()
        self.set_api_key()

    def create_widgets(self):
        self.api_key_line_edit = FileEdit()
        self.api_key_line_edit.setPlaceholderText("API_KEY")
        self.src_line_edit = FileEdit()
        self.src_line_edit.setPlaceholderText("Source images folder path")
        self.dst_line_edit = FileEdit()
        self.dst_line_edit.setPlaceholderText("Destination images folder path")
        self.src_folder_btn = QtWidgets.QPushButton("Choose Source Folder")
        self.dst_folder_btn = QtWidgets.QPushButton("Choose Destination Folder")
        self.tiny_pass_btn = QtWidgets.QPushButton("Tiny Pass")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        hbox_1 = QtWidgets.QHBoxLayout()
        hbox_1.addWidget(self.api_key_line_edit)

        hbox_2 = QtWidgets.QHBoxLayout()
        hbox_2.addWidget(self.src_line_edit)
        hbox_2.addWidget(self.src_folder_btn)

        hbox_3 = QtWidgets.QHBoxLayout()
        hbox_3.addWidget(self.dst_line_edit)
        hbox_3.addWidget(self.dst_folder_btn)

        hbox_4 = QtWidgets.QHBoxLayout()
        hbox_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        hbox_4.addWidget(self.tiny_pass_btn)

        main_layout.addLayout(hbox_1)
        main_layout.addLayout(hbox_2)
        main_layout.addLayout(hbox_3)
        main_layout.addLayout(hbox_4)

        # connections
        self.api_key_line_edit.editingFinished.connect(self.set_api_key)
        self.src_folder_btn.clicked.connect(self.get_src_directory)
        self.dst_folder_btn.clicked.connect(self.get_dst_directory)
        self.tiny_pass_btn.clicked.connect(
            lambda: self.TPC.compress(self.src_line_edit.text(), self.dst_line_edit.text()))

    def get_src_directory(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        folder_name = file_dialog.getExistingDirectory()
        self.src_line_edit.setText(folder_name)
        print(folder_name)

    def get_dst_directory(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        folder_name = file_dialog.getExistingDirectory()
        self.dst_line_edit.setText(folder_name)
        print(folder_name)

    def set_api_key(self):
        self.TPC = TinyPngCompressor(self.api_key_line_edit.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = TinyPngDialog('Tiny PNG Pass')
    dialog.show()
    sys.exit(app.exec())
