from abc import ABC, abstractmethod
import time
import json

class Pet(ABC):
    def __init__(self, name: str):
        self._name = name
        self._hunger = 100
        self._happiness = 100
        self._cleanliness = 100
        self._energy = 100

        self._created_at = time.time()
        self._last_decay_applied = 0
        self._last_interaction_time = time.time()
        self._has_run_away = False
        self._zero_since = None

    def _apply_stat_decay(self):
        now = time.time()
        elapsed_seconds = (now - self._created_at)
        decay_interval_seconds = 300

        expected_intervals = int(elapsed_seconds // decay_interval_seconds)

        if expected_intervals > self._last_decay_applied:
            missed = expected_intervals - self._last_decay_applied
            decay_amount = missed * 5

            self._hunger = max(0, self._hunger - decay_amount)
            self._cleanliness = max(0, self._cleanliness - decay_amount)
            self._happiness = max(0, self._happiness - decay_amount)
            self._energy = max(0, self._energy - decay_amount)

            self._last_decay_applied = expected_intervals

        if all(stat <= 0 for stat in [self._hunger, self._happiness, self._cleanliness, self._energy]):
            if self._zero_since is None:
                self._zero_since = time.time()
        else:
            self._zero_since = None

    def _update_last_interaction(self):
        self._last_interaction_time = time.time()
    
    def save(self):
        filename = "pet_save.json"
        pet_data = {
            "type": self.__class__.__name__.lower(),
            "name": self._name,
            "hunger": self._hunger,
            "cleanliness": self._cleanliness,
            "happiness": self._happiness,
            "energy": self._energy,
            "created_at": self._created_at,
            "last_decay_applied": self._last_decay_applied,
            "last_interaction_time": self._last_interaction_time,
            "zero_since": self._zero_since,
            "has_run_away": self._has_run_away
        }

        with open(filename, "w") as f:
            json.dump(pet_data, f)

    @abstractmethod
    def speak(self) -> str:
        pass

    @property
    def name(self):
        return self._name
    
    @property
    def hunger(self):
        return self._hunger
    
    @property
    def happiness(self):
        return self._happiness
    
    @property
    def cleanliness(self):
        return self._cleanliness
    
    @property
    def energy(self):
        return self._energy
    
    def feed(self):
        if self._has_run_away:
            return "You can no longer feet your pet. It has run away."
        if self._hunger >= 100:
            return f"{self.name} is already full!"
        else:
            self._hunger = min(100, self._hunger + 20)
            self._update_last_interaction()
            return f"You fed {self.name}"

    def clean(self):
        if self._has_run_away:
            return ("You can no longer clean your pet. It has run away.")
        if self._cleanliness >= 100:
            return f"{self.name} is already squeaky clean!"
        else:
            self._cleanliness = min(100, self._cleanliness + 20)
            self._update_last_interaction()
            return f"You cleaned {self.name}"

    def play(self):
        if self._has_run_away:
            return ("You can no longer play with your pet. It has run away.")
        if self._happiness >= 100:
            return f"{self.name} is already super happy!"
        else:
            self._happiness = min(100, self._happiness + 20)
            self._energy = max(0, self._energy - 10)
            self._update_last_interaction()
            return f"You played with {self.name}"

    def sleep(self):
        if self._has_run_away:
            return ("Your pet has run away and can not sleep anymore.")
        if self._energy >= 100:
            return f"{self.name} is already full of energy!"
        else:
            self._energy = min(100, self._energy + 100)
            self._update_last_interaction()
            return "Your pet is sleeping"

    def is_gone(self):
        if self._has_run_away:
            return True
        if self._zero_since and (time.time() - self._zero_since > 900):
            self._has_run_away = True
            return True
        return False
    
    def get_mood(self):
        avg = (self._hunger + self._cleanliness + self._happiness + self._energy) / 4

        if avg >= 80:
            return "Very happy!"
        elif avg >= 50:
            return "Doing okay."
        elif avg >= 20:
            return "Not feeling well..."
        elif avg > 0:
            return "Barely holding on..."
        else:
            return "Totally neglected!"


class Cat(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self._happiness = 80
        self._energy = 60

    def speak(self):
        return "meow ≽^•⩊•^≼"
    
class Dog(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self._energy = 80
        self._cleanliness = 80

    def speak(slef):
        return "woof ૮ • ﻌ - ა"
