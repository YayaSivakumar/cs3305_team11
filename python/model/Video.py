from python.model.FileSystemNodeModel import File
from python.model.FileSystemCache import FileSystemCache
import ffmpeg
import os
class Video(File):
    """A class representing a video file. Inherits from File."""
    def __init__(self, path, cache):
        super().__init__(path, cache)
        self._filetype = 'video'
        # Initialize additional attributes
        self.duration = None
        self.video_codec = None
        self.bitrate = None
        self.frame_rate = None
        self.audio_codec = None
        # Load video metadata
        self._load_metadata() # This will set the above attributes

    def _load_metadata(self):
        """Load metadata from the video file using ffmpeg-python."""
        try:
            # Correctly using ffmpeg.probe from ffmpeg-python
            probe = ffmpeg.probe(self.path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)

            if video_stream:
                self.duration = float(video_stream.get('duration', 0))
                self.video_codec = video_stream.get('codec_name', None)
                self.bitrate = int(video_stream.get('bit_rate', 0)) / 1000  # Convert to kbps
                self.frame_rate = eval(video_stream['avg_frame_rate'])  # Be cautious with eval()

            if audio_stream:
                self.audio_codec = audio_stream.get('codec_name', None)

        except ffmpeg._run.Error as e:  # Correctly catching exceptions from ffmpeg-python
            print(f"Error loading video metadata for {self.path}: {e}")

    def _show_video_data(self):
        """Print video metadata to the console."""
        for filename in os.listdir(directory_path):
            if filename.endswith(('.mp4') or ('.heic') or ('m4a')):  # Filter for MP4 files, adjust as needed
                video_path = os.path.join(directory_path, filename)
                video = Video(video_path, cache)
                print(f"Analyzing {filename}:")
                print(f"  Duration: {video.duration} seconds")
                print(f"  Video Codec: {video.video_codec}")
                print(f"  Bitrate: {video.bitrate} kbps")
                print(f"  Frame Rate: {video.frame_rate} fps")
                print(f"  Audio Codec: {video.audio_codec}")
                print(f"  Size: {video.size()}")

directory_path = '/Users/danielcagney/Desktop/'

cache = FileSystemCache()
video_file = Video(directory_path, cache)
video_file._show_video_data()

