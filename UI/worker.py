import os
import shutil
import subprocess
from io import BytesIO
from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog, QFileDialog, QWidget, QMessageBox

from Class.exceptions import ExternalExecutableException, RandomizerExceptions
from Class.seedSettings import SeedSettings, ExtraConfigurationData
from Module import appconfig, platformutils
from Module.RandomizerSettings import RandomizerSettings
from Module.generate import generateSeed, generateMultiWorldSeed
from Module.zipper import BossEnemyOnlyZip, CosmeticsOnlyZip, SeedZipResult
from UI import qtlib
from UI.workers import BaseWorkerThread, BaseWorker


class GenerateModWorker(BaseWorker):

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent

    @staticmethod
    def run_custom_cosmetics_executables(extra_data: ExtraConfigurationData):
        for custom_executable in extra_data.custom_cosmetics_executables:
            custom_file_path = Path(custom_executable)
            if custom_file_path.is_file():
                custom_cwd = custom_file_path.parent
                if platformutils.is_windows():
                    subprocess.call([str(custom_file_path)], cwd=custom_cwd)
                elif custom_file_path.suffix.lower() == ".exe":
                    subprocess.call(
                        platformutils.windows_exe_command(custom_file_path, []), cwd=custom_cwd
                    )
                elif os.access(custom_file_path, os.X_OK):
                    subprocess.call([str(custom_file_path)], cwd=custom_cwd)
                elif custom_file_path.suffix.lower() == ".sh":
                    subprocess.call(["/bin/sh", str(custom_file_path)], cwd=custom_cwd)
                else:
                    raise ExternalExecutableException(
                        f"{custom_file_path.name} is not executable. Mark it executable"
                        " (chmod +x) or choose a .sh or .exe file."
                    )

    def download_mod(self, zip_data: BytesIO, output_file_name: str, title: str):
        last_save_path = appconfig.read_last_save_path()
        if last_save_path is not None:
            output_file_name = str(last_save_path / output_file_name)

        save_widget = QFileDialog()
        filter_name = f"{title} (*.zip)"
        save_widget.setNameFilters([filter_name])
        outfile_name, _ = save_widget.getSaveFileName(self.parent, f"Save {title}", output_file_name, filter_name)
        if outfile_name != "":
            if not outfile_name.endswith(".zip"):
                outfile_name += ".zip"
            with open(outfile_name, "wb") as out_zip:
                out_zip.write(zip_data.getbuffer())
            appconfig.write_last_save_path(str(Path(outfile_name).parent))

    @staticmethod
    def install_mod(zip_data: BytesIO, mod_name: str) -> bool:
        openkh_path = appconfig.read_openkh_path()
        if not openkh_path:
            return False

        kh2_mods_path = appconfig.kh2_mods_path(local=True)
        if not kh2_mods_path:
            return False

        mod_path = kh2_mods_path / mod_name
        if mod_path.is_dir():
            overwrite_reply = QMessageBox.question(
                None,
                "KH2 Seed Generator",
                f"{mod_name} mod already exists. Overwrite?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if overwrite_reply == QMessageBox.StandardButton.Yes:
                shutil.rmtree(mod_path)
            else:
                return False

        mod_path.mkdir(parents=True, exist_ok=True)

        with ZipFile(zip_data, "r") as zip_file:
            zip_file.extractall(mod_path)

        installed_message = f"Installed {mod_name} mod at\n{mod_path}"

        if platformutils.is_windows() or platformutils.wine_available():
            mods_manager_exe = openkh_path / "OpenKh.Tools.ModsManager.exe"
            if mods_manager_exe.is_file():
                open_reply = QMessageBox.question(
                    None,
                    "KH2 Seed Generator",
                    f"{installed_message}\n\nOpen Mods Manager?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if open_reply == QMessageBox.StandardButton.Yes:
                    command = platformutils.windows_exe_command(mods_manager_exe, args=[])
                    subprocess.call(command)
                return True

        # If we got here we don't know how to open Mods Manager from here
        qtlib.show_alert(installed_message)
        return True

    @staticmethod
    def display_emu_warnings(rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        if not extra_data.disable_emu_warning and rando_settings.keyblades_unlock_chests and extra_data.platform == "PCSX2":
            from UI import theme
            explainer_text = f'''You've generated a seed for PCSX2 with the setting for locking chests with keyblades. <br><br>
    This requires running the lua file included in the seed zip. This means, either move the lua file from the zip 
    (randoseed-mod-files/keyblade_locking/keyblade.lua) manually to your scripts folder, or reconfigure PCSX2 to use the folder made by the mod manager.<br><br>
    A tutorial to do so can be found here: <a href="LINK_HERE" style="color: {theme.LinkColor}">Tutorial</a><br><br>
    '''
            message = QMessageBox(text=explainer_text)
            message.setTextFormat(Qt.TextFormat.RichText)
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()


class GenerateSeedThread(BaseWorkerThread):

    def __init__(self, rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        super().__init__()
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def do_work(self) -> SeedZipResult:
        extra_data = self.extra_data
        seed_zip_result = generateSeed(self.rando_settings, extra_data)
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)
        return seed_zip_result


class GenerateSeedWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        super().__init__(parent)
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateSeedThread(self.rando_settings, self.extra_data)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog(
            label_text=f"Creating seed with name {self.rando_settings.random_seed}",
            title_text="Making your Seed, please wait...",
        )

    def handle_result(self, result: SeedZipResult):
        extra_data = self.extra_data
        zip_data, _, _ = result

        installed = False
        if extra_data.attempt_mod_install:
            installed = self.install_mod(zip_data, mod_name="randoseed")
        if not installed:
            self.download_mod(zip_data, output_file_name="randoseed.zip", title="Randomizer Seed")

        self.display_emu_warnings(self.rando_settings, extra_data)

    def handle_failure(self, failure: Exception):
        super().handle_failure(failure)
        if not isinstance(failure, RandomizerExceptions):
            raise failure


class GenerateMultiWorldSeedThread(BaseWorkerThread):

    def __init__(self, rando_settings: list[RandomizerSettings], extra_data: ExtraConfigurationData):
        super().__init__()
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def do_work(self) -> list[SeedZipResult]:
        extra_data = self.extra_data
        all_output = generateMultiWorldSeed(self.rando_settings, extra_data)
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)
        return all_output


class GenerateMultiWorldSeedWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, rando_settings: list[RandomizerSettings], extra_data: ExtraConfigurationData):
        super().__init__(parent)
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateMultiWorldSeedThread(self.rando_settings, self.extra_data)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog(
            label_text=f"Creating seed with name {self.rando_settings[0].random_seed}",
            title_text="Making your Seed, please wait...",
        )

    def handle_result(self, result: list[SeedZipResult]):
        for zip_data, _, _ in result:
            self.download_mod(zip_data, output_file_name="randoseed.zip", title="Randomizer Seed")

    def handle_failure(self, failure: Exception):
        super().handle_failure(failure)
        if not isinstance(failure, RandomizerExceptions):
            raise failure


class GenerateCosmeticsModThread(BaseWorkerThread):

    def __init__(self, ui_settings: SeedSettings, extra_data: ExtraConfigurationData):
        super().__init__()
        self.ui_settings = ui_settings
        self.extra_data = extra_data

    def do_work(self) -> BytesIO:
        extra_data = self.extra_data
        zipper = CosmeticsOnlyZip(self.ui_settings)
        zip_data = zipper.create_zip()
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)
        return zip_data


class CosmeticsModWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, ui_settings: SeedSettings, extra_data: ExtraConfigurationData):
        super().__init__(parent)
        self.ui_settings = ui_settings
        self.extra_data = extra_data

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateCosmeticsModThread(self.ui_settings, self.extra_data)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Creating cosmetics-only mod")

    def handle_result(self, result: BytesIO):
        installed = False
        if self.extra_data.attempt_mod_install:
            installed = self.install_mod(result, mod_name="randomized-cosmetics")
        if not installed:
            self.download_mod(result, output_file_name="randomized-cosmetics.zip", title="Cosmetics Mod")


class GenerateBossEnemyModThread(BaseWorkerThread):

    def __init__(self, seed_name: str, ui_settings: SeedSettings, platform: str):
        super().__init__()
        self.ui_settings = ui_settings
        self.platform = platform
        self.seed_name = seed_name

    def do_work(self) -> BytesIO:
        platform = self.platform
        zipper = BossEnemyOnlyZip(self.seed_name, self.ui_settings, platform)
        zip_data = zipper.create_zip()
        return zip_data


class BossEnemyModWorker(GenerateModWorker):

    def __init__(
            self,
            parent: QWidget,
            seed_name: str,
            ui_settings: SeedSettings,
            platform: str,
            attempt_mod_install: bool,
    ):
        super().__init__(parent)
        self.ui_settings = ui_settings
        self.platform = platform
        self.seed_name = seed_name
        self.attempt_mod_install = attempt_mod_install

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateBossEnemyModThread(self.seed_name, self.ui_settings, self.platform)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Creating boss/enemy-only mod")

    def handle_result(self, result: BytesIO):
        installed = False
        if self.attempt_mod_install:
            installed = self.install_mod(result, mod_name="randomized-bosses-enemies")
        if not installed:
            self.download_mod(result, output_file_name="randomized-bosses-enemies.zip", title="Boss/Enemy Mod")
