import random
import pygame as pg
from cell import Cell

class Board:
    def __init__(self, width: int, height: int, bomb_count: int, margin: int = 30, tile_size: int = 50) -> None:
        self.cells = [[Cell(x, y, tile_size) for x in range(width)] for y in range(height)]
        self.height = height
        self.width = width
        self.bomb_count = bomb_count
        self.amount_of_placed_flags = 0
        self.tile_size = tile_size
        self.margin = margin

    def print_board(self, screen: pg.Surface) -> None:
        screen.fill((230,230,230))
        for row in self.cells:
            for cell in row:
                screen.blit(cell.image, (cell.rect.x+self.margin, cell.rect.y+self.margin, self.tile_size, self.tile_size))
        

    def activate_cell(self, x: int, y: int) -> bool | None:
        cell = self.cells[y][x]

        if cell.is_flagged:
            return
        
        if cell.is_bomb:
            cell.activate()    
            return True

        if cell.is_clicked:
            return
        
        

        cell.activate()

        if cell.adjacent_bombs == 0:
            
            adjacent_positions = [(cell.x + dx, cell.y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
            for x, y in adjacent_positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.activate_cell(x, y)
    
    def toggle_flag(self, x: int, y: int) -> None:
        if self.cells[y][x].is_clicked:
            print(f"\n This Cell ({x + 1}, {y + 1}) is already active.")
            return
        if self.cells[y][x].is_flagged:
            self.amount_of_placed_flags -= 1
        elif self.amount_of_placed_flags < self.bomb_count:
            self.amount_of_placed_flags += 1
        else:
            print("\nYou have no flags left...")
            return

        self.cells[y][x].toggle_flag()

    def middle_click(self, x: int, y: int) -> bool|None:

        cell = self.cells[y][x]

        if not cell.is_clicked:
            return

        if self.adjacent_flags(x,y) == cell.adjacent_bombs:
            adjacent_positions = [(cell.x + dx, cell.y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
            for x, y in adjacent_positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    if self.activate_cell(x, y):
                        return True
    
    def populate_bombs(self, x: int, y: int) -> int:
        
        excluded_positions = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
        placed_bombs = 0
        failed_attempts = 0
        
        while placed_bombs < self.bomb_count:
            x = random.randint(0, len(self.cells[0]) - 1)
            y = random.randint(0, len(self.cells) - 1)
            if not (x, y) in excluded_positions and self.cells[y][x].make_bomb():
                placed_bombs += 1
            else:
                failed_attempts += 1
                if failed_attempts > self.bomb_count * 10:
                    return placed_bombs
        return placed_bombs
    
    def check_adjacent_bombs(self) -> None:
        for row in self.cells:
            for cell in row:
                bombs = 0
                adjacent_positions = [(cell.x + dx, cell.y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
                
                for x, y in adjacent_positions:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if self.cells[y][x].is_bomb:
                            bombs += 1
                cell.set_adjacent_bombs(bombs)
    
    def adjacent_flags(self, x: int, y: int) -> int:
        flags = 0
        cell = self.cells[y][x]
        adjacent_positions = [(cell.x + dx, cell.y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
        for x, y in adjacent_positions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.cells[y][x].is_flagged:
                    flags += 1
        return flags

    def check_win(self) -> bool: 
        for row in self.cells:
            for cell in row:
                if not (cell.is_clicked or cell.is_bomb):
                    return False

        return True

    def reveal_bombs(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.show_bomb()
