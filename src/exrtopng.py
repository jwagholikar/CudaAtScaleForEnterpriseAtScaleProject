import OpenEXR
import Imath
from PIL import Image
import numpy as np

def convert_exr_to_png(exr_path, png_path, gray_png_path):
    """
    Converts an OpenEXR image to a PNG image.
    Handles the conversion from float (EXR) to 16-bit or 8-bit (PNG).
    """
    try:
        # Open the EXR file
        exr_file = OpenEXR.InputFile(exr_path)
        dw = exr_file.header()['dataWindow']
        size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        # Read channels (R, G, B) as floats
        red_channel = np.frombuffer(exr_file.channel('R', Imath.PixelType(Imath.PixelType.FLOAT)), dtype=np.float32)
        green_channel = np.frombuffer(exr_file.channel('G', Imath.PixelType(Imath.PixelType.FLOAT)), dtype=np.float32)
        blue_channel = np.frombuffer(exr_file.channel('B', Imath.PixelType(Imath.PixelType.FLOAT)), dtype=np.float32)

        # Reshape to image dimensions
        red_channel = red_channel.reshape(size[1], size[0])
        green_channel = green_channel.reshape(size[1], size[0])
        blue_channel = blue_channel.reshape(size[1], size[0])

        # Stack channels to create an RGB image
        rgb_image_float = np.stack([red_channel, green_channel, blue_channel], axis=-1)

        # Tone mapping/normalization for display (optional, depending on desired output)
        # For simplicity, a basic scaling to 0-1 range and then to 0-255 for 8-bit PNG
        # Or to 0-65535 for 16-bit PNG
        rgb_image_normalized = np.clip(rgb_image_float, 0, 1) # Clip values to 0-1 range

        # Convert to 16-bit unsigned integer (for 16-bit PNG)
        rgb_image_uint16 = (rgb_image_normalized * 65535).astype(np.uint16)

        # Create PIL Image from NumPy array
        pil_image = Image.fromarray(rgb_image_uint16, mode='RGB')

        # Save as PNG
        pil_image.save(png_path)
        print(f"Successfully converted '{exr_path}' to '{png_path}'")

        img = Image.open(png_path)

        gray_img = img.convert("L")

        gray_img.save(gray_png_path)

    except Exception as e:
        print(f"Error converting EXR to PNG: {e}")

# Example usage:
convert_exr_to_png("../data/1.5.01_harrisFilter.exr", "../data/1.5.01_harrisFilter.png", "../data/gray_1.5.01_harrisFilter.png")
convert_exr_to_png("../data/Lena_harrisFilter.exr", "../data/Lena_harrisFilter.png", "../data/gray_Lena_harrisFilter.png")