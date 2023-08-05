import sys
import os
import glob
from PyQt5.QtWidgets import (QApplication, QSlider, QScrollArea, QGridLayout, QHBoxLayout, QWidget, 
                            QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QSplitter, QCheckBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PIL import Image

# Define constants
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
THUMBNAIL_SIZE = 100

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

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

        self.tag_label = QLabel('Tag:')
        self.layout.addWidget(self.tag_label)

        self.tag_entry = QLineEdit()
        self.tag_entry.setPlaceholderText('Tags go here')
        self.layout.addWidget(self.tag_entry)

        self.tag_button = QPushButton('Tag Images')
        self.tag_button.clicked.connect(self.tag_images)
        self.layout.addWidget(self.tag_button)

        # New QSplitter
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)

        # QScrollArea inside QSplitter
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.splitter.addWidget(self.scroll_area)

        # QWidget inside QScrollArea
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # QGridLayout inside QWidget
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.grid_layout)

        # QLabel and QSlider inside QSplitter
        self.thumbnail_label = QLabel('Thumbnail Size:')
        self.splitter.addWidget(self.thumbnail_label)
        
        self.thumbnail_slider = QSlider(Qt.Horizontal)
        self.thumbnail_slider.setMinimum(50)
        self.thumbnail_slider.setMaximum(500)
        self.thumbnail_slider.setValue(THUMBNAIL_SIZE)
        self.thumbnail_slider.valueChanged.connect(self.update_thumbnails)
        self.thumbnail_slider.setFixedHeight(50)
        self.splitter.addWidget(self.thumbnail_slider)


    def load_images(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        print(f"Selected directory: {dir_path}")
        
        paths = []
        for ext in IMAGE_EXTENSIONS:
            paths.extend(glob.glob(os.path.join(dir_path, f'*{ext}')))

        print(f"Found {len(paths)} image(s) in the directory.")

        self.images = paths
        self.update_thumbnails()

    def update_thumbnails(self):
        THUMBNAIL_SIZE = self.thumbnail_slider.value()

        for i in range(self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().deleteLater()

        column_count = self.scroll_area.width() // THUMBNAIL_SIZE

        for i, path in enumerate(self.images):
            print(f"Loading image: {path}")
            pixmap = QPixmap(path)

            if pixmap.isNull():
                print(f"Failed to create QPixmap from image: {path}")
                continue

            pixmap = pixmap.scaledToWidth(THUMBNAIL_SIZE)

            if pixmap.isNull():
                print(f"Failed to scale QPixmap from image: {path}")
                continue

            # Create a widget to hold both the QLabel and QCheckBox
            widget = QWidget()
            layout = QHBoxLayout(widget)

            icon = ClickableLabel()
            icon.setPixmap(pixmap)
            layout.addWidget(icon)

            check_box = QCheckBox()
            layout.addWidget(check_box)

            icon.clicked.connect(check_box.toggle)

            row = i // column_count
            column = i % column_count
            self.grid_layout.addWidget(widget, row, column)
            
    def resizeEvent(self, event):
        self.update_thumbnails()

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
