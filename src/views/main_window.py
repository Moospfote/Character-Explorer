from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QLineEdit, QLabel, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from views.add_character_dialog import AddCharacterDialog
from views.edit_character_dialog import EditCharacterDialog
from views.character_details_dialog import CharacterDetailsDialog

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.all_characters = []
        self.init_ui()
        self.load_characters()
    
    def init_ui(self):
        """Initializes the user interface"""
        self.setWindowTitle('Character Explorer')
        self.setGeometry(100, 100, 1000, 600)

        logo_path = 'assets/character_explorer_logo.png'
        self.setWindowIcon(QIcon(logo_path))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel('Search:')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by name, creator, or franchise...')
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Character Name', 'Creator', 'Franchise', 'Details'])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 100)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton('Add Character')
        add_btn.clicked.connect(self.add_character)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton('Edit Character')
        edit_btn.clicked.connect(self.edit_character)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton('Delete Character')
        delete_btn.clicked.connect(self.delete_character)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def load_characters(self):
        """Loads all characters into the table"""
        self.all_characters = self.controller.get_all_characters()
        self.display_characters(self.all_characters)
    
    def display_characters(self, characters):
        """Displays characters in the table"""
        self.table.setRowCount(len(characters))
        
        for row, character in enumerate(characters):
            # character format: (chara_id, chara_name, chara_creator, franchise_name, 
            #                    chara_age, is_oc, chara_info, franchise_id, character_image)
            
            # Character Name
            name_item = QTableWidgetItem(character[1])
            name_item.setData(Qt.ItemDataRole.UserRole, character[0])  # Store ID
            self.table.setItem(row, 0, name_item)
            
            # Creator
            creator = character[2] if character[2] else ''
            self.table.setItem(row, 1, QTableWidgetItem(creator))
            
            # Franchise
            franchise = character[3] if character[3] else ''
            self.table.setItem(row, 2, QTableWidgetItem(franchise))
            
            # Details button
            details_btn = QPushButton('View Details')
            details_btn.clicked.connect(lambda checked, c_id=character[0]: self.show_details(c_id))
            self.table.setCellWidget(row, 3, details_btn)
    
    def filter_table(self):
        """Filters the table based on search input"""
        search_term = self.search_input.text().lower()
        
        if not search_term:
            self.display_characters(self.all_characters)
            return
        
        filtered_characters = [
            char for char in self.all_characters
            if search_term in str(char[1]).lower() or  # chara_name
               search_term in str(char[2] or '').lower() or  # chara_creator
               search_term in str(char[3] or '').lower()  # franchise_name
        ]
        
        self.display_characters(filtered_characters)
    
    def show_details(self, character_id):
        """Shows character details dialog"""
        character = self.controller.get_character_by_id(character_id)
        if character:
            dialog = CharacterDetailsDialog(character, self)
            dialog.exec()
    
    def add_character(self):
        """Opens dialog to add a character"""
        dialog = AddCharacterDialog(self.controller, self)
        if dialog.exec():
            self.load_characters()
            self.search_input.clear()
            QMessageBox.information(self, 'Success', 'Character added successfully!')
    
    def edit_character(self):
        """Opens dialog to edit a character"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Warning', 'Please select a character!')
            return
        
        character_id = self.table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        character = self.controller.get_character_by_id(character_id)
        
        dialog = EditCharacterDialog(character, self.controller, self)
        if dialog.exec():
            self.load_characters()
            self.search_input.clear()
            QMessageBox.information(self, 'Success', 'Character updated successfully!')
    
    def delete_character(self):
        """Deletes the selected character"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Warning', 'Please select a character!')
            return
        
        character_name = self.table.item(selected_row, 0).text()
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            f'Do you really want to delete "{character_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            character_id = self.table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
            self.controller.delete_character(character_id)
            self.load_characters()
            self.search_input.clear()
            QMessageBox.information(self, 'Success', 'Character deleted successfully!')
