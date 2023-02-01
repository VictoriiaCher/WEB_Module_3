from pathlib import Path
import shutil
import re
import argparse
from threading import Thread

"""Скрипт виконує сортування у вказанній директорії, нормалізовує назви файлів та вкладених директорій
Після закінчення роботи виводить у консоль перелік файлів,
перелік відомих та невідомих розширень. Директорії оброблюються в режимі багатопотоковості """

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('-s', '--source', help='The path of source folder', required=True)
args = vars(parser.parse_args())
source = args.get('source')


names_dir = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [
        ".txt",
        ".docx",
        ".doc",
        ".pdf",
        ".rtf",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
    ],
    "Archives": [".tar", ".gz", ".7z", ".zip"],
    "Audio": [".mp3", "ogg", ".wav", ".amr"],
    "Video": [".avi", ".mov", ".mp4", ".mkv"],
    "Python": [".py", ".pyw"],
}

CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
FOLDERS = []
translate_map = {}
for key, value in zip(CYRILLIC, LATIN):
    translate_map[ord(key)] = value
    translate_map[ord(key.upper())] = value.upper()

list_files = []
ext = set()
unknow = set()


def normalise(file_stem: str) -> str:
    new_name = file_stem.translate(translate_map)
    new_name = re.sub(r"\W", "_", new_name)
    return new_name


def handle_imgs(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_docs(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_audio(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_video(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_py(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    unknow.add(filename.suffix)


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalise(
        filename.name.replace(filename.suffix, "")
    )

    folder_for_file.mkdir(exist_ok=True, parents=True)
    shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    list_files.append((normalise(filename.stem) + filename.suffix))
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
        print(f"Знайдено порожню директорію, яку буде видалено {folder}")
        return False
    except OSError:
        return True


def data_output(
):
    print(f"ПЕРЕЛІК ФАЙЛІВ:")
    for i in list_files:
        print(i)

    print(f"\nПЕРЕЛІК ВІДОМИХ РОЗШИРЕНЬ:")
    for i in ext:
        print(i)

    print(f"\nПЕРЕЛІК НЕВІДОМИХ РОЗШИРЕНЬ:")
    for i in unknow:
        print(i)


def scan(folder: Path):
    for file in folder.iterdir():
        if file.is_file():
            suf = file.suffix
            if suf in names_dir["Images"]:
                handle_imgs(file, folder / "Images")
            elif suf in names_dir["Documents"]:
                handle_docs(file, folder / "Documents")
            elif suf in names_dir["Audio"]:
                handle_audio(file, folder / "Audio")
            elif suf in names_dir["Video"]:
                handle_video(file, folder / "Video")
            elif suf in names_dir["Python"]:
                handle_py(file, folder / "Python")
            elif suf in names_dir["Archives"]:
                handle_archive(file, folder / "Archives")
            else:
                handle_other(file, folder / "Other")
        elif file.name not in (
                "Images",
                "Documents",
                "Audio",
                "Video",
                "Python",
                "Archives",
                "Other",
        ):
            if handle_folder(file):
                scan(file)


def list_folder(folder: Path):
    FOLDERS.append(folder)
    for el in folder.iterdir():
        if el.is_dir():
            el = el.replace(folder / normalise(el.name))
            FOLDERS.append(el)
            list_folder(el)


if __name__ == "__main__":
    base_folder = Path(source)  # r"C:\Users\hp\Desktop\sort"
    list_folder(base_folder)

    threads = []
    for folder in FOLDERS:
        print(f'Початок сортування у папці {folder}')
        th = Thread(target=scan, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print('Сортування завершено!')
    data_output()
