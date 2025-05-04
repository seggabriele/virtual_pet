import os
from factory import PetFactory, load_pet

if os.path.exists("pet_save.json"):
    try:
        pet = load_pet()
        print("Pet loaded successfully!")
    except Exception as e:
        print(f"Failed to load save. Starting fresh. Error: {e}")
        pet_type = input("Choose your pet (cat/dog): ")
        name = input("Give your pet a name: ")
        pet = PetFactory.create_pet(pet_type, name)
        print(f"You adopted {pet.name}! They say: {pet.speak()}")
else:
    pet_type = input("Choose your pet (cat/dog): ")
    name = input("Give your pet a name: ")
    pet = PetFactory.create_pet(pet_type, name)
    print(f"You adopted {pet.name}! They say: {pet.speak()}")

def show_menu():
    print("\nMenu:")
    print("1. Feed")
    print("2. Clean")
    print("3. Play")
    print("4. Sleep")
    print("5. Show Stats")
    print("6. Save Pet")
    print("7. Load Pet")
    print("8. Quit")

def show_stats(pet):
    print(f"\n--- {pet.name}'s Stats ---")
    print(f"Hunger: {pet.hunger}")
    print(f"Cleanliness: {pet.cleanliness}")
    print(f"Happiness: {pet.happiness}")
    print(f"Energy: {pet.energy}")
    print(f"Mood: {pet.get_mood()}")
    print("-------------------------")


while True:
    
    if pet.is_gone():
        print(f"\n:( {pet.name} has run away... You neglected them for too long.")
        show_stats(pet)
        print("\n(Your pet is gone...)")
        

    show_menu()
    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        pet._apply_stat_decay()
        message = pet.feed()
        print(message)
    elif choice == "2":
        pet._apply_stat_decay()
        message = pet.clean()
        print(message)
    elif choice == "3":
        pet._apply_stat_decay()
        message = pet.play()
        print(message)
    elif choice == "4":
        pet._apply_stat_decay()
        message = pet.sleep()
        print(message)
    elif choice == "5":
        pet._apply_stat_decay()
        show_stats(pet)
    elif choice == "6":
        pet._apply_stat_decay()
        pet.save()
        print ("Pet saved successfully!")
    elif choice == "7":
        from factory import load_pet
        try:
            pet = load_pet()
            print("Pet loaded :)")
        except Exception as e:
            print(f"Failed to load {e}")
    elif choice == "8":
        print("Bye bye!")
        break
    else:
        print("Invalid choice! Try again.")
