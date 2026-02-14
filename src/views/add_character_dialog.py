from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QFormLayout,
                             QSpinBox, QCheckBox, QComboBox, QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class AddCharacterDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.image_data = None
        self.init_ui()
    
    def init_ui(self):
        """Initializes the dialog"""
        self.setWindowTitle('Add Character')
        self.setGeometry(200, 200, 550, 500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Form
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        form_layout.addRow('Character Name*:', self.name_input)
        
        self.age_input = QSpinBox()
        self.age_input.setMinimum(0)
        self.age_input.setMaximum(10000)
        self.age_input.setSpecialValueText('Unknown')
        form_layout.addRow('Age:', self.age_input)
        
        self.oc_checkbox = QCheckBox()
        form_layout.addRow('Original Character (OC)*:', self.oc_checkbox)
        
        self.creator_input = QLineEdit()
        form_layout.addRow('Creator:', self.creator_input)
        
        # Franchise selection with add new option
        franchise_layout = QHBoxLayout()
        self.franchise_combo = QComboBox()
        self.load_franchises()
        franchise_layout.addWidget(self.franchise_combo)
        
        add_franchise_btn = QPushButton('New Franchise')
        add_franchise_btn.clicked.connect(self.add_new_franchise)
        franchise_layout.addWidget(add_franchise_btn)
        
        form_layout.addRow('Franchise:', franchise_layout)
        
        self.info_input = QTextEdit()
        self.info_input.setMaximumHeight(100)
        form_layout.addRow('Information:', self.info_input)
        
        # Image selection
        image_layout = QHBoxLayout()
        self.image_label = QLabel('No image selected')
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedHeight(150)
        self.image_label.setStyleSheet('border: 1px solid gray;')
        
        select_image_btn = QPushButton('Select Image')
        select_image_btn.clicked.connect(self.select_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(select_image_btn)
        
        form_layout.addRow('Character Image:', image_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(self.save_character)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_franchises(self):
        """Loads all franchises into the combo box"""
        self.franchise_combo.clear()
        self.franchise_combo.addItem('None', None)
        
        franchises = self.controller.get_all_franchises()
        for franchise in franchises:
            self.franchise_combo.addItem(franchise[1], franchise[0])
    
    def add_new_franchise(self):
        """Opens a simple input dialog for new franchise"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, 'New Franchise', 'Franchise Name:')
        if ok and name.strip():
            info, ok2 = QInputDialog.getMultiLineText(self, 'New Franchise', 'Franchise Info (optional):')
            franchise_id = self.controller.add_franchise(name.strip(), info if ok2 else '')
            self.load_franchises()
            # Select the newly added franchise
            index = self.franchise_combo.findData(franchise_id)
            if index >= 0:
                self.franchise_combo.setCurrentIndex(index)
    
    def select_image(self):
        """Opens file dialog to select an image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Select Character Image', 
            '', 
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        
        if file_path:
            with open(file_path, 'rb') as file:
                self.image_data = file.read()
            
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(
                self.image_label.width() - 10, 
                self.image_label.height() - 10,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def save_character(self):
        """Validates and saves the character"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, 'Validation Error', 'Character name is required!')
            return
        
        age = self.age_input.value() if self.age_input.value() > 0 else None
        is_oc = 1 if self.oc_checkbox.isChecked() else 0
        creator = self.creator_input.text().strip() or None
        info = self.info_input.toPlainText().strip() or None
        franchise_id = self.franchise_combo.currentData()
        
        self.controller.add_character(
            name, age, is_oc, creator, info, franchise_id, self.image_data
        )
        
        self.accept()
