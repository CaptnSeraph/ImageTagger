# Image Tagger

Image Tagger is a simple tool designed to help you tag your images quickly and efficiently. It provides a convenient graphical user interface for loading images, viewing thumbnails, and tagging selected images

## Features

    - Load images from a directory of your choice
    - View thumbnails of all loaded images
    - Adjust the size of the thumbnails with a convenient slider
    - Select images to tag by checking the box next to the thumbnail
    - Enter your tag in a text box and apply it to all selected images with a single click
## Requirements

    This application requires Python 3.6 or higher, and the following Python libraries:

    - Pillow
    - PyQt5

    You can install these libraries using pip:

    ```
    pip install -r requirements.txt
    ```

## Usage

    1. Run the script:

    ```
    python imagetagger.py
    ```

    2. Click on the "Load Images" button and select a directory. All images in the directory will be loaded and their thumbnails will be displayed.

    3. Select the images you want to tag by clicking on them

    4. Enter a tag in the text entry field and click on the "Tag Images" button. The tag will be applied to all selected images and appended to a self named .txt in the same directory

    5. The selected images will be deselected and you can start the process again from step 3.

## License

  This project is licensed under the MIT License.
