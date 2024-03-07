import os
import shutil
from python.model.FileSystemNodeModel import FileSystemNode


def analyze_storage(self):
    """Analyzes storage usage starting from the given path."""
    largest_files = []
    largest_dirs = []

    for dirpath, dirnames, filenames in os.walk(self.path):
        dir_size = self.get_size()
        largest_dirs.append((dirpath, dir_size))
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp) and not os.path.islink(fp):
                file_size = os.path.getsize(fp)
                largest_files.append((fp, file_size))

    # Sort and get top 10 largest directories and files
    largest_dirs.sort(key=lambda x: x[1], reverse=True)
    largest_files.sort(key=lambda x: x[1], reverse=True)

    print("Top 10 largest directories:")
    for d in largest_dirs[:10]:
        print(f"{d[0]} - {d[1] / (1024 * 1024):.2f} MB")

    print("\nTop 10 largest files:")
    for f in largest_files[:10]:
        print(f"{f[0]} - {f[1] / (1024 * 1024):.2f} MB")
