from dataclasses import dataclass

@dataclass
class UserDTO:
    user_data: dict

    def add_data(self, tag_name, data):
        self.user_data[tag_name] = data