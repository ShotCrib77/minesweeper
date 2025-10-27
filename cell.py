import pygame as pg

class Cell:
    def __init__(self, x: int, y: int, cell_size) -> None:
        self.x = x
        self.y = y
        self.cell_size = cell_size

        self.image = pg.image.load("Sprites\\TileUnknown.png")
        self.scale_image()
        
        self.rect = self.image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size
        
        self.is_bomb = False
        self.is_flagged = False
        self.is_clicked = False
        self.adjacent_bombs = 0
    
    def update_status(self):
        if self.is_flagged:
            self.status = "flagged"
        elif self.is_clicked and self.is_bomb:
            return "M"
        elif self.is_clicked:
            return f"{self.adjacent_bombs}"
        else:
            return "▢"

    def __str__(self) -> str:
        if self.is_flagged:
            return "F"
        elif self.is_clicked and self.is_bomb:
            return "M"
        elif self.is_clicked:
            return f"{self.adjacent_bombs}"
        else:
            return "▢"

    def make_bomb(self) -> bool:
        if self.is_bomb:
            return False
        else:
            self.is_bomb = True
            return True
    
    def toggle_flag(self) -> None:
        self.is_flagged = not self.is_flagged
        
        if self.is_flagged:
            self.image = pg.image.load("Sprites\\TileFlag.png")
            self.scale_image()
        else:
            self.image = pg.image.load("Sprites\\TileUnknown.png")
            self.scale_image()

    def activate(self) -> bool:
        self.is_clicked = True
        
        if self.is_bomb:
            self.image = pg.image.load("Sprites\\TileExploded.png")
            self.scale_image()
        elif self.adjacent_bombs > 0:
            self.image = pg.image.load(f"Sprites\\Tile{self.adjacent_bombs}.png")
            self.scale_image()
        else:
            self.image = pg.image.load(f"Sprites\\TileEmpty.png")
            self.scale_image()
    
    def show_bomb(self):
        if self.is_bomb and not self.is_clicked:
            self.image = pg.image.load("Sprites\\TileMine.png")
            self.scale_image()

    def scale_image(self):
        self.image = pg.transform.scale(self.image, (self.cell_size, self.cell_size))

    def set_adjacent_bombs(self, bombs: int) -> None:
        self.adjacent_bombs = bombs