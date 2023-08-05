from PyQt5.QtWidgets import (QApplication, QSlider, QScrollArea, QGridLayout, 
                             QHBoxLayout, QWidget, QVBoxLayout, QPushButton, 
                             QFileDialog, QLabel, QLineEdit, QSplitter, QCheckBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSignal, pyqtSlot, QObject
from PIL import Image
import glob
import os
import sys

# Define constants
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
THUMBNAIL_SIZE = 100

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class WorkerSignals(QObject):
    thumbnailLoaded = pyqtSignal(QPixmap, int)

class ThumbnailLoader(QRunnable):
    def __init__(self, image_path, thumbnail_size, index):
        super().__init__()
        self.signals = WorkerSignals()
        self.image_path = image_path
        self.thumbnail_size = thumbnail_size
        self.index = index

    @pyqtSlot()
    def run(self):
        image = QImage()
        if not image.load(self.image_path):
            print(f"Failed to load image: {self.image_path}")
            return
        image = image.scaledToWidth(self.thumbnail_size)
        pixmap = QPixmap.fromImage(image)
        self.signals.thumbnailLoaded.emit(pixmap, self.index)

class ImageTagger(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("QCheckBox{margin-left:50%; margin-right:50%;}")
        self.images = []
        self.items = []

        self.initUI()
        self.thread_pool = QThreadPool()

    def initUI(self):
        self.setWindowTitle('Image Tagger')

        self.layout = QVBoxLayout(self)
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
        self.thumbnail_slider.setFixedHeight(50)
        self.splitter.addWidget(self.thumbnail_slider)
        self.thumbnail_slider.sliderReleased.connect(self.on_slider_value_changed)

    def clear_gallery(self):
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.items = []


# Change the on_slider_value_changed function to this
    def on_slider_value_changed(self):
        # Get the current value of the slider
        value = self.thumbnail_slider.value()
        # Update the thumbnail size
        global THUMBNAIL_SIZE
        THUMBNAIL_SIZE = value
        # Clear the current images
        self.clear_gallery()
        # Reload the images with the new size
        self.update_gallery()


    def load_images(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        print(f"Selected directory: {dir_path}")

        paths = []
        for ext in IMAGE_EXTENSIONS:
            paths.extend(glob.glob(os.path.join(dir_path, f'*{ext}')))
            
        print(f"Found {len(paths)} image(s) in the directory.")

        self.images = paths
        self.update_gallery()

    def update_gallery(self):
        self.thread_pool.setMaxThreadCount(10)

        for i, path in enumerate(self.images):
            thumbnail_loader = ThumbnailLoader(path, THUMBNAIL_SIZE, i)
            thumbnail_loader.signals.thumbnailLoaded.connect(self.add_thumbnail)
            self.thread_pool.start(thumbnail_loader)

    @pyqtSlot(QPixmap, int)
    def add_thumbnail(self, pixmap, img_index):
        label = ClickableLabel()
        label.setPixmap(pixmap)

        checkbox = QCheckBox()
        label.clicked.connect(checkbox.toggle)

        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.addWidget(label)
        container_layout.addWidget(checkbox)
        self.items.append(container_widget)

        self.grid_layout.addWidget(container_widget, img_index // 5, img_index % 5)

    def tag_images(self):
        tag = self.tag_entry.text()
        for checkbox_widget, image in zip(self.items, self.images):
            checkbox = checkbox_widget.children()[-1]
            if checkbox.isChecked():
                txt_file = f"{os.path.splitext(image)[0]}.txt"
                with open(txt_file, "a") as f:
                    f.write(tag + "\n")
                checkbox.setChecked(False)
        self.tag_entry.clear()

app = QApplication(sys.argv)

window = ImageTagger()
window.show()

sys.exit(app.exec_())