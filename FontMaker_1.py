import fontforge
import subprocess
import os


BASE_DIR = "FontMaker.nosync/FontMaker"
DIRTY_SVGs = os.path.join(BASE_DIR, "SVGs")
CLEAN_SVGs = os.path.join(BASE_DIR, "SVGs_cleaned")


def main():
    # clean_SVGs(DIRTY_SVGs, CLEAN_SVGs)
    font = fontforge.font()

    for SVG_path in os.listdir(CLEAN_SVGs):
        name = SVG_path.split(".")[0]
        char = font.createChar(-1, name)
        char.importOutlines(os.path.join(CLEAN_SVGs, SVG_path))
    
    font.generate(os.path.join(BASE_DIR, "output.ttf"))


def clean_SVGs(input_dir, output_dir):
    if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
    
    for svg in os.listdir(input_dir):

        input_path = os.path.join(input_dir, svg)
        
        output_path = os.path.join(output_dir, svg)

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

        subprocess.run(command)



if __name__ == "__main__":
    main()