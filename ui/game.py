import pygame
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from button import Button
from factory import PetFactory, load_pet
from pet import Cat, Dog


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virtual Pet")

def get_asset_path(relative_path):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

cat_icon = pygame.image.load(get_asset_path("../assets/icons/cat_icon.png")).convert_alpha()
dog_icon = pygame.image.load(get_asset_path("../assets/icons/dog_icon.png")).convert_alpha()

cat_icon = pygame.transform.scale(cat_icon, (120, 120))
dog_icon = pygame.transform.scale(dog_icon, (120, 120))

cat_rect = cat_icon.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 15))
dog_rect = dog_icon.get_rect(center=(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2))


BG_COLOR = (244, 194, 194)

clock = pygame.time.Clock()
FPS = 10

def load_animation_frames(folder_relative_path):
    script_dir = os.path.dirname(__file__)
    folder_path = os.path.join(script_dir, folder_relative_path)
    
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            img_path = os.path.join(folder_path, filename)
            image = pygame.image.load(img_path).convert_alpha()
            frames.append(image)
    return frames

    
feed_img = pygame.transform.scale(pygame.image.load(get_asset_path("../assets/icons/food.png")).convert_alpha(),
(128, 128))
clean_img = pygame.transform.scale(pygame.image.load(get_asset_path("../assets/icons/soap.png")).convert_alpha(),
(128, 128))
play_img = pygame.transform.scale(pygame.image.load(get_asset_path("../assets/icons/ball.png")).convert_alpha(),
(128, 128))
sleep_img = pygame.transform.scale(pygame.image.load(get_asset_path("../assets/icons/bed.png")).convert_alpha(),
(128, 128))

feed_button = Button(feed_img, 10, 450)
clean_button = Button(clean_img, 210, 440)
play_button = Button(play_img, 410, 460)
sleep_button = Button(sleep_img, 610, 450)


current_frame = 0
animation_timer = 0
ANIMATION_SPEED = 0.1

pet = None
selecting_pet = True
typing_name = False
entered_name = ""
font = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 32)
idle_frames = []
happy_frames = []
active_frames = []
showing_happy = False
happy_start_time = 0
selected_type = None
pet_ran_away = False

save_text = font_small.render("Save Game", True, (0, 0, 0))
save_rect = save_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # viršuje dešinėje

reset_text = font_small.render("Reset Game", True, (0, 0, 0))
reset_rect = reset_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))


if os.path.exists("pet_save.json"):
    try:
        pet = load_pet()
        pet._apply_stat_decay()
        if isinstance(pet, Cat):
            idle_frames = load_animation_frames("../assets/cat_idle")
            happy_frames = load_animation_frames("../assets/cat_happy")
        elif isinstance(pet, Dog):
            idle_frames = load_animation_frames("../assets/dog_idle")
            happy_frames = load_animation_frames("../assets/dog_happy")
        active_frames = idle_frames
        selecting_pet = False
    except Exception as e:
        print(f"Failed to load saved pet: {e}")


running = True
while running:
    screen.fill(BG_COLOR)

    if pet and not pet_ran_away:
        pet._apply_stat_decay()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif selecting_pet and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if cat_rect.collidepoint(pos):
                selected_type = "cat"
                typing_name = True
            elif dog_rect.collidepoint(pos):
                selected_type = "dog"
                typing_name = True

        elif typing_name and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if selected_type == "cat":
                    pet = Cat(entered_name)
                    idle_frames = load_animation_frames("../assets/cat_idle")
                    happy_frames = load_animation_frames("../assets/cat_happy")
                elif selected_type == "dog":
                    pet = Dog(entered_name)
                    idle_frames = load_animation_frames("../assets/dog_idle")
                    happy_frames = load_animation_frames("../assets/dog_happy")
                selecting_pet = False
                typing_name = False
                active_frames = idle_frames
                entered_name = ""
            elif event.key == pygame.K_BACKSPACE:
                entered_name = entered_name[:-1]
            else:
                entered_name += event.unicode

        elif not selecting_pet and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if pet and pet.is_gone():
                    pet_ran_away = True

            if reset_rect.collidepoint(pos):
                pet = None
                idle_frames = []
                happy_frames = []
                active_frames = []
                selecting_pet = True
                typing_name = False
                entered_name = ""
                pet_ran_away = False
                print("Resetting game...")
            if not pet_ran_away:
                if feed_button.is_clicked(pos):
                    print(pet.feed())
                    showing_happy = True
                    happy_start_time = pygame.time.get_ticks()
                elif clean_button.is_clicked(pos):
                    print(pet.clean())
                    showing_happy = True
                    happy_start_time = pygame.time.get_ticks()
                elif play_button.is_clicked(pos):
                    print(pet.play())
                    showing_happy = True
                    happy_start_time = pygame.time.get_ticks()
                elif sleep_button.is_clicked(pos):
                    print(pet.sleep())
                    showing_happy = True
                    happy_start_time = pygame.time.get_ticks()
                elif save_rect.collidepoint(pos):
                    if pet:
                        pet.save()
                        print("Pet saved successfully.")


    if selecting_pet:
        screen.blit(cat_icon, cat_rect)
        screen.blit(dog_icon, dog_rect)
        if typing_name:
            name_text = font.render("Enter pet name: " + entered_name, True, (0, 0, 0))
            screen.blit(name_text, (SCREEN_WIDTH // 2 - 200, 50))

    elif idle_frames:
        if showing_happy and pygame.time.get_ticks() - happy_start_time > 2000:
            showing_happy = False
            current_frame = 0

        active_frames = happy_frames if showing_happy else idle_frames

        dt = clock.tick(FPS) / 1000
        animation_timer += dt

        if animation_timer >= ANIMATION_SPEED:
            current_frame = (current_frame + 1) % len(active_frames)
            animation_timer = 0

        pet_image = active_frames[current_frame]
        pet_rect = pet_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pet_image, pet_rect)

        feed_button.draw(screen)
        clean_button.draw(screen)
        play_button.draw(screen)
        sleep_button.draw(screen)
        screen.blit(save_text, save_rect)

        if pet:
            name_text = font.render(pet.name, True, (0, 0, 0))
            screen.blit(name_text, (20, 2))

        mood_text = font.render(f"Mood: {pet.get_mood()}", True, (0, 0, 0))
        screen.blit(mood_text, (20, 26))
        stats_text = [
            f"Hunger: {pet.hunger}",
            f"Happiness: {pet.happiness}",
            f"Cleanliness: {pet.cleanliness}",
            f"Energy: {pet.energy}"
        ]

        for i, line in enumerate(stats_text):
            stat_surface = font_small.render(line, True, (0, 0, 0))
            screen.blit(stat_surface, (20, 50 + i * 25))

        if pet_ran_away:
            runaway_text = font.render(f"{pet.name} has run away...", True, (255, 0, 0))
            screen.blit(runaway_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
        
        screen.blit(reset_text, reset_rect)


    pygame.display.update()
    clock.tick(FPS)



pygame.quit()
