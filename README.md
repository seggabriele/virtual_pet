# Virtual Pet 

**OOP Coursework 2025**  
Author: Gabrielė Šėgždaitė  
Group: EKf-24
Topic: Virtual Pet (Tamagotchi-style game) with graphical interface using Pygame.

---

## 1. Introduction

This project is a virtual pet simulator where the user can adopt a pet (cat or dog), name it, and take care of its' well-being through a graphical interface. The game is developed in **Python**, applying **OOP principles**, with animations and a save/load system using **JSON files**.

### How to Run the Program

1. Install required dependencies (Pygame):
   ```bash
   pip install pygame
   ```

2. Launch the graphical game:
   ```bash
   python game.py
   ```

3. A simple console-based version is also available:
   ```bash
   python main.py
   ```

---

## 2. Analysis (OOP, design pattern, testing, file handling)

### OOP Principles Implemented

| Principle Usage  |
|------------------|

**Inheritance**: `Cat` and `Dog` classes inherit from the abstract `Pet` base class.

**Polymorphism**: The `speak()` method is overridden in each subclass.   

**Abstraction**: `Pet` is an abstract class using `ABC` and `@abstractmethod`.
**Encapsulation**: Attributes are private (`_attr`) and accessed via `@property`.

### Design Pattern: **Factory Pattern**

- Implemented in the `PetFactory` class to create pets based on user selection.
- The `load_pet()` function also acts as a loader factory that restores pet state from a JSON file.

### Composition

- The UI uses composition via the `Button` class, where multiple `Button` objects are drawn and checked for interaction in `game.py`.

### File Handling

- The pet's state is saved and loaded using the `pet_save.json` file.
- The `save()` method writes pet data, and `load_pet()` restores it.

### Testing

- Core logic is tested using the `unittest` module in `test_pet.py`:
  - Tests for `feed()`, `sleep()`, mood calculation, save/load, and stat decay.
  - Mocking is used to simulate file reading/writing.

---

## 3. Results

- A fully functional graphical virtual pet game was built with user interactions.
- All OOP pillars and required design patterns were implemented successfully.
- File I/O and automatic decay logic were integrated and tested.
- The code is organized using clean structure and PEP8 formatting.

---

## 4. Conclusions

This project allowed practice the application of all core OOP principles, test-driven development, and basic design patterns.  
Future improvements may include:
- More pet types with unique behaviors, moods
- Sound effects and animations per action
- Age system, illness, and advanced care needs
- Online save system or cloud sync using APIs

---

## Project Structure

```
virtual_pet/

main.py            # Console-based gameplay
pet.py             # Pet base class and Cat/Dog subclasses
factory.py         # Factory design pattern & file loading
pet_save.json      # JSON file for saving pet state
|---ui/
   button.py       # Reusable GUI Button class
   game.py         # Pygame game loop and GUI logic
|---tests
   test_pet.py     # Unit tests using unittest module
|---assets/        # Icons, animations (excluded from GitHub)
README.md          # This report file
```

---

## For the Lecturer

This OOP coursework is available on GitHub:  
👉 https://github.com/seggabriele/virtual_pet
