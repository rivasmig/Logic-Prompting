# will hold the main code for the UI
import pygame
from functools import partial
from ui import Button, Panel, Image, water_ripple

def play_sound(sound_path, outer_panel, button):
    # Load the sound
    sound_effect = pygame.mixer.Sound(sound_path)
    # Play the sound
    sound_effect.play()

def subtract_colors(color1, color2):
    return tuple(c1 - c2 for c1, c2 in zip(color1, color2))

def main():

    pygame.init()

    WINDOW_SIZE = [900, 600]

    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    main_panel = Panel.Panel(screen=screen, width=WINDOW_SIZE[0], 
                            height=WINDOW_SIZE[1], color=(230, 230, 230))

    img1 = Image.Image(outer_panel=main_panel, 
                                    image_path='assets\images\wii_menu_background.png', 
                                    width=1, height=1, position=(0,0))
    img1.stretch_fill()
    img1.set_transparency(0.3)

    img2 = Image.Image(outer_panel=main_panel,
                       image_path='assets\images\wii_menu_background.png', 
                       width=1, height=1, position=(0,0))
    img2.stretch_fill()
    img2.set_transparency(0.3)
    img2.flip_on_vertical_axis()

    b_color = (175, 0, 180)
    off_color = (10, 0, 10)
    button1 = Button.Button(outer_panel=main_panel, width=0.05, 
                        height=0.07, position=(-0.45, -0.2), 
                        default_color=b_color, 
                        default_hover_color= subtract_colors(b_color, off_color), 
                        shadow_offset=(10, 10), shadow_transparency= 0.6)
    button_action1 = partial(play_sound, sound_path="assets\sounds\wii_sounds\piano_no_reverb_key.wav", 
                            outer_panel=main_panel, button=button1)
    button1.one_time_action = button_action1

    button2 = Button.Button(outer_panel=main_panel, width=0.05, 
                            height=0.07, position=(-0.45, -0.1), 
                            default_color=b_color, 
                            default_hover_color= subtract_colors(b_color, off_color), 
                            shadow_offset=(10, 10), shadow_transparency= 0.6)
    button_action2 = partial(play_sound, sound_path="assets\sounds\wii_sounds\electric_piano_note.wav", 
                            outer_panel=main_panel, button=button2)
    button2.one_time_action = button_action2

    button3 = Button.Button(outer_panel=main_panel, width=0.05, 
                            height=0.07, position=(-0.45, 0), 
                            default_color=b_color, 
                            default_hover_color= subtract_colors(b_color, off_color), 
                            shadow_offset=(10, 10), shadow_transparency= 0.6)
    button_action3 = partial(play_sound, sound_path="assets\sounds\wii_sounds\orchestra_90s_hit.wav", 
                            outer_panel=main_panel, button=button3)
    button3.one_time_action = button_action3

    main_panel.Panel_Manager.add_image(img1)
    main_panel.Panel_Manager.add_image(img2)
    main_panel.Panel_Manager.add_button(button1)
    main_panel.Panel_Manager.add_button(button2)
    main_panel.Panel_Manager.add_button(button3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_SIZE[0], WINDOW_SIZE[1] = event.w, event.h
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                main_panel.Width = event.w  # Modified to use lowercase convention
                main_panel.Height = event.h  # Modified to use lowercase convention

        main_panel.Panel_Manager.handle_event(event)
        main_panel.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
