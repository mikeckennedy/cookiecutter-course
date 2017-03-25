import os


def main():
    favorite_color = '{{cookiecutter.favorite_color}}'
    remove_unused_project_files(favorite_color)
    display_getting_started_instructions(favorite_color)


# Selected project files based on user choices
def remove_unused_project_files(favorite_color):
    working_dir = os.path.join(
        os.path.abspath(os.path.curdir), 'color_files')

    file_list = []
    if favorite_color == 'yellow':
        file_list = ['blue_file.txt', 'green_file.txt']
    if favorite_color == 'green':
        file_list = ['blue_file.txt', 'yellow_file.txt']
    if favorite_color == 'blue':
        file_list = ['green_file.txt', 'yellow_file.txt']

    delete_files(file_list, working_dir)


def delete_files(file_list, working_dir):
    for file in file_list:
        full_file = os.path.join(working_dir, file)
        if os.path.exists(full_file):
            os.remove(full_file)
        else:
            print("WARNING: Could not file to remove in hook: " + full_file)


def display_getting_started_instructions(favorite_color):
    print()
    print("------------------------------------------")
    print("  Welcome to the color project: " + favorite_color)
    print("  Your world is a rainbow (but mostly " + favorite_color + ")")
    print("------------------------------------------")
    print()
    print("To get started, read the readme.md")
    print()


if __name__ == '__main__':
    main()
