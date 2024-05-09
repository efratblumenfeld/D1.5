from PIL import Image
import os

def create_image_grid(folder_path):
    images = []  # List to store images

    # List image files in the folder and process the first 9 images named 'Map'
    files = [f for f in os.listdir(folder_path) if f.startswith('Map') and f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    files = sorted(files)[:9]  # Ensure only the first 9 are processed

    # Open the images and append to the list
    for file in files:
        img_path = os.path.join(folder_path, file)
        img = Image.open(img_path)
        images.append(img)

    # Assuming all images are the same size, create a grid
    if images:
        # Get dimensions
        img_width, img_height = images[0].size
        grid_width = 3 * img_width
        grid_height = 3 * img_height

        # Create a new blank image for the grid
        grid_image = Image.new('RGB', (grid_width, grid_height))

        # Paste images into the grid
        for index, image in enumerate(images):
            x_offset = (index % 3) * img_width
            y_offset = (index // 3) * img_height
            grid_image.paste(image, (x_offset, y_offset))

        # Save the new image under the name "MAPS.jpg" in the input folder
        grid_image.save(os.path.join(folder_path, 'MAPS.jpg'))
        print("Image grid created successfully at:", os.path.join(folder_path, 'MAPS.jpg'))
    else:
        print("No images found.")

# Input the folder path from the user
user_input_folder_path = input("Enter the path to the folder: ")

# Call the function with the user provided path
create_image_grid(user_input_folder_path)
