
def main():
    create_info = gather_inputs()
    proj_dir = build_game(create_info)


def gather_inputs():
    return ""


def build_game(create_info):
    return ""


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
