# pour lecture des images

import os
import cv2
import pytesseract
import regex

def ocr_images_in_folder(folder_path):
    ocr_results = []
    try:
        # Recursively iterate over all files and directories in the folder
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith((".jpg", ".jpeg")):
                    # Construct the full path to the image file
                    image_path = os.path.join(root, filename)

                    # Check if the parent directory is not named "thumbnail"
                    if "thumbnail" not in os.path.dirname(image_path).lower():
                        try:
                            # Read the image using OpenCV
                            image = cv2.imread(image_path)

                            # Perform OCR using pytesseract with Unicode output
                            data = pytesseract.image_to_string(image, lang='ben', config='--psm 6', output_type=pytesseract.Output.STRING)
                            print(f'OCR result for {image_path}: {data}')
                            # plus rapide
                            # with open('banglaGanashakti_output.txt', 'w', encoding='utf-8') as f:
                            #     f.write(data)

                            data = regex.sub(r'[^\p{Bengali}\s]+', '', data)
                            ocr_results.append((image_path, data))
                        except Exception as e:
                            print(f"Failed to OCR image {image_path}: {e}")
    except Exception as e:
        print(f"Error while processing folder {folder_path}: {e}")

    return ocr_results

def main():
    # Example usage
    images_folder = 'bangla_ganashakti'
    ocr_results = ocr_images_in_folder(images_folder)

    # Export OCR results to a text file
    with open('banglaGanashakti.txt', 'w', encoding='utf-8') as f:
        for image_path, text in ocr_results:
            f.write(f"Image Path: {image_path}\n")
            f.write(f"{text}\n\n")

if __name__ == "__main__":
    main()
