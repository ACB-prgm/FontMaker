import concurrent.futures as cfut
from pathlib import Path
import subprocess
import fontforge
import pickle
import scour # only here to remind you to pip install scour.  This is run from the command line via subprocess
import os


LOWERS = "abcdefghijklmnopqrstuvwxyz"
UPPERS = LOWERS.upper() + "1234567890"
FONT_NAME = "Cartoon Roman"
BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = os.path.join(BASE_DIR, "CLEAN_LOG.pickle")
DIRTY_SVGs = os.path.join(BASE_DIR, "SVGs")
CLEAN_SVGs = os.path.join(BASE_DIR, "SVGs_cleaned")


def main():
    clean_SVGs(DIRTY_SVGs, CLEAN_SVGs)

    font = fontforge.font()
    font.familyname = FONT_NAME

    I = font.createChar(-1, "I").importOutlines(os.path.join(CLEAN_SVGs, "I.svg"))
    I_width = get_glyph_width(I)
    space = font.createChar(-1, "space")
    space.width = round(I_width * 3)

    for SVG_path in os.listdir(CLEAN_SVGs):
        if "DS_Store" in SVG_path:
            continue

        name = SVG_path.split(".")[0].replace("-", "")
        char = font.createChar(-1, name)
        char.importOutlines(os.path.join(CLEAN_SVGs, SVG_path))
        # char.genericGlyphChange(stemScale=1.0, vCounterType="scaled", vCounterScale=1.0, hCounterType="center")

        kern = I_width/4

        char.left_side_bearing = round(kern)
        char.width = round(kern * 2 + get_glyph_width(char))
        if name in ["T", "F"]:
            char.width = 400
    
    font.generate(os.path.join(BASE_DIR, "{}.ttf".format(FONT_NAME.replace(" ", "_"))))
    font.close()


def get_glyph_width(char):
    box = char.boundingBox()
    return box[2] - box[0]


def clean_SVGs(input_dir, output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    
    commands = []
    if os.listdir(input_dir) == os.listdir(output_dir):
        log = get_log()
    else:
        log = {}

    for svg_file in os.listdir(input_dir):
        input_path = os.path.join(input_dir, svg_file)
        output_path = os.path.join(output_dir, svg_file)

        mtime = os.path.getmtime(input_path)
        if input_path in log and log.get(input_path) == mtime:
            continue
        else:
            log[input_path] = mtime

        command = [
            "scour"
            ,"-i"
            ,input_path
            ,"-o"
            ,output_path
            ,"--enable-viewboxing"
            ,"--enable-id-stripping"
            ,"--enable-comment-stripping"
            ,"--shorten-ids"
            ,"--indent=none"
        ]

        commands.append(command)
    
    save_log(log)

    with cfut.ThreadPoolExecutor() as executor:
        executor.map(subprocess.run, commands)


def get_log():
    if os.path.exists(LOG_PATH): # Load log
        with open(LOG_PATH, 'rb') as file:
            log = pickle.load(file)
            return log

    return {}


def save_log(log: dict):
    with open(LOG_PATH, 'wb') as file:
        pickle.dump(log, file)


if __name__ == "__main__":
    main()