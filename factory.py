import json
from pet import Cat, Dog, Pet

def load_pet():
    filename = "pet_save.json"
    with open(filename, "r") as f:
        data = json.load(f)

    if data["type"] == "cat":
        pet = Cat(data["name"])
    elif data["type"] == "dog":
        pet = Dog(data["name"])
    else:
        raise ValueError("Unknown pet type")
    
    pet._hunger = data["hunger"]
    pet._cleanliness = data["cleanliness"]
    pet._happiness = data["happiness"]
    pet._energy = data["energy"]
    pet._created_at = data["created_at"]
    pet._last_decay_applied = data["last_decay_applied"]
    pet._last_interaction_time = data["last_interaction_time"]
    pet._zero_since = data["zero_since"]
    pet._has_run_away = data["has_run_away"]

    return pet

class PetFactory:
    @staticmethod
    def create_pet(pet_type: str, name: str) -> Pet:
        pet_type = pet_type.lower()

        if pet_type == "cat":
            return Cat(name)
        elif pet_type == "dog":
            return Dog(name)
        else:
            raise ValueError("Unknown pet type. Choose 'cat' or 'dog'.")
        