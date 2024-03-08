# script_name: compress.py
import subprocess
import shutil
import os
from python.model.FileSystemNodeModel import File, Directory


def compress(file_node: object):
    """Compression based on type of file."""

    if os.path.isdir(file_node.path):
        output_path = _compress_directory_zip(file_node)
    else:
        output_path = _compress_single_file_gzip(file_node)
    return output_path


def _reduce_audio_quality(file_node: File, bitrate="128k"):
    """
    Compress an audio file using ffmpeg by reducing the audio bitrate.

    Parameters:
    - input_node: Input audio file.
    - target_bitrate: Target bitrate for the output file (default is 128k).
    """

    output_path = os.path.dirname(file_node.path) + '/archive_' + file_node.name
    command = [
        "ffmpeg",
        "-i", file_node.path,
        "-b:a", bitrate,  # reduced bitrate
        output_path
    ]
    subprocess.run(command)
    return output_path


def _reduce_video_quality(file_node: File, video_bitrate: str='1000k', audio_bitrate: str='128k'):
    """
    Compresses a video file using FFmpeg by reducing video and audio bitrates.

    Parameters:
    - input_node: Input video file.
    - video_bitrate: Desired video bitrate for compression.
    - audio_bitrate: Desired audio bitrate for compression.
    """

    output_path = os.path.dirname(file_node.path) + '/archive_' + file_node.name
    command = [
        'ffmpeg',
        '-i', file_node.path,
        '-b:v', video_bitrate,    # video bitrate
        '-c:a', 'aac',
        '-b:a', audio_bitrate,    # audio bitrate
        output_path
    ]
    subprocess.run(command)
    return output_path


def _compress_single_file_gzip(file_node: File):
    """
    Compresses a single file using gzip.

    Parameters:
    - input_path: Path to the input file to be compressed.
    """
    command = ['gzip', '-k', '-f', file_node.path]
    subprocess.run(command)
    return file_node.path + '.gz'


def _compress_directory_zip(dir_node: Directory):
    """
    Compresses an entire directory using tar with gzip compression.

    Parameters:
    - input_directory: Path to the directory to be compressed.
    - output_filename: Name of the output file (compressed archive).
    """
    output_filename = os.path.dirname(dir_node.path) + '/' + os.path.basename(dir_node.path)
    # Create a zip archive of the directory
    shutil.make_archive(output_filename, 'zip', dir_node.path)
    return output_filename + '.zip'


if __name__ == "__main__":
    pass