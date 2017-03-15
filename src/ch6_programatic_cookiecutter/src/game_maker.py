import os

import collections
import cookiecutter.main
import cookiecutter.config
import subprocess

import sys

GameCreateInfo = collections.namedtuple('GameCreateInfo',
                                        'project_name full_name game_type working_dir')


def main():
    print_welcome()
    create_info = gather_inputs()
    # print(create_info)
    proj_dir = build_game(create_info)

    run = input(
        "We've created {} at {}/game.py. Want to run it? [y]es, no: ".format(
            create_info.project_name, proj_dir))
    game_path = os.path.join(proj_dir, 'game.py')

    if run == '' or run == 'y' or run == 'yes':
        subprocess.call(['python3', game_path], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)


def print_welcome():
    print("************ Welcome to the game creator! ************")
    print("We will create either hi-lo, pacman, or pong for you")
    print("******************************************************")
    print()


def gather_inputs():
    config = cookiecutter.config.get_user_config()
    ctx = config.get('default_context')

    full_name = ctx.get('full_name')
    if not full_name:
        full_name = input('What is your full name? ')

    game_type = None
    while game_type not in ['hilo', 'pacman', 'pong']:
        game_type = input('Game type? [hilo, pacman, pong]? ')

    package_name = input("What do you call your game? ")
    package_name = to_package_style(package_name)

    working_dir = input('Full path where to create the project [must exist]? ')
    while not os.path.exists(working_dir):
        print("Oh, that doesn't exist, try again...")
        working_dir = input('Full path where to create the project [must exist]? ')

    return GameCreateInfo(package_name, full_name, game_type, working_dir)


def build_game(info):
    print("Building game {} of type {}, just a moment ...".format(
        info.project_name, info.game_type), flush=True)

    working_dir = os.path.abspath(os.path.dirname(__file__))
    template = os.path.join(working_dir, 'templates', 'cookiecutter-use-api')

    proj_dir = cookiecutter.main.cookiecutter(
        template,
        no_input=True,
        output_dir=info.working_dir,
        extra_context={
            'project_name': info.project_name,
            'full_name': info.full_name,
            'game_type': info.game_type
        }
    )

    return proj_dir


def to_package_style(text):
    if not text:
        return text

    text = text.strip()
    url_txt = ''
    for ch in text:
        url_txt += ch if ch.isalnum() or ch == '.' else ' '

    count = -1
    while count != len(url_txt):
        count = len(url_txt)
        url_txt = url_txt.strip()
        url_txt = url_txt.replace('  ', ' ')
        url_txt = url_txt.replace(' ', '-')
        url_txt = url_txt.replace('--', '-')

    return url_txt.lower()


if __name__ == '__main__':
    main()
