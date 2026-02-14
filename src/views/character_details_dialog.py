from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QScrollArea, QWidget)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class CharacterDetailsDialog(QDialog):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.init_ui()
    
    def init_ui(self):
        """Initializes the detail view"""
        self.setWindowTitle('Character Details')
        self.setGeometry(150, 150, 600, 700)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # character: (chara_id, chara_name, chara_age, is_oc, chara_creator,
        #            chara_info, franchise_id, franchise_name, franchise_info, character_image)
        
        # Character Image
        if self.character[9]:
            image_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(self.character[9])
            scaled_pixmap = pixmap.scaled(
                400, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scroll_layout.addWidget(image_label)
        
        # Character Name
        name_label = QLabel(f"<h2>{self.character[1]}</h2>")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(name_label)
        
        # OC Status
        oc_status = "Original Character (OC)" if self.character[3] else "Canon Character"
        oc_label = QLabel(f"<b>Status:</b> {oc_status}")
        scroll_layout.addWidget(oc_label)
        
        # Creator
        if self.character[4]:
            creator_label = QLabel(f"<b>Creator:</b> {self.character[4]}")
            scroll_layout.addWidget(creator_label)
        
        # Age
        if self.character[2]:
            age_label = QLabel(f"<b>Age:</b> {self.character[2]}")
            scroll_layout.addWidget(age_label)
        
        # Franchise
        if self.character[7]:
            franchise_label = QLabel(f"<b>Franchise:</b> {self.character[7]}")
            scroll_layout.addWidget(franchise_label)
            
            # Franchise Info
            if self.character[8]:
                franchise_info_label = QLabel("<b>Franchise Information:</b>")
                scroll_layout.addWidget(franchise_info_label)
                
                franchise_info_text = QTextEdit()
                franchise_info_text.setPlainText(self.character[8])
                franchise_info_text.setReadOnly(True)
                franchise_info_text.setMaximumHeight(100)
                scroll_layout.addWidget(franchise_info_text)
        
        # Character Info
        if self.character[5]:
            info_label = QLabel("<b>Character Information:</b>")
            scroll_layout.addWidget(info_label)
            
            info_text = QTextEdit()
            info_text.setPlainText(self.character[5])
            info_text.setReadOnly(True)
            info_text.setMaximumHeight(150)
            scroll_layout.addWidget(info_text)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
