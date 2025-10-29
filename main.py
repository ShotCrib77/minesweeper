import pygame as pg
from board import Board


pg.init()
pg.font.init()
pg.mixer.init()

my_font = pg.font.SysFont('yugothicuiregular', 30)

tick_sound_effect = pg.mixer.Sound("Sound/tick.wav")
win_sound_effect = pg.mixer.Sound("Sound/win.wav")
lose_sound_effect = pg.mixer.Sound("Sound/lose.wav")

tick_sound_effect.set_volume(0.5)
win_sound_effect.set_volume(0.5)
lose_sound_effect.set_volume(0.5)

def game_over_screen(screen: pg.Surface, screen_size: int, image_src):

    game_over_surface = pg.Surface((screen_size, screen_size))
    game_over_surface.fill((0, 0, 0))
    game_over_surface.set_alpha(75)

    result_image = pg.image.load(image_src).convert()
    result_image.set_colorkey((255, 255, 255))
    result_image_rect = result_image.get_rect()
    result_image_rect.center = (screen_size // 2, screen_size // 2)

    play_again_image = pg.image.load("images/play_again.png").convert()
    play_again_image_rect = play_again_image.get_rect()
    play_again_image_rect.center = (screen_size // 2, screen_size // 2)
    play_again_image_rect.y = play_again_image_rect.y + result_image.get_height() - 30


    # Image resize if images are more than half of the screen
    combined_height = result_image.get_height() + play_again_image.get_height() + 20
    max_height = screen_size/2
    if combined_height > (max_height):
        scale_factor = max_height / combined_height
        
        result_image = pg.transform.scale(result_image, (int(result_image.get_width() * scale_factor), int(result_image.get_height() * scale_factor)))
        play_again_image = pg.transform.scale(play_again_image, (int(play_again_image.get_width() * scale_factor), int(play_again_image.get_height() * scale_factor)))


        result_image_rect = result_image.get_rect()
        result_image_rect.center = (screen_size // 2, screen_size // 2)
        
        play_again_image_rect = play_again_image.get_rect()
        play_again_image_rect.center = (screen_size // 2, screen_size // 2)
        play_again_image_rect.y = play_again_image_rect.y + result_image.get_height() - 30

        
    screen.blit(game_over_surface, (0, 0))
    screen.blit(result_image, result_image_rect)
    screen.blit(play_again_image, play_again_image_rect)
    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_image_rect.collidepoint(event.pos[0], event.pos[1]):
                    return True
            
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                return True



def main():

    def input_coordinates_to_index(click_x, click_y):
        x = (click_x - margin) // tile_size
        y = (click_y - margin) // tile_size

        if click_x <= margin or click_x > (screen_size - margin):
            x = False
        if click_y <= margin or click_y > (screen_size - margin):
            y = False
        
        return x, y

    bombs = 40
    board_size = 15 # 15 x 15
    margin = 50
    tile_size = 60
    screen_size = board_size*tile_size+(margin*2)
    screen_resolution = (screen_size, screen_size)
    
    screen = pg.display.set_mode(screen_resolution)
    pg.display.set_caption("Minesweeper")

    clock = pg.time.Clock()
    FPS = 60
    
    running = True

    while running:
        board = Board(board_size, board_size, bombs, margin = margin, tile_size=tile_size)
        first_click = True
        has_lost = False
        has_won = False

        
        playing = True
        while playing:
            clock.tick(FPS)
            current_time = pg.time.get_ticks()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    playing = False
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not has_lost:
                    x, y = input_coordinates_to_index(event.pos[0], event.pos[1])
    
                    if x is not False and y is not False:
                        if first_click:
                            first_click = False
                            bombs = board.populate_bombs(x, y)
                            text_surface = my_font.render(f"{bombs}/{bombs} flags", False, (30, 0, 0))
                            
                            board.check_adjacent_bombs()
                        
                        tick_sound_effect.play()

                        has_lost = board.activate_cell(x, y)
                        has_won =  board.check_win()
            
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and not has_lost:
                    if not first_click:
                        x, y = input_coordinates_to_index(event.pos[0] , event.pos[1])
                        if x is not False and y is not False:
                            board.toggle_flag(x, y)
                            flags = bombs - board.amount_of_placed_flags
                            text_surface = my_font.render(f"{flags}/{bombs} flags", False, (0, 0, 0))

                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 2 and not has_lost:
                    if not first_click:
                        x, y = input_coordinates_to_index(event.pos[0] , event.pos[1])
                        if x is not False and y is not False:
                            has_lost = board.middle_click(x, y)
                            has_won =  board.check_win()
                            tick_sound_effect.play()

            
            
            board.print_board(pg.display.get_surface())
            if not first_click:
                screen.blit(text_surface, (50,0))
            if has_lost:
                board.reveal_bombs()
                board.print_board(screen)
                
                lose_sound_effect.play()
                restart = game_over_screen(screen, screen_size, "images/you_lost.png")
                
                playing = False
                if not restart:
                    running = False
            
            if has_won:
                win_sound_effect.play()
                restart = game_over_screen(screen, screen_size, "images/winner.png")
                
                playing = False
                if not restart:
                    running = False
                

            pg.display.flip()
    
    pg.quit()

if __name__ == "__main__":
    main()