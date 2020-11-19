import os

token_dirs = [
    os.path.join(os.path.expanduser('~'), '.evernote2/token'),
    os.path.join('/etc', 'evernote2/token'),
]

EVERNTOE_TOKEN = None

for token_file in token_dirs:
    if os.path.exists(token_file):
        with open(token_file) as fr:
            content = ''.join(fr.readlines())
            EVERNTOE_TOKEN = content.strip()
        break


token_hint = 'evernote Developer Token not found. searched files: %s' \
    % ', '.join(token_dirs)
assert EVERNTOE_TOKEN is not None, token_hint


if __name__ == '__main__':
    print(EVERNTOE_TOKEN)
