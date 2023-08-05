import sys
import os
import glob
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QLabel, QLineEdit, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

# Define constants
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
THUMBNAIL_SIZE = 100

class ImageTagger(QWidget):
    def __init__(self):
        super().__init__()

        self.images = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Tagger')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.load_button = QPushButton('Load Images')
        self.load_button.clicked.connect(self.load_images)
        self.layout.addWidget(self.load_button)

        self.tag_entry = QLineEdit()
        self.layout.addWidget(self.tag_entry)

        self.tag_button = QPushButton('Tag Images')
        self.tag_button.clicked.connect(self.tag_images)
        self.layout.addWidget(self.tag_button)

        self.image_list = QListWidget()
        self.layout.addWidget(self.image_list)

    def load_images(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        paths = []
        for ext in IMAGE_EXTENSIONS:
            paths.extend(glob.glob(os.path.join(dir_path, f'*{ext}')))

        for path in paths:
            item = QListWidgetItem(self.image_list)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(THUMBNAIL_SIZE, THUMBNAIL_SIZE, Qt.KeepAspectRatio)
            icon = QLabel()
            icon.setPixmap(pixmap)
            check_box = QCheckBox()
            self.image_list.setItemWidget(item, check_box)
            self.images.append(path)

    def tag_images(self):
        tag = self.tag_entry.text()

        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            check_box = self.image_list.itemWidget(item)
            if check_box.isChecked():
                image = self.images[i]
                txt_file = f"{os.path.splitext(image)[0]}.txt"
                with open(txt_file, "a") as f:
                    f.write(tag + "\n")
                check_box.setChecked(False)

        self.tag_entry.clear()


app = QApplication(sys.argv)

window = ImageTagger()
window.show()

sys.exit(app.exec_())
