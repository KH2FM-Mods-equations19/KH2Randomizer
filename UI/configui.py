import textwrap
from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from Module import appconfig
from Module.cosmetics import CosmeticsMod
from UI.qtlib import show_alert


CUSTOM_MUSIC_NOT_CHOSEN = "Custom Music Folder has not been chosen."
CUSTOM_VISUALS_NOT_CHOSEN = "Custom Visuals Folder has not been chosen."
OPENKH_LOCATION_NOT_CHOSEN = "OpenKH installation location has not been chosen."


def openkh_folder_getter() -> bool:
    save_file_widget = QFileDialog()
    selected_directory = save_file_widget.getExistingDirectory(caption="Select OpenKH Folder")

    if selected_directory is None or selected_directory == "":
        return False

    selected_path = Path(selected_directory)
    if not appconfig.is_openkh_folder(selected_path):
        show_alert("Not a valid OpenKH folder.")
        return False

    appconfig.write_openkh_path(selected_directory)
    return True


def custom_music_folder_getter() -> bool:
    save_file_widget = QFileDialog()
    selected_directory = save_file_widget.getExistingDirectory(caption="Select Custom Music Folder")

    if selected_directory is None or selected_directory == "":
        return False

    CosmeticsMod.bootstrap_custom_music_folder(Path(selected_directory))
    appconfig.write_custom_music_path(selected_directory)
    return True


def custom_visuals_folder_getter() -> bool:
    save_file_widget = QFileDialog()
    selected_directory = save_file_widget.getExistingDirectory(caption="Select Custom Visuals Folder")

    if selected_directory is None or selected_directory == "":
        return False

    CosmeticsMod.bootstrap_custom_visuals_folder(Path(selected_directory))
    appconfig.write_custom_visuals_path(selected_directory)
    return True


def should_attempt_mod_install(parent: QWidget | None, force_prompt: bool) -> bool:
    output_preference = appconfig.read_output_preference()
    if not output_preference or force_prompt:
        message = textwrap.dedent("""
        Generated seeds and mods can be installed directly into OpenKH Mods Manager.

        When enabled, this skips the creation of seed/mod zip files altogether.

        - Updated versions of the common trackers can be configured to load seeds directly from Mods Manager.

        - The spoiler log (if any) can be found inside of the seed mod's folder.

        - If in doubt, choose No.

        - If you change your mind, use the Configure Seed Output option in the Configure menu to be asked again.
        
        
        
        Enable direct Mods Manager installation?
        """).strip()
        reply = QMessageBox.question(
            parent,
            "KH2 Seed Generator",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            appconfig.write_output_preference(appconfig.OUTPUT_PREFERENCE_MODS_MANAGER)
        elif reply == QMessageBox.StandardButton.No:
            appconfig.write_output_preference(appconfig.OUTPUT_PREFERENCE_FILE)
            return False
        else:
            return False
    elif output_preference == appconfig.OUTPUT_PREFERENCE_MODS_MANAGER:
        pass  # Fall through to below
    else:
        return False

    kh2_mods_path = appconfig.kh2_mods_path(local=False)
    if not kh2_mods_path:
        show_alert(OPENKH_LOCATION_NOT_CHOSEN)
        openkh_folder_getter()

    return appconfig.kh2_mods_path(local=False) is not None
