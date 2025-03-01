
import json
import os
import re
from PIL import Image
import copy

class DataAugmentation:


    path_to_save_labels = 'labels/augmented'

    path_to_raw_labels = 'labels/raw_proper/'

    def __init__(self):
        # override this name for new DataAugmentation
        self.name = "original"

    def augment(self):
        print("Start augmentation for " + self.name)
        for char_folder in os.scandir(self.path_to_raw_labels):

            for file in os.scandir(self.path_to_raw_labels + "/" + char_folder.name):
                if file.name == ".init":
                    continue

                list_of_img_name = self.load_images_from_jsons(self.path_to_raw_labels + char_folder.name + '/'+ file.name)
                
                for img_name in list_of_img_name:
                    #Krzychu, mamy inny format danych
                    letter = img_name.split('_')[0]
                    temp = img_name.split('_')[1]
                    number = temp.split('.')[0]
                    img_name = f'{letter} ({number}).jpg'
                    print(img_name)
                    # try:
                    with Image.open('images/' + img_name) as img:
                        img = img.convert('RGB')
                        img = self.aug_image(img)
                        self.save_image(img, img_name)
                    # except:
                    #     print("Error: Cannot to save " + img_name)
                
                self.aug_json(self.path_to_raw_labels + char_folder.name + '/'+ file.name, file.name)
        print("End augmentation for " + self.name)

    def load_images_from_jsons(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        images = []
        for image in data:
            images.append(image["data"]["ocr"])
        pattern = r"[A-Za-z]+_\d+\.jpg"
        for i in range(len(images)):
            match = re.search(pattern, images[i])
            if match:
                images[i] = match.group()
            else:
                print("ERROR: strings does not match")
        return images

    def save_image(self, image, img_name):
        image.save('images/aug/'+ self.name + '_'+img_name)

    # override this method
    def aug_image(self, image):
        return image

    def aug_json(self, path, name_of_file):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        data_cp = copy.deepcopy(data)
        pattern = r"[A-Za-z]+_\d+\.jpg"
        for image in data_cp:
            ocr_text = image["data"]["ocr"]
            match = re.search(pattern, ocr_text)
            if match:
                image["data"]["ocr"] = self.name + '_' + match.group()
            else:
                print(f"ERROR: string '{ocr_text}' does not match the pattern")
                
        with open(self.path_to_save_labels + '/' + self.name + '_' + name_of_file, 'w', encoding='utf-8') as file:
            json.dump(data_cp, file, indent=4, ensure_ascii=False)