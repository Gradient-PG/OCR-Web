import os
import sys
import json
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import re

# Ścieżka do wytrenowanego modelu
model_path = "with_aug_1"

# Załaduj model i processor
model = VisionEncoderDecoderModel.from_pretrained(model_path)
processor = DonutProcessor.from_pretrained(model_path)

# Ustaw model na GPU, jeśli dostępne
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Używasz " + device)
model.to(device)

def sort_key(filename):
    match = re.match(r"([A-ZŻŹĆŚŃŁÓ]) \((\d+)\)", filename)
    if match:
        letter = match.group(1)
        number = int(match.group(2))
        return (letter, number)

def analyze_image(image_path):
    """Analizuje obraz i zwraca wygenerowany tekst"""
    try:
        image = Image.open(image_path).convert("RGB")

        # Przetwórz obraz na tensor, używając procesora Donut
        pixel_values = processor(image, return_tensors="pt").pixel_values

        # Przenieś na GPU, jeśli używasz
        pixel_values = pixel_values.to(device)

        # Przygotowanie dekodera
        decoder_input_ids = torch.full(
            (1, 1), model.config.decoder_start_token_id, device=device
        )

        # Wygenerowanie predykcji (ciągu znaków)
        outputs = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=768,  # zgodne z konfiguracją Twojego modelu
            # early_stopping=True,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
        )

        # Zdekodowanie wyniku
        predicted_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        return predicted_text

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main(folder_path, output_json_path):
    results = {}

    # Przechodzimy przez wszystkie pliki w folderze
    listdir = os.listdir(folder_path)
    listdir = sorted(listdir, key=sort_key)
    for filename in listdir:
        file_path = os.path.join(folder_path, filename)

        # Sprawdzamy, czy to obraz (można dodać więcej rozszerzeń w zależności od potrzeb)
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing {filename}...")
            text = analyze_image(file_path)

            if text:
                results[filename] = text

    # Zapisujemy wyniki do pliku JSON
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Wyniki zapisane do {output_json_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie: py my_script.py folder_ze_zdjęciami nazwa_pliku_wyjściowego.json")
        sys.exit(1)

    folder_ze_zdjęciami = sys.argv[1]
    nazwa_pliku = sys.argv[2]

    main(folder_ze_zdjęciami, nazwa_pliku)