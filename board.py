import random
from cell import Cell

class Board:
    def __init__(self, width: int, height: int, bomb_count: int) -> None:
        self.cells = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.height = height
        self.width = width
        self.bomb_count = bomb_count
        self.amount_of_placed_flags = 0

    def print_board(self) -> None:

        print(f"Flags: {self.bomb_count-self.amount_of_placed_flags}/{self.bomb_count}")

        digits_width = len(str(self.height))

        print(" " * (digits_width + 2), end="")

        for i in range(self.height):
            print(f"{" " * (2 - len(str(i+1)))}{int(i+1)} ", end="")
            if i == 8:
                print(" ", end="")
                
        print("")
        print(f"{" " * (digits_width + 2)}{"---" * self.height}")

        for i, row in enumerate(self.cells):
            indent = digits_width - len(str(i+1)) + 1
            
            print(f"{i+1}{" " * indent}| ", end="")
            
            print("  ".join(str(cell) for cell in row))

    def activate_cell(self, x: int, y: int) -> str | None:
        cell = self.cells[y][x]

        if cell.is_bomb:
            cell.activate()    
            return "You hit a mine, you lost."
        
        if cell.is_clicked:
            return f"This cell ({x + 1}, {y + 1}) is already active."
        
        if cell.is_flagged:
            return f"This cell ({x + 1}, {y + 1}) is a flag."
        
        cell.activate()

        if cell.adjacent_bombs == 0:
            
            adjacent_positions = [(cell.x + dx, cell.y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
            for x, y in adjacent_positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.activate_cell(x, y)
    
    def toggle_flag(self, x: int, y: int) -> None:
        if self.cells[x][y].is_clicked:
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
    
    def check_win(self) -> bool: 
        if self.bomb_count == self.amount_of_placed_flags:
            for row in self.cells:
                for cell in row:
                    if cell.is_bomb and not cell.is_flagged:
                        return False
        else:
            for row in self.cells:
                for cell in row:
                    if not cell.is_clicked and not cell.is_bomb:
                        return False

        return True
