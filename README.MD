    # Image Tagger

    Image Tagger is a simple Python application that allows you to easily apply tags to multiple images at once.

    ## Features

    - Load an entire directory of images
    - View thumbnails of all loaded images
    - Select multiple images using checkboxes
    - Apply a tag to all selected images at once
    - Automatically generates and updates a .txt file for each image that stores its tags

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

    3. Select the images you want to tag by checking their checkboxes.

    4. Enter a tag in the text entry field and click on the "Tag Images" button. The tag will be applied to all selected images.

    5. The selected images will be deselected and you can start the process again from step 3.

    ## License

    This project is licensed under the MIT License.
