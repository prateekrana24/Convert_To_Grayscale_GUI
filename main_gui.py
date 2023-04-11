import os
import pyautogui
import cv2 as cv

from PyQt6.QtGui import QPixmap, QFont, QImage
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QListWidget, \
    QPushButton, QFileDialog, QLabel, QSizePolicy, QScrollArea


class MainWindow(QMainWindow, QScrollArea):
    def __init__(self):
        super().__init__()
        self.screen_width, self.screen_height = pyautogui.size()

        self.setWindowTitle("Image Converter - Original To Grayscale GUI")

        main_frame_widget = QWidget()
        main_frame = QGridLayout()
        self.list_box = QListWidget()
        list_box_widget = QWidget(main_frame_widget)

        self.top_image = QLabel()
        top_image_text = QLabel(self.top_image)

        self.bottom_image = QLabel()
        bottom_image_text = QLabel(self.bottom_image)

        top_image_text.setText("Original Image")
        top_image_text.setFont(QFont("Arial", 26))
        top_image_text.setStyleSheet("border: none;")

        self.top_image.setStyleSheet("border: 2px solid black;")
        self.top_image.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        bottom_image_text.setText("Grayscale Image")
        bottom_image_text.setFont(QFont("Arial", 26))
        bottom_image_text.setStyleSheet("border: none;")

        self.bottom_image.setStyleSheet("border: 2px solid black;")
        self.bottom_image.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        main_frame.setColumnStretch(0, 1)
        main_frame.setColumnStretch(1, 1)
        main_frame.setRowStretch(0, 1)
        main_frame.setRowStretch(1, 1)

        # Create a button to add items to the QListWidget
        list_box_add_items_button = QPushButton("Add Items")
        list_box_add_items_button.clicked.connect(self.add_folder)

        list_box_clear_all_button = QPushButton("Clear All Items")
        list_box_clear_all_button.clicked.connect(self.clear_list_box)

        list_box_clear_item_button = QPushButton("Clear An Item")
        list_box_clear_item_button.clicked.connect(self.delete_item_in_list_box)

        self.list_box.currentRowChanged.connect(self.on_item_clicked)

        # Create a vertical layout to add the QListWidget and button
        list_box_layout = QVBoxLayout()
        list_box_layout.addWidget(list_box_add_items_button)
        list_box_layout.addWidget(list_box_clear_all_button)
        list_box_layout.addWidget(list_box_clear_item_button)
        list_box_layout.addWidget(self.list_box)

        list_box_widget.setLayout(list_box_layout)

        main_frame.addWidget(self.top_image, 0, 0)
        main_frame.addWidget(self.bottom_image, 1, 0)
        main_frame.addWidget(list_box_widget, 1, 1)

        main_frame_widget.setLayout(main_frame)

        self.setCentralWidget(main_frame_widget)

    def on_item_clicked(self):
        if self.list_box.currentItem() is None:
            return

        image_path = self.list_box.currentItem().data(Qt.ItemDataRole.DisplayRole)

        pixmap = QPixmap(image_path)

        scaled_pixmap_top = pixmap.scaled(self.top_image.contentsRect().width(), self.top_image.contentsRect().height(),
                                          Qt.AspectRatioMode.KeepAspectRatio)

        image_path_ndarray = cv.imread(image_path)

        gray_img = cv.cvtColor(image_path_ndarray, cv.COLOR_BGR2GRAY)
        q_image = QImage(gray_img.data, gray_img.shape[1], gray_img.shape[0], QImage.Format.Format_Grayscale8)

        pixmap2 = QPixmap.fromImage(q_image)

        scaled_pixmap2_bottom = pixmap2.scaled(self.bottom_image.contentsRect().width(),
                                               self.bottom_image.contentsRect().height(),
                                               Qt.AspectRatioMode.KeepAspectRatio)

        self.top_image.setPixmap(scaled_pixmap_top)
        self.bottom_image.setPixmap(scaled_pixmap2_bottom)

    def clear_list_box(self):
        self.list_box.clear()
        self.top_image.clear()
        self.bottom_image.clear()

    def delete_item_in_list_box(self):
        current_item = self.list_box.currentItem()
        if current_item is not None:
            self.list_box.takeItem(self.list_box.row(current_item))
            if self.list_box.count() == 0:
                self.top_image.clear()
                self.bottom_image.clear()

    def add_folder(self):
        # Prompt the user to select a folder and add it to the list box
        folder_path = QFileDialog.getExistingDirectory(self,
                                                       "Select Folder To Add To The ListBox")  # folder_path type is str

        if folder_path:
            bmp_files = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.bmp'):
                        file_path = os.path.join(root, file)
                        if os.path.basename(file_path) not in [os.path.basename(self.list_box.item(i).text()) for i in
                                                               range(self.list_box.count())]:
                            bmp_files.append(os.path.normpath(os.path.join(root, file)))

            # Add the .bmp files to the list box
            for bmp_file in bmp_files:
                self.list_box.addItem(bmp_file)


app = QApplication([])
window = MainWindow()
window.showMaximized()
window.show()
app.exec()
