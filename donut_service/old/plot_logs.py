import matplotlib.pyplot as plt
import pandas as pd



data = pd.read_csv('OCR-PCK-labels/scripts/logs/OCR-PCK/version_5(no_augmentation)/metrics.csv')
filtered_data = data.dropna(subset=['val_edit_distance'])


plt.figure(figsize=(10, 6))
plt.plot(filtered_data['epoch'], filtered_data['val_edit_distance'], marker='o', linestyle='-', color='b', label='Val Edit Distance')


plt.title('Validation Edit Distance over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Val Edit Distance')
#plt.grid(True)
plt.legend()


#plt.tight_layout()
plt.savefig('OCR-PCK-labels/scripts/logs/OCR-PCK/version_5(no_augmentation)/val_ed_plot.png')
plt.show()
