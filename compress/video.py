'''Khalaf'''
from compress.ffmpeg_tools import compress_video

def compress_video_file(video_path, target_size, use_gpu, output_name):
     compressed_video, original_size, compressed_size, entropy = compress_video(video_path, target_size, use_gpu, output_name)
     return compressed_video, original_size, compressed_size, entropy