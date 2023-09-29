
import argparse
from collections import namedtuple, OrderedDict
import os
import struct

GameSave = namedtuple('GameSave',
    ('forest_level', 'volcano_level', 'factory_level', 'beach_level',
    'unknown0', 'unknown1', 'unknown2', 'unknown3',
    'all_status', 'beach_status', 'factory_status', 'forest_status', 'volcano_status', 'high_score'))

DEFAULT_SAVE = GameSave(1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,)
GAME_SAVE_FIELD_COUNT = 14
SAVE_FIELD_PREFIX = (8, 2)
# Could be an Enum
LEVEL_TYPES = ('forest', 'volcano', 'factory', 'beach')
SAVE_ACTIONS = ('read', 'reset', 'overwrite')

def get_save_path():
    # Windows-specific
    return os.path.join(os.getenv('APPDATA'),
        'Godot', 'app_userdata', 'Mr. Platformer', 'progress.save')

def end_game_process():
    # Windows-specific
    print("[ending game processes]")
    os.system('''wmic process where "name='mrplatformer.exe'" delete''')

def read_save(save_path, message="read save"):
    save_items = []
    try:
        with open(save_path, 'rb') as infile:
            for i in range(GAME_SAVE_FIELD_COUNT):
                field_triplet = struct.unpack('<3i', infile.read(3*4))
                assert field_triplet[:2] == SAVE_FIELD_PREFIX
                save_items.append(field_triplet[2])
        save = GameSave(*save_items)
    except FileNotFoundError:
        save = None
    print(f"[{message}]\ncontents: {save}")

def overwrite_save(save_path, save):
    read_save(save_path, "previous save contents")
    save_items = GameSave(*save.values())
    print(f"[overwriting save]\ncontents: {save_items}")
    with open(save_path, 'wb') as outfile:
        for item in save_items:
            outfile.write(struct.pack('<3i', *SAVE_FIELD_PREFIX, item))

def delete_save(save_path):
    read_save(save_path, "previous save contents")
    print("[deleting save]")
    try:
        os.remove(save_path)
    except FileNotFoundError:
        pass

def main():
    parser = argparse.ArgumentParser(prog='mr_platformer_saves.py',
        description="Save editing tools for Terry Cavanagh's 2023 game Mr. Platformer",)
    parser.add_argument('--action', help='action to apply to save file', choices=SAVE_ACTIONS)
    for level in LEVEL_TYPES:
        parser.add_argument(f'--{level}', type=int, help=f'{level} levels index')
    parser.add_argument('--autofill', type=int, help='autofill non-specified level indexes with this value')
    parser.add_argument('--closegame', help='close any remaining game processes, foreground or background', action='store_true')
    if os.name != 'nt':
        # get_save_path and end_game_process are both Windows-specific
        raise OSError('Only Windows is currently supported')
    args = parser.parse_args()
    save_path = get_save_path()
    if args.closegame:
        end_game_process()
    action = args.action
    if action == 'overwrite':
        save = OrderedDict(DEFAULT_SAVE._asdict())
        autofill_value = args.autofill
        for level in LEVEL_TYPES:
            level_index = getattr(args, level)
            if level_index is not None:
                save[f'{level}_level'] = level_index
            elif autofill_value is not None:
                save[f'{level}_level'] = autofill_value
        overwrite_save(save_path, save)
    elif action == 'reset':
        delete_save(save_path)
    elif action == 'read':
        read_save(save_path)
    elif not args.closegame:
        parser.print_help()

if __name__ == '__main__':
    main()
