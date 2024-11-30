import base64
from app.core.db import get_db


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_images(files):
    all_success = True
    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            return {"error": "Invalid file type or no file selected"}, 415

        image_code = file.filename

        try:
            response, status_code = load_image_to_db(file, image_code)
            if status_code != 200:
                all_success = False
        except Exception as e:
            print(f"Exception occurred for {file.filename}: {e}")
            all_success = False


    if all_success:
        return {"message": "All items loaded successfully."}, 200
    else:
        return {"message": "Some items failed to load."}, 400

def load_image_to_db(file, image_code):
    db = get_db()
    collection = db['images']

    try:
        file_content = file.read()
        photo_data = base64.b64encode(file_content).decode('utf-8')

        existing_image = list(collection.find({"_id": image_code}))

        if existing_image:
            collection.update_one({"_id": image_code}, {"$set": {"photo": photo_data}})
            return {"message": "Photo successfully updated"}, 200
        else:
            collection.insert_one({"_id": image_code, "photo": photo_data})
            return {"message": "Photo successfully uploaded and linked to the card"}, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_image(image_code):
    db = get_db()
    collection = db['images']

    image_data = list(collection.find({"_id": image_code}))
    return image_data