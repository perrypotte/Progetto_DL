import os
import shutil
import random

def split_images(images_dir, synth_dir, real_dir, test_dir, test_ratio=0.2):
    # Creazione delle directory di output se non esistono
    os.makedirs(synth_dir, exist_ok=True)
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Lista di tutte le immagini
    images = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    synth_images = []
    real_images = []

    # Separare le immagini sintetiche da quelle reali
    for img in images:
        if img.startswith("camera"):
            synth_images.append(img)
        else:
            real_images.append(img)

    # Mescolare le immagini reali per una divisione casuale
    random.shuffle(real_images)

    # Suddividere il 20% delle immagini reali in test
    test_count = int(len(real_images) * test_ratio)
    test_images = real_images[:test_count]
    train_images = real_images[test_count:]

    # Funzione per copiare le immagini in una directory
    def copy_images(image_list, dest_dir):
        for img in image_list:
            shutil.copy2(os.path.join(images_dir, img), os.path.join(dest_dir, img))

    # Copia delle immagini nelle rispettive directory
    copy_images(synth_images, synth_dir)
    copy_images(train_images, real_dir)
    copy_images(test_images, test_dir)

    print(f"Copiati {len(synth_images)} immagini in synth")
    print(f"Copiati {len(train_images)} immagini in real")
    print(f"Copiati {len(test_images)} immagini in test")

# Imposta i percorsi
images_directory = "images"  # Directory con tutte le immagini
synth_directory = "synth"  # Directory per immagini sintetiche
real_directory = "real"  # Directory per immagini reali
test_directory = "test"  # Directory per il test

# Esegui lo script
split_images(images_directory, synth_directory, real_directory, test_directory)
