from constant import *
import config
import draw
import game
import game_text
import magic
import buttonmanager


class TextButton:
    def __init__(self, button_text, size, center, colour, clickable=True):
        """
        Class representing button with text

        Args:
            button_text (String): String to display on button
            size ((int, int)): Size of button
            center ((int, int)): Coord of center of button
            colour (Colour): Colour of button
            clickable (Boolean): If button is clickable/mouse-overable

        Attributes:
            normal_colour (Colour): Normal colour of button
            mouse_over_colour (Colour): Mouse over colour of button
        """
        self.button_text = button_text
        self.size = size
        self.center = center
        self.colour = colour
        self.clickable = clickable

        self.normal_colour = self.colour
        # Darkens color
        self.mouse_over_colour = (max(self.colour[0] - 50, 0),
                                  max(self.colour[1] - 50, 0),
                                  max(self.colour[2] - 50, 0))

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center

    def draw(self):
        """
        Draws button with text on it
        """
        pygame.draw.rect(config.SURFACE_MAIN, self.colour, self.rect)
        game_text.draw_text(config.SURFACE_MAIN, self.center, BLACK, self.button_text, center=True)

    def mouse_over(self):
        """
        Checks if button is moused over and if so, darken it

        If button is clickable and moused over, darken the button,
        else return button to normal colour
        """
        if self.clickable:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            mouse_over = (self.rect.left <= mouse_x <= self.rect.right and
                          self.rect.top <= mouse_y <= self.rect.bottom)

            if mouse_over:
                self.colour = self.mouse_over_colour
            else:
                self.colour = self.normal_colour


