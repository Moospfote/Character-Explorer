import sqlite3
import os
import sys

def get_database_path():
    """Returns the correct path for the database (also for .exe)"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    data_dir = os.path.join(base_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'characters.db')

class Database:
    def __init__(self):
        self.db_path = get_database_path()
        self.create_tables()
    
    def get_connection(self):
        """Creates a new database connection with foreign key support"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def create_tables(self):
        """Creates the franchise and character tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Franchise table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS franchise (
                franchise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                franchise_name TEXT NOT NULL UNIQUE,
                franchise_info TEXT
            )
        ''')
        
        # Character table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character (
                chara_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chara_name TEXT NOT NULL,
                chara_age INTEGER,
                is_oc INTEGER NOT NULL DEFAULT 0,
                chara_creator TEXT,
                chara_info TEXT,
                franchise_id INTEGER,
                character_image BLOB,
                FOREIGN KEY (franchise_id) REFERENCES franchise(franchise_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Franchise operations
    def add_franchise(self, franchise_name, franchise_info=''):
        """Adds a new franchise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO franchise (franchise_name, franchise_info)
                VALUES (?, ?)
            ''', (franchise_name, franchise_info))
            conn.commit()
            franchise_id = cursor.lastrowid
            return franchise_id
        except sqlite3.IntegrityError:
            # Franchise already exists, return its ID
            cursor.execute('SELECT franchise_id FROM franchise WHERE franchise_name = ?', 
                         (franchise_name,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    def get_all_franchises(self):
        """Returns all franchises"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM franchise ORDER BY franchise_name')
        franchises = cursor.fetchall()
        conn.close()
        return franchises
    
    def get_franchise_by_id(self, franchise_id):
        """Returns a single franchise by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM franchise WHERE franchise_id = ?', (franchise_id,))
        franchise = cursor.fetchone()
        conn.close()
        return franchise
    
    def update_franchise(self, franchise_id, franchise_name, franchise_info):
        """Updates a franchise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE franchise 
            SET franchise_name = ?, franchise_info = ?
            WHERE franchise_id = ?
        ''', (franchise_name, franchise_info, franchise_id))
        conn.commit()
        conn.close()
    
    def delete_franchise(self, franchise_id):
        """Deletes a franchise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM franchise WHERE franchise_id = ?', (franchise_id,))
        conn.commit()
        conn.close()
    
    # Character operations
    def add_character(self, chara_name, chara_age, is_oc, chara_creator, 
                     chara_info, franchise_id, character_image=None):
        """Adds a new character"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO character 
            (chara_name, chara_age, is_oc, chara_creator, chara_info, franchise_id, character_image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chara_name, chara_age, is_oc, chara_creator, chara_info, franchise_id, character_image))
        conn.commit()
        character_id = cursor.lastrowid
        conn.close()
        return character_id
    
    def get_all_characters(self, sort_by='chara_name'):
        """Returns all characters with franchise info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        valid_columns = ['chara_name', 'chara_creator', 'franchise_name', 'chara_age']
        if sort_by not in valid_columns:
            sort_by = 'chara_name'
        
        cursor.execute(f'''
            SELECT c.chara_id, c.chara_name, c.chara_creator, f.franchise_name, 
                   c.chara_age, c.is_oc, c.chara_info, c.franchise_id, c.character_image
            FROM character c
            LEFT JOIN franchise f ON c.franchise_id = f.franchise_id
            ORDER BY {sort_by}
        ''')
        characters = cursor.fetchall()
        conn.close()
        return characters
    
    def get_character_by_id(self, character_id):
        """Returns a single character with franchise info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.chara_id, c.chara_name, c.chara_age, c.is_oc, c.chara_creator,
                   c.chara_info, c.franchise_id, f.franchise_name, f.franchise_info, 
                   c.character_image
            FROM character c
            LEFT JOIN franchise f ON c.franchise_id = f.franchise_id
            WHERE c.chara_id = ?
        ''', (character_id,))
        character = cursor.fetchone()
        conn.close()
        return character
    
    def search_characters(self, search_term):
        """Searches characters by name, creator, or franchise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.chara_id, c.chara_name, c.chara_creator, f.franchise_name,
                   c.chara_age, c.is_oc, c.chara_info, c.franchise_id, c.character_image
            FROM character c
            LEFT JOIN franchise f ON c.franchise_id = f.franchise_id
            WHERE c.chara_name LIKE ? OR c.chara_creator LIKE ? OR f.franchise_name LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        characters = cursor.fetchall()
        conn.close()
        return characters
    
    def update_character(self, character_id, chara_name, chara_age, is_oc, 
                        chara_creator, chara_info, franchise_id, character_image=None):
        """Updates a character"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if character_image is not None:
            cursor.execute('''
                UPDATE character 
                SET chara_name = ?, chara_age = ?, is_oc = ?, chara_creator = ?,
                    chara_info = ?, franchise_id = ?, character_image = ?
                WHERE chara_id = ?
            ''', (chara_name, chara_age, is_oc, chara_creator, chara_info, 
                 franchise_id, character_image, character_id))
        else:
            cursor.execute('''
                UPDATE character 
                SET chara_name = ?, chara_age = ?, is_oc = ?, chara_creator = ?,
                    chara_info = ?, franchise_id = ?
                WHERE chara_id = ?
            ''', (chara_name, chara_age, is_oc, chara_creator, chara_info, 
                 franchise_id, character_id))
        
        conn.commit()
        conn.close()
    
    def delete_character(self, character_id):
        """Deletes a character"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM character WHERE chara_id = ?', (character_id,))
        conn.commit()
        conn.close()
