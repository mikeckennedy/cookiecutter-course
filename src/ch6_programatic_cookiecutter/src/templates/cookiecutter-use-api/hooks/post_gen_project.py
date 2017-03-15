import os
import sys


def main():
    sys.exit(clean_unused_color_files())


def clean_unused_color_files():
    selected_game = '{{ cookiecutter.game_type }}'
    working = os.path.abspath(os.path.join(os.path.curdir))
    files = ["hilo.py", "pacman.py", "pong.py"]
    for file in files:
        if selected_game + ".py" != file:
            os.remove(os.path.join(working, file))

    full_selected = os.path.join(working, selected_game + ".py")
    game = os.path.join(working, 'game.py')
    os.rename(full_selected, game)
    return 0


if __name__ == '__main__':
    main()
