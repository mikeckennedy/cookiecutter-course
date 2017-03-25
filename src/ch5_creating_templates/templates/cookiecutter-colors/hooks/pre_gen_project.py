import sys


def validate():
    creator = '{{ cookiecutter.creator }}'

    if not creator.strip():
        print("You must specify a creator to use this template.")
        sys.exit(1)

    favorite_color = '{{ cookiecutter.favorite_color }}'
    if favorite_color == 'black':
        print("Currently black is actually not implemented!")
        sys.exit(7)


if __name__ == '__main__':
    validate()
