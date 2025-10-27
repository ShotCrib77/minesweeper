import os
from board import Board

def start_screen() -> None:

    def options():
        print("Temporary options menu :)")
        input("Press enter to go back...")

    os.system("cls" if os.name == "nt" else "clear")
    print("Welcome to minesweeper")
    print("----------------------")
    print("1. Start game")
    print("2. Options")
    print("3. Quit")

    choosen_option = input("\nChoose an option: ").strip()

    if choosen_option == "1":
        return
    elif choosen_option == "2": # Är det bättre att skriva return start_screen() på båda ställen för tydlighets skull eller bör man bara ha 1?
        options()
        return start_screen()
    elif choosen_option == "3":
        print("Goodbye")
        exit()
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Wrong input format.")
    
        return start_screen()

def get_user_input_coordinate(skip_menu_option: bool = False, option: str | None = None) -> tuple[str, tuple[int, int]]:

    if not skip_menu_option:
        while True:
            print("1. Activate coordinate (M1 click).")
            print("2. Place Flag (M2 click).")
            print("----------------------------------")

            option = input("Choose option: ").strip()

            if option in ["1", "2"]:
                break
            else:
                print("Invalid option. Enter 1 or 2. \n")

    while True:
        user_coordinate_input = input("Input format - x, y (or *back* to go back to the options menu): ").strip()

        if user_coordinate_input.lower() == "back":
            return get_user_input_coordinate()
        
        try:
            x, y = user_coordinate_input.split(",")
            x, y = int(x), int(y[-1])
            return option, (x-1, y-1) # Ändra till indexvärdet som måste vara ofsett med -1
        except (ValueError, IndexError):
            print("Wrong input format.")
            return get_user_input_coordinate(True, option)    

def main() -> None:
    start_screen()
    
    board = Board(7, 7, 10)
    board.print_board()
    
    _, (x, y) = get_user_input_coordinate(skip_menu_option=True)
    os.system("cls" if os.name == "nt" else "clear")


    board.activate_cell(x, y)
    
    while True:
        cell_value = None
    
        board.print_board()
    
        option, (x, y) = get_user_input_coordinate()
        os.system("cls" if os.name == "nt" else "clear")
        if option == "1":
            cell_value = board.activate_cell(x, y)
        elif option == "2":
            board.toggle_flag(x, y)
        
        if cell_value:
            print(f"{cell_value}")
            if cell_value == "You hit a mine, you lost.":
                board.print_board()
                break
        
        if board.check_win():
            board.print_board()
            print("You won!")
            break

if __name__ == "__main__":
    main()