def main():
    """
    Main menu before starting game

    Menu has new game, continue game (only available if save.txt > 1kb in size) and exit
    """
    # Make buttons
    if os.stat(SAVE_PATH).st_size == 0:
        continue_clickable = False
    else:
        continue_clickable = True

    new_button = TextButton("New Game", (BUTTON_WIDTH, BUTTON_HEIGHT),
                            (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 4 + 100), RED)

    continue_button = TextButton("Continue", (BUTTON_WIDTH, BUTTON_HEIGHT),
                                 (CAMERA_WIDTH // 2, new_button.rect.midbottom[1] + 100), GREEN, continue_clickable)

    exit_button = TextButton("Exit", (BUTTON_WIDTH, BUTTON_HEIGHT),
                             (CAMERA_WIDTH // 2, continue_button.rect.midbottom[1] + 100), GREY)

    g = game.Game()

    while True:
        config.SURFACE_MAIN.fill(WHITE)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        new_button.mouse_over()
        continue_button.mouse_over()
        exit_button.mouse_over()

        new_button.draw()

        continue_button.draw()

        exit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if new_button.rect.collidepoint((mouse_x, mouse_y)):
                        game.populate_map()
                        g.run()
                    elif continue_button.rect.collidepoint((mouse_x, mouse_y)) and continue_button.clickable:
                        game.load_game()
                        g.run()
                    elif exit_button.rect.collidepoint((mouse_x, mouse_y)):
                        pygame.quit()

        pygame.display.update()


def pause():
    """
    Pause menu with continue button, save and exit button and exit button
    """
    # Make buttons
    resume_button = TextButton("Resume", (BUTTON_WIDTH, BUTTON_HEIGHT),
                               (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 4 + 100), GREEN)

    save_and_quit_button = TextButton("Save and quit", (BUTTON_WIDTH, BUTTON_HEIGHT),
                                      (CAMERA_WIDTH // 2, resume_button.rect.midbottom[1] + 100), RED)

    exit_button = TextButton("Exit", (BUTTON_WIDTH, BUTTON_HEIGHT),
                             (CAMERA_WIDTH // 2, save_and_quit_button.rect.midbottom[1] + 100), GREY)

    pause_menu = True
    while pause_menu:
        config.SURFACE_MAIN.blit(config.SPRITE.unfocused_window, (0, 0))

        game_text.draw_text(config.SURFACE_MAIN,
                            (CAMERA_WIDTH // 2, resume_button.rect.midtop[1] - 100), WHITE,
                            "PAUSED", BLACK, center=True)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        resume_button.mouse_over()
        save_and_quit_button.mouse_over()
        exit_button.mouse_over()

        resume_button.draw()

        save_and_quit_button.draw()

        exit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if resume_button.rect.collidepoint((mouse_x, mouse_y)):
                        pause_menu = False
                        break
                    elif save_and_quit_button.rect.collidepoint((mouse_x, mouse_y)) and resume_button.clickable:
                        game.quit_game()
                    elif exit_button.rect.collidepoint((mouse_x, mouse_y)):
                        pygame.quit()

        config.CLOCK.tick(FPS)
        pygame.display.update()


def map_menu():
    """
    Creates full map menu

    Only input available is closing game or clicking any other button to close map
    """
    menu_closed = False
    while not menu_closed:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    button = config.BUTTON_PANEL.check_if_button_pressed(mouse_x, mouse_y)
                    if button:
                        menu_closed = True
                        break

        draw.draw_map_menu(config.MAP_INFO)
        config.BUTTON_PANEL.draw_buttons(config.SURFACE_MAIN)
        config.CLOCK.tick(FPS)
        pygame.display.update()


def magic_targetting_menu():
    """
    Selects target for spell and cast magic and updates display
    """
    magic_cast = True
    while magic_cast:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    magic_cast = False
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    button = config.BUTTON_PANEL.check_if_button_pressed(mouse_x, mouse_y)
                    if button:
                        button.left_click_fn()
                        break

                    game.cast_magic(line)
                    magic_cast = False
                    break

        config.CLOCK.tick(FPS)
        game.update()
        draw.draw_mouse()
        m_x, m_y = config.CAMERA.get_mouse_coord()
        line = magic.line(config.PLAYER.position, (m_x, m_y), config.MAP_INFO.tile_array, config.FOV)
        draw.draw_magic_path(line)
        pygame.display.flip()


def stat_menu():
    """
    Draws stat menu
    """
    menu_width, menu_height = config.CAMERA.camera_width / 3, config.CAMERA.camera_height / 3
    stat_surface = pygame.Surface((menu_width, menu_height))

    # Could move this to _draw_stat if you want animated character icon in stat menu
    character_icon = pygame.transform.scale(config.PLAYER.image, (SPRITE_SIZE * 2, SPRITE_SIZE * 2))

    stat_open = True
    while stat_open:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                stat_open = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                stat_open = False
                break

        config.CLOCK.tick(FPS)
        game.update()
        _draw_stat(config.PLAYER, stat_surface, character_icon)
        # Centers stat_menu
        stat_rect = stat_surface.get_rect()
        stat_rect.center = (config.CAMERA.camera_width // 2, config.CAMERA.camera_height // 2)

        config.SURFACE_MAIN.blit(stat_surface, stat_rect)
        draw.draw_mouse()

        pygame.display.flip()


def _draw_stat(player, surface, character_icon):
    """
    Draws player stat to stat_surface

    Args:
        player (Entity): Player's stat to draw
        surface (Surface): Surface to draw stats on
        character_icon (Sprite): Sprite of character
    """
    max_hp = player.creature.stat.max_hp
    max_mp = player.creature.stat.max_mp
    hp = player.creature.stat.hp
    mp = player.creature.stat.mp
    strength = player.creature.stat.strength
    defense = player.creature.stat.defense
    wizardry = player.creature.stat.wizardry
    exp = player.creature.stat.exp
    level = player.creature.stat.level

    stat_list = ["hp: " + str(hp) + "/" + str(max_hp),
                 "mp: " + str(mp) + "/" + str(max_mp),
                 "strength: " + str(strength),
                 "defense: " + str(defense),
                 "wizardry: " + str(wizardry),
                 "exp: " + str(exp) + "/ 100",
                 "level: " + str(level)]

    for i, stat in enumerate(stat_list):
        game_text.draw_text(surface, (character_icon.get_width(), FONT_SIZE * i),
                            WHITE, stat)

    surface.blit(character_icon, (0, 0))


def inventory_menu():
    """
    create screens for inventory + equipment menus
    """
    menu_closed = False
    menu_width, menu_height = config.CAMERA.camera_width / 2, config.CAMERA.camera_height
    menu_surface = pygame.Surface((menu_width, menu_height - SPRITE_SIZE))
    menu_surface.fill(INVENTORY_BEIGE)

    while not menu_closed:
        events_list = pygame.event.get()
        game.update()

        config.SURFACE_MAIN.blit(menu_surface, (menu_width, 0))

        equipment = _load_equipment_screen()
        equipment.draw_buttons(config.SURFACE_MAIN)

        inventory = _load_inventory_screen()
        inventory.draw_buttons(config.SURFACE_MAIN)

        draw.draw_mouse()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_button = inventory.check_if_button_hovered(mouse_x, mouse_y)

        if hovered_button and hovered_button.mouse_over_fn:
            hovered_button.mouse_over_fn()

        for event in events_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    inventory_button = config.BUTTON_PANEL.check_if_specific_button_pressed(
                        'inventory', mouse_x, mouse_y)
                    if inventory_button:
                        menu_closed = True
                        break

                    minimap_button = config.BUTTON_PANEL.check_if_specific_button_pressed(
                        'minimap', mouse_x, mouse_y)
                    if minimap_button:
                        game.toggle_minimap()
                        break

                    item_slot = inventory.check_if_button_pressed(mouse_x, mouse_y)
                    if item_slot and item_slot.left_click_fn:
                        item_slot.left_click_fn()

                    equip_slot = equipment.check_if_button_pressed(mouse_x, mouse_y)
                    if equip_slot and equip_slot.left_click_fn:
                        equip_slot.left_click_fn()

                elif event.button == 3:
                    clicked_button = inventory.check_if_button_pressed(mouse_x, mouse_y)
                    if clicked_button and clicked_button.right_click_fn:
                        clicked_button.right_click_fn()
                        game.update_creatures(config.GAME_DATA.creature_data, 0, 0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    game.toggle_minimap()
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_closed = True

        config.CLOCK.tick(FPS)
        pygame.display.update()


def _load_equipment_screen():
    """
    Helper method to create equipment screen with equip slots

    Returns:
        equip_slot (ButtonManager): ButtonManager representing equip slots + equipped items
    """
    menu_width = config.CAMERA.camera_width / 2

    num_of_row = TILE_WIDTH // 2
    num_of_col = TILE_HEIGHT // 2

    equip_slot = buttonmanager.ButtonManager(menu_width, 0, num_of_row, num_of_col)

    hand_scale = (SPRITE_SIZE * 2, SPRITE_SIZE * 4)
    armor_scale = (SPRITE_SIZE * 4, SPRITE_SIZE * 6)

    # Make equipment slots
    left_hand_slot = pygame.transform.scale(config.SPRITE.empty_inventory_slot, hand_scale)
    left_hand = buttonmanager.IconButton(0, SPRITE_SIZE * 1, left_hand_slot)
    equip_slot.add_button(left_hand, "Left hand")

    right_hand_slot = pygame.transform.scale(config.SPRITE.empty_inventory_slot, hand_scale)
    right_hand = buttonmanager.IconButton(SPRITE_SIZE * 6, SPRITE_SIZE * 1, right_hand_slot)
    equip_slot.add_button(right_hand, "Right hand")

    armor_slot = pygame.transform.scale(config.SPRITE.empty_inventory_slot, armor_scale)
    armor = buttonmanager.IconButton(SPRITE_SIZE * 2, 0, armor_slot)
    equip_slot.add_button(armor, "Armor")

    # Find all entities equipped by player
    equipped_entities = config.PLAYER.creature.equipment.values()
    for equip_entity in equipped_entities:
        if equip_entity and equip_entity.equipment.equipped:
            slot = equip_entity.equipment.slot
            if slot == "Left hand":
                scaled_equip = pygame.transform.scale(equip_entity.image, hand_scale)
                left_hand_slot.blit(scaled_equip, (0, 0))
                left_hand.left_click_fn = equip_entity.equipment.toggle_equip
            elif slot == "Right hand":
                scaled_equip = pygame.transform.scale(equip_entity.image, hand_scale)
                right_hand_slot.blit(scaled_equip, (0, 0))
                right_hand.left_click_fn = equip_entity.equipment.toggle_equip
            elif slot == "Armor":
                scaled_equip = pygame.transform.scale(equip_entity.image, armor_scale)
                armor_slot.blit(scaled_equip, (0, 0))
                armor.left_click_fn = equip_entity.equipment.toggle_equip


    return equip_slot



# def _load_equipment_screen():
#     """
#     Helper to create equipment_screen with items
#     :return:  equipment_surface
#     """
#     equipment_rects = []
#
#     menu_width, menu_height = config.CAMERA.camera_width / 2, config.CAMERA.camera_height / 2
#     equipment_surface = pygame.Surface((menu_width, menu_height))
#
#     helmet_tl, helmet_br = (243, 24), (294, 67)
#     armor_tl, armor_br = (218, 70), (319, 185)
#     amulet_tl, amulet_br = (323, 52), (361, 89)
#     main_tl, main_br = (38, 83), (114, 274)
#     off_tl, off_br = (390, 83), (466, 274)
#     ringL_tl, ringL_br = (176, 171), (214, 208)
#     ringR_tl, ringR_br = (323, 171), (361, 208)
#     pants_tl, pants_br = (218, 188), (319, 301)
#     gloves_tl, gloves_br = (134, 230), (209, 299)
#     boots_tl, boots_br = (232, 308), (305, 356)
#
#     helmet_rect = pygame.Rect(helmet_tl, ((helmet_br[0] - helmet_tl[0]), (helmet_br[1] - helmet_tl[1])))
#     armor_rect = pygame.Rect(armor_tl, ((armor_br[0] - armor_tl[0]), (armor_br[1] - armor_tl[1])))
#     amulet_rect = pygame.Rect(amulet_tl, ((amulet_br[0] - amulet_tl[0]), (amulet_br[1] - amulet_tl[1])))
#     main_rect = pygame.Rect(main_tl, ((main_br[0] - main_tl[0]), (main_br[1] - main_tl[1])))
#     off_rect = pygame.Rect(off_tl, ((off_br[0] - off_tl[0]), (off_br[1] - off_tl[1])))
#     ringL_rect = pygame.Rect(ringL_tl, ((ringL_br[0] - ringL_tl[0]), (ringL_br[1] - ringL_tl[1])))
#     ringR_rect = pygame.Rect(ringR_tl, ((ringR_br[0] - ringR_tl[0]), (ringR_br[1] - ringR_tl[1])))
#     pants_rect = pygame.Rect(pants_tl, ((pants_br[0] - pants_tl[0]), (pants_br[1] - pants_tl[1])))
#     gloves_rect = pygame.Rect(gloves_tl, ((gloves_br[0] - gloves_tl[0]), (gloves_br[1] - gloves_tl[1])))
#     boots_rect = pygame.Rect(boots_tl, ((boots_br[0] - boots_tl[0]), (boots_br[1] - boots_tl[1])))
#
#     equipment_rects.append(helmet_rect)
#     equipment_rects.append(armor_rect)
#     equipment_rects.append(amulet_rect)
#     equipment_rects.append(main_rect)
#     equipment_rects.append(off_rect)
#     equipment_rects.append(ringL_rect)
#     equipment_rects.append(ringR_rect)
#     equipment_rects.append(pants_rect)
#     equipment_rects.append(gloves_rect)
#     equipment_rects.append(boots_rect)
#
#     for rect in equipment_rects:
#         pygame.draw.rect(equipment_surface, INVENTORY_BEIGE, rect)
#
#     equipment_surface.blit(config.SPRITE.equip_screen, (0, 0))
#
#     return equipment_surface
#
#     # equip_dictionary = {
#     #     "main": None,
#     #     "off": None,
#     #     "helmet": None,
#     #     "armor": None,
#     #     "amulet": None,
#     #     "ring": None,
#     #     "pants": None,
#     #     "boots": None,
#     #     "gloves": None,
#     # }


def _load_inventory_screen():
    """
    Helper method to create inventory screen with items

    Returns:
        inventory (GridButtonManager): GridButtonManager representing inventory + items
    """
    menu_width, menu_height = config.CAMERA.camera_width / 2, config.CAMERA.camera_height / 2
    counter = 0

    num_item_in_row = TILE_WIDTH // 2
    num_item_in_col = TILE_HEIGHT // 2 - 1

    inventory = buttonmanager.GridButtonManager(menu_width, menu_height, num_item_in_row, num_item_in_col,
                                                (num_item_in_row * num_item_in_col))

    for y in range(num_item_in_col):
        for x in range(num_item_in_row):
            inventory_array = config.PLAYER.container.inventory
            # Separate surface for item
            item_slot = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
            item_slot.blit(config.SPRITE.empty_inventory_slot, (0, 0))

            inventory.create_button(item_slot, str(x + (num_item_in_row * y)))
            if len(inventory_array) >= counter + 1:
                button = inventory.get_button(str(x + (num_item_in_row * y)))
                item_entity = inventory_array[counter]
                item_slot.blit(item_entity.image, (0, 0))
                counter = counter + 1

                _create_item_mouse_interaction(button, item_entity, menu_height, menu_width)

    return inventory


def _create_item_mouse_interaction(button, item_entity, menu_height, menu_width):
    """
    Creates all mouse interaction for button

    Args:
        button (IconButton): IconButton to create mouse interaction for
        item_entity (Entity): Entity representing item that IconButton is
            holding/creating actions for
        menu_width (int): Where GridButtonManager is (needed for finding where to
            place hover box)
        menu_height (int): Where GridButtonManager is (needed for finding where to
            place hover box)
    """
    _create_item_mouse_interaction_hover(button, item_entity, menu_height, menu_width)

    _create_item_mouse_interaction_right_click(button, item_entity)

    _create_item_mouse_interaction_left_click(button, item_entity)


def _create_item_mouse_interaction_left_click(button, item_entity):
    """
    Creates IconButton left mouse click action for items

    Args:
        button (IconButton): IconButton to create interaction for
        item_entity (Entity): Entity representing item that IconButton is
            holding/creating actions for
    """
    button.left_click_fn = item_entity.item.use_item


def _create_item_mouse_interaction_right_click(button, item_entity):
    """
    Creates IconButton right mouse click action for items

    Args:
        button (IconButton): IconButton to create interaction for
        item_entity (Entity): Entity representing item that IconButton is
            holding/creating actions for
    """
    item_entity.item.drop_item_args = (item_entity.item.current_container.owner)
    button.right_click_fn = item_entity.item.drop_item_fn_pointer
    # button.right_click_fn = (lambda: item_entity.item.drop_item(config.PLAYER, config.PLAYER.x, config.PLAYER.y))


def _create_item_mouse_interaction_hover(button, item_entity, menu_height, menu_width):
    """
    Creates IconButton hover mouse action for items

    Args:
        button (IconButton): IconButton to create interaction for
        item_entity (Entity): Entity representing item that IconButton is
            holding/creating actions for
        menu_width (int): Where GridButtonManager is (needed for finding where to
            place hover box)
        menu_height (int): Where GridButtonManager is (needed for finding where to
            place hover box)
    """
    button_x, button_y = button.rect.topleft
    item_entity.item.hover_args = (button_x, button_y, menu_width, menu_height)
    button.mouse_over_fn = item_entity.item.hover_over_item
    # button.mouse_over_fn = (lambda: test_fn(lambda: item_mouse_over(item_entity, button, menu_width, menu_height)))
