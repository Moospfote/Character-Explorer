from models.database import Database

class CharacterController:
    def __init__(self):
        self.db = Database()
    
    # Character operations
    def add_character(self, chara_name, chara_age, is_oc, chara_creator, 
                     chara_info, franchise_id, character_image):
        """Adds a new character"""
        if not chara_name.strip():
            raise ValueError('Character name cannot be empty!')
        return self.db.add_character(chara_name, chara_age, is_oc, chara_creator,
                                     chara_info, franchise_id, character_image)
    
    def get_all_characters(self, sort_by='chara_name'):
        """Returns all characters"""
        return self.db.get_all_characters(sort_by)
    
    def get_character_by_id(self, character_id):
        """Returns a character by ID"""
        return self.db.get_character_by_id(character_id)
    
    def search_characters(self, search_term):
        """Searches characters"""
        return self.db.search_characters(search_term)
    
    def update_character(self, character_id, chara_name, chara_age, is_oc,
                        chara_creator, chara_info, franchise_id, character_image):
        """Updates a character"""
        if not chara_name.strip():
            raise ValueError('Character name cannot be empty!')
        self.db.update_character(character_id, chara_name, chara_age, is_oc,
                                chara_creator, chara_info, franchise_id, character_image)
    
    def delete_character(self, character_id):
        """Deletes a character"""
        self.db.delete_character(character_id)
    
    # Franchise operations
    def add_franchise(self, franchise_name, franchise_info=''):
        """Adds a new franchise"""
        if not franchise_name.strip():
            raise ValueError('Franchise name cannot be empty!')
        return self.db.add_franchise(franchise_name, franchise_info)
    
    def get_all_franchises(self):
        """Returns all franchises"""
        return self.db.get_all_franchises()
    
    def get_franchise_by_id(self, franchise_id):
        """Returns a franchise by ID"""
        return self.db.get_franchise_by_id(franchise_id)
    
    def update_franchise(self, franchise_id, franchise_name, franchise_info):
        """Updates a franchise"""
        if not franchise_name.strip():
            raise ValueError('Franchise name cannot be empty!')
        self.db.update_franchise(franchise_id, franchise_name, franchise_info)
    
    def delete_franchise(self, franchise_id):
        """Deletes a franchise"""
        self.db.delete_franchise(franchise_id)
