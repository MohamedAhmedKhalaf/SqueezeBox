from PIL import Image
import os

def compress_image(input_path: str, output_path: str, quality: int):
    try:
        original_size = os.path.getsize(input_path)

        with Image.open(input_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            img.save(output_path, "JPEG", quality=quality)

        compressed_size = os.path.getsize(output_path)

        compression_ratio = original_size / compressed_size

        print(f"Image successfully compressed and saved at: {output_path}")
        print(f"Original size: {original_size / 1024:.2f} KB")
        print(f"Compressed size: {compressed_size / 1024:.2f} KB")
        print(f"Compression ratio: {compression_ratio:.2f}")
    
    except Exception as e:
        print(f"Error compressing image: {e}")


if __name__ == "__main__":
    input_file = r"simple.jpg"
    output_file = "output_compressed.JPEG"
    compression_quality = 20  

    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' does not exist. Place your file in the same directory.")
    else:
        compress_image(input_file, output_file, compression_quality)
