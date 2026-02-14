class Character:
    """Data model for a character"""
    def __init__(self, chara_id=None, chara_name='', chara_age=None, is_oc=False, 
                 chara_creator='', chara_info='', franchise_id=None, 
                 franchise_name='', franchise_info='', character_image=None):
        self.chara_id = chara_id
        self.chara_name = chara_name
        self.chara_age = chara_age
        self.is_oc = is_oc
        self.chara_creator = chara_creator
        self.chara_info = chara_info
        self.franchise_id = franchise_id
        self.franchise_name = franchise_name
        self.franchise_info = franchise_info
        self.character_image = character_image
