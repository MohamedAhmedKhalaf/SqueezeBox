'''                                                                                      
                                                       KHALAF

    DON'T TOUCH THIS 
    VIDEO COMPRESSION 
    NEED TO BE FIXED 

'''

import ffmpeg
import os
from pathlib import Path
import math
import numpy as np
import tempfile
import subprocess

def probe_video(video_path):
  try:
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return video_stream
  except ffmpeg.Error as e:
    print(f"FFmpeg probe error: {e.stderr.decode('utf8')}")
    return None

def create_temp_dir():
  temp_dir = Path(Path.cwd() / "static/uploads/tmp")
  temp_dir.mkdir(exist_ok=True)
  return temp_dir

def calculate_entropy(data):
  if not data:
      return 0
  probabilities = [data.count(c) / len(data) for c in set(data)]
  entropy = -sum([p * math.log2(p) for p in probabilities])
  return entropy
def get_file_size_in_mb(file_path):
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    return file_size_mb

def compress_video(video_path, target_size, use_gpu, output_name): 
    temp_dir = create_temp_dir()
    output_path = os.path.join(temp_dir, output_name + ".mp4") 
    try:
        video_stream = probe_video(video_path)
        if not video_stream:
             return None, None, None, None
        input_file_size = get_file_size_in_mb(video_path)
        ffmpeg_path = "ffmpeg"
        command = [
            ffmpeg_path,
             "-y",
            "-i",
            video_path,
            output_path,
            "-vf",
            f"scale=-2:{int(1080 * (float(target_size)/input_file_size))}",
             "-c:v",
             "libx264",
            "-c:a",
            "aac",
            "-movflags",
            "frag_keyframe+empty_moov",
             "-preset",
            "fast",
        ]
        if use_gpu == "True":
          command.insert(5, "-hwaccel")
          command.insert(6, "cuda")

        try:
          process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding="utf-8",
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

          out, err = process.communicate()
          if process.returncode != 0:
               print(f"Error compressing {video_path}: {err}")
               return None, None, None, None
        except Exception as e:
            print(f"Error during subprocess call {e}")
            return None, None, None, None

        compressed_file_size = get_file_size_in_mb(output_path)
        with open(output_path, 'rb') as f:
            compressed_video = f.read()
        compressed_video_entropy = calculate_entropy(compressed_video)

        os.remove(output_path)
        return compressed_video, input_file_size, compressed_file_size, compressed_video_entropy
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode('utf8')}")
        return None, None, None, None
    except Exception as e:
        print(f"Error during compression: {e}")
        return None, None, None, None