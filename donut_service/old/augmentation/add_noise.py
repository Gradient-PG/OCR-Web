import os
import numpy as np
from PIL import Image
def add_noise(image, noise_level):
    """
    Function to add noise to an image.
    
    Arguments:
    image (Image): An Image object from the PIL library.
    noise_level (float): The noise level, determining the intensity of the noise.
                         The higher the value, the stronger the noise.
    
    Returns:
    Image: Modified Image object with added noise.
    """
    width, height = image.size
    # Generating a matrix of random values from the range [-noise_level, noise_level]
    noise = np.random.uniform(-noise_level, noise_level, (height, width, 3))
    # Converting the image to a numpy array
    image_array = np.array(image)
    # Adding noise to the image
    noisy_image = np.clip(image_array + noise, 0, 255).astype(np.uint8)
    # Converting back to an Image object
    noisy_image = Image.fromarray(noisy_image)
    return noisy_image
 
def add_gaussian_noise(image, mean=0, std=2):

    image_array = np.array(image)
    noise = np.random.normal(mean, std, image_array.shape).astype(np.uint8)
    noisy_image_array = np.clip(image_array + noise, 0, 255)

    return Image.fromarray(noisy_image_array)

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):

            img_path = os.path.join(input_folder, filename)
            image = Image.open(img_path)
            image = image.convert('RGB')
            noisy_image = add_noise(image,50)

            noisy_image.save(os.path.join(output_folder, filename))