import os
import re

folder_path = 'images'

for filename in os.listdir(folder_path):
    match = re.match(r'([A-Za-z]+) \((\d+)\)\.jpg', filename)
    
    if match:
        new_filename = f"{match.group(1)}_{match.group(2)}.jpg"
        
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        
        os.rename(old_file, new_file)
        print(f"Changed: {filename} -> {new_filename}")