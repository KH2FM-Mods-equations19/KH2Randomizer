import json
from pathlib import Path
from typing import Optional

import yaml

from Module import platformutils

AUTOSAVE_FOLDER = "auto-save"
PRESET_FOLDER = "presets"

OUTPUT_PREFERENCE_MODS_MANAGER = "mm"
OUTPUT_PREFERENCE_FILE = "file"


def settings_presets_folder() -> Path:
    return Path(PRESET_FOLDER).absolute()


def read_app_config() -> dict:
    config_path = Path('randomizer-config.json').absolute()
    if config_path.is_file():
        with open(config_path, encoding='utf-8') as config_file:
            return json.load(config_file)
    else:
        return {}


def read_boss_enemy_override_files() -> str:
    result_string = ""
    location_override_path = Path('override_enemies.yaml').absolute()
    if location_override_path.is_file():
        with open(location_override_path, encoding='utf-8') as location_override:
            result_string += location_override.read()
    enemy_override_path = Path('override_enemies.yaml').absolute()
    if enemy_override_path.is_file():
        with open(enemy_override_path, encoding='utf-8') as enemy_override:
            result_string += enemy_override.read()
    return result_string


def write_app_config(config: dict):
    config_path = Path('randomizer-config.json').absolute()
    with open(config_path, mode='w', encoding='utf-8') as config_file:
        json.dump(config, config_file, indent=4)


def update_app_config(key: str, value):
    randomizer_config = read_app_config()
    randomizer_config[key] = value
    write_app_config(randomizer_config)


def remove_app_config(key: str):
    randomizer_config = read_app_config()
    if key in randomizer_config:
        del randomizer_config[key]
        write_app_config(randomizer_config)


def _read_directory(key: str) -> Optional[Path]:
    randomizer_config = read_app_config()
    value = randomizer_config.get(key, "to-nowhere")
    if value is None:
        return None

    candidate = platformutils.path_from_config_value(value)
    if candidate.is_dir():
        return candidate
    else:
        return None


def read_last_save_path() -> Optional[Path]:
    return _read_directory("last_save_folder")


def write_last_save_path(selected_directory):
    update_app_config("last_save_folder", selected_directory)


def read_openkh_path() -> Optional[Path]:
    return _read_directory("openkh_folder")


def write_openkh_path(selected_directory):
    update_app_config('openkh_folder', selected_directory)


def is_openkh_folder(selected_path: Path) -> bool:
    mods_manager_names = [
        "OpenKh.Tools.ModManager.exe",        # Avalonia Mods Manager
        "OpenKh.Tools.ModsManager.exe",       # Legacy Mods Manager
        "OpenKh.Tools.ModManager",            # Avalonia Mods Manager (Linux)
        "OpenKh.Tools.ModsManager",           # Possibly an older Linux prototype?
        "OpenKh.Tools.ModsManager.Avalonia",  # Possibly the Linux one that never got merged
    ]
    tool_directories = [selected_path, selected_path / "Apps"]
    return any(
        (tool_directory / name).is_file()
        for tool_directory in tool_directories
        for name in mods_manager_names
    )


def read_custom_music_path() -> Optional[Path]:
    return _read_directory("custom_music_folder")


def write_custom_music_path(selected_directory):
    update_app_config('custom_music_folder', selected_directory)


def read_custom_visuals_path() -> Optional[Path]:
    return _read_directory("custom_visuals_folder")


def write_custom_visuals_path(selected_directory):
    update_app_config('custom_visuals_folder', selected_directory)


def read_output_preference() -> str | None:
    return read_app_config().get("outputPreference")


def write_output_preference(preference: str):
    update_app_config("outputPreference", preference)


def extracted_data_path() -> Optional[Path]:
    return _read_mods_manager_config_dir([
        "DataPath",               # Avalonia Mods Manager, inside the `Frontend` grouping
        "extractedGameDataPath",  # The unfortunately-timed rename
        "gameDataPath",           # The original name
    ])


def extracted_game_path(game: str) -> Optional[Path]:
    """Returns the path to extracted game data for the specified game, or None if not found."""
    base_extracted_path = extracted_data_path()
    if base_extracted_path is None:
        return None

    game_path = base_extracted_path / game
    if game_path.is_dir():
        return game_path
    else:
        return None


def kh2_mods_path(local: bool=False) -> Path | None:
    """
    Returns the path to KH2 mods, or None if not found.

    local controls whether the result should attempt to be the path for local mods (newer Mods Manager separates them)
    """
    openkh_path = read_openkh_path()
    if openkh_path is None:
        return None

    mods_path = _read_mods_manager_config_dir([
        "ModPath",            # Avalonia Mods Manager, inside the `Frontend` grouping
        "installedModsPath",  # The unfortunately-timed rename
        # Not sure what the original was meant to be, but we only started supporting custom once the rename happened
    ])
    if not mods_path:
        mods_path = openkh_path / "mods"

    kh2_path = mods_path / "kh2"
    if not kh2_path.is_dir():
        return None

    if local:
        # File that indicates it's the newer Avalonia Mods Manager
        # TODO: Might be better to just detect which version up front rather than checking files just-in-time?
        memory_file_path = kh2_path / "mod_memory.yml"
        if memory_file_path.is_file():
            local_path = kh2_path / "local"
            local_path.mkdir(parents=True, exist_ok=True)
            return local_path
        else:
            return kh2_path

    return kh2_path


def goa_mod_path() -> Path | None:
    """Returns the path to the Garden of Assemblage mod, or None if not found."""
    game_mods_path = kh2_mods_path(local=False)
    if not game_mods_path:
        return None

    # Best effort here to try to find GoA ROM mod. If this doesn't seem good enough, could change to a folder chooser.
    for top_mod_dir in game_mods_path.iterdir():
        if not top_mod_dir.is_dir():
            continue

        if top_mod_dir.name.startswith("GoA-ROM-Edition"):
            return top_mod_dir

        for second_dir in top_mod_dir.iterdir():
            if second_dir.is_dir() and second_dir.name.startswith("GoA-ROM-Edition"):
                return second_dir

    return None


def _read_mods_manager_config_dir(keys: list[str]) -> Path | None:
    """Returns a path configured in the Mods Manager config file at one of the provided keys, or None if not found."""
    openkh_path = read_openkh_path()
    if openkh_path is None:
        return None

    def read_from_file(file_path: Path, prefix: str | None = None) -> Path | None:
        if file_path.is_file():
            with open(file_path, encoding="utf-8") as opened_file:
                config_yaml = yaml.safe_load(opened_file)

                if prefix is not None:
                    config_yaml = config_yaml.get(prefix, {})

                for key in keys:
                    value = config_yaml.get(key, "")
                    if value:
                        directory = platformutils.path_from_config_value(value)
                        if directory.is_dir():
                            return directory

        return None

    # Making an assumption here that any of the config dirs are under the "Frontend" prefix.
    # Obviously subject to change, but we'd need to change our code regardless if it does.
    result = read_from_file(openkh_path / "config.yml", prefix="Frontend")
    if result is not None:
        return result

    return read_from_file(openkh_path / "mods-manager.yml")
