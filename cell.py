class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.is_bomb = False
        self.is_flagged = False
        self.is_clicked = False
        self.adjacent_bombs = 0
    
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

    def activate(self) -> None:
        self.is_clicked = True
    
    def set_adjacent_bombs(self, bombs: int) -> None:
        self.adjacent_bombs = bombs