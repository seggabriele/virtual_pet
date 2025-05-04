import unittest
from unittest.mock import mock_open, patch
from pet import Cat, Dog
from factory import load_pet
import time
import json

class TestPet(unittest.TestCase):

    def setUp(self):
        self.cat = Cat("Kitty")
        self.dog = Dog("Puppy")

    def test_feed_increases_hunger(self):
        self.cat._hunger = 50
        result = self.cat.feed()
        self.assertIn("fed", result.lower())
        self.assertGreater(self.cat.hunger, 50)

    def test_feed_when_full(self):
        self.dog._hunger = 100
        result = self.dog.feed()
        self.assertIn("already full", result.lower())
        self.assertEqual(self.dog.hunger, 100)

    def test_sleep_restores_energy(self):
        self.cat._energy = 30
        self.cat.sleep()
        self.assertGreater(self.cat.energy, 30)

    def test_is_gone_false_initially(self):
        self.assertFalse(self.cat.is_gone())

    def test_get_mood(self):
        self.cat._hunger = 10
        self.cat._cleanliness = 10
        self.cat._happiness = 10 
        self.cat._energy = 10
        mood = self.cat.get_mood()
        self.assertEqual(mood, "Barely holding on...")

    def test_decay_applies_correctly(self):
        self.cat._created_at -= 900
        self.cat._last_decay_applied = 0
        self.cat._apply_stat_decay()
        self.assertLess(self.cat.hunger, 100)
        self.assertLess(self.cat.energy, 100)

    def test_save_creates_correct_json(self):
        pet = Cat("Test")
        pet._hunger = 88
        expected_data = {
            "type": "cat",
            "name": "Test",
            "hunger": 88,
            "cleanliness": 100,
            "happiness": 80,
            "energy": 60,
            "created_at": pet._created_at,
            "last_decay_applied": pet._last_decay_applied,
            "last_interaction_time": pet._last_interaction_time,
            "zero_since": pet._zero_since,
            "has_run_away": pet._has_run_away
        }

        with patch("builtins.open", mock_open()) as mocked_file:
            pet.save()
            mocked_file.assert_called_once_with("pet_save.json", "w")
            handle = mocked_file()
            written = "".join(call.args[0] for call in handle.write.call_args_list)
            self.assertEqual(json.loads(written), expected_data)

    def test_load_pet_restores_pet(self):
        fake_json = json.dumps({
            "type": "cat",
            "name": "Loaded",
            "hunger": 70,
            "cleanliness": 90,
            "happiness": 85,
            "energy": 60,
            "created_at": time.time(),
            "last_decay_applied": 3,
            "last_interaction_time": time.time(),
            "zero_since": None,
            "has_run_away": False                   
 })
        
        with patch("builtins.open", mock_open(read_data=fake_json)):
            pet = load_pet()
            self.assertEqual(pet.name, "Loaded")
            self.assertEqual(pet.hunger, 70)
            self.assertEqual(pet.cleanliness, 90)
            self.assertFalse(pet._has_run_away)


if __name__ == "__main__":
    unittest.main()