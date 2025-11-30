import os
import shutil
from pathlib import Path

PHOTO_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic'}
VIDEO_EXT = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.m4v'}

def safe_move(src_path: Path, dest_dir: Path):
    """Move a file safely. If a file exists, rename it with a counter."""
    dest_path = dest_dir / src_path.name
    counter = 1
    
    while dest_path.exists():
        dest_path = dest_dir / f"{src_path.stem}_{counter}{src_path.suffix}"
        counter += 1
    
    shutil.move(str(src_path), str(dest_path))


def organize_media(directory):
    directory = Path(directory)

    photos_dir = directory / 'Photos'
    videos_dir = directory / 'Videos'
    others_dir = directory / 'Others'

    # Create required folders
    photos_dir.mkdir(exist_ok=True)
    videos_dir.mkdir(exist_ok=True)
    others_dir.mkdir(exist_ok=True)

    photos_moved = 0
    videos_moved = 0
    others_moved = 0

    print("\nOrganizing... Please wait...\n")

    # Walk through all subdirectories
    for root, _, files in os.walk(directory):

        root = Path(root)

        # Skip destination folders
        if root in {photos_dir, videos_dir, others_dir}:
            continue

        for file in files:
            src = root / file
            ext = src.suffix.lower()

            try:
                if ext in PHOTO_EXT:
                    safe_move(src, photos_dir)
                    photos_moved += 1
                elif ext in VIDEO_EXT:
                    safe_move(src, videos_dir)
                    videos_moved += 1
                else:
                    safe_move(src, others_dir)
                    others_moved += 1
            except Exception as e:
                print(f"Error moving {src.name}: {e}")

    print("✔ Organization complete!\n")
    print(f"🖼  Photos moved: {photos_moved}")
    print(f"🎥  Videos moved: {videos_moved}")
    print(f"📦  Other files moved: {others_moved}")


if __name__ == "__main__":
    print("📁 Media Organizer Tool")
    directory = input("Enter the directory path to organize: ")

    if os.path.isdir(directory):
        organize_media(directory)
    else:
        print("❌ Error: The specified directory does not exist.")
