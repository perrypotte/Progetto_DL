import os
import shutil
import random

def create_yolo_dataset(test_path, test_labels_path, synth_path, real_path, synth_labels_path, real_labels_path, output_path, real_percentage, train_split):
    # Creazione della struttura delle cartelle
    for subset in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_path, subset, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_path, subset, 'labels'), exist_ok=True)

    # Recupera tutte le immagini sintetiche e reali
    synth_images = [f for f in os.listdir(synth_path) if f.endswith(('.jpg', '.png'))]
    real_images = [f for f in os.listdir(real_path) if f.endswith(('.jpg', '.png'))]

    # Seleziona una percentuale delle immagini reali
    num_real = int(len(real_images) * real_percentage)
    real_images = random.sample(real_images, num_real)

    # Combina immagini sintetiche e reali
    all_images = synth_images + real_images
    random.shuffle(all_images)  # Mischia i dati

    # Suddivisione in train/val
    num_train = int(len(all_images) * train_split)
    train_images = all_images[:num_train]
    val_images = all_images[num_train:]

    def move_files(images, subset):
        """Copia immagini e etichette nelle rispettive cartelle."""
        for img in images:
            src_img = os.path.join(synth_path if img in synth_images else real_path, img)
            src_label = os.path.join(synth_labels_path if img in synth_images else real_labels_path, img.replace('.jpg', '.txt').replace('.png', '.txt'))

            dst_img = os.path.join(output_path, subset, 'images', img)
            dst_label = os.path.join(output_path, subset, 'labels', os.path.basename(src_label))

            shutil.copy(src_img, dst_img)
            if os.path.exists(src_label):
                shutil.copy(src_label, dst_label)

    # Muove le immagini ed etichette nei rispettivi folder
    move_files(train_images, 'train')
    move_files(val_images, 'val')

    # Copia tutte le immagini e etichette del test set senza modificarle
    for img in os.listdir(test_path):
        if img.endswith(('.jpg', '.png')):
            shutil.copy(os.path.join(test_path, img), os.path.join(output_path, 'test/images', img))
            label_path = os.path.join(test_labels_path, img.replace('.jpg', '.txt').replace('.png', '.txt'))
            if os.path.exists(label_path):
                shutil.copy(label_path, os.path.join(output_path, 'test/labels', os.path.basename(label_path)))

    print(f"✅ Dataset YOLO creato con successo in {output_path}")
    print(f"📂 Train: {len(train_images)} immagini")
    print(f"📂 Val: {len(val_images)} immagini")
    print(f"📂 Test: {len(os.listdir(test_path))} immagini (copiate interamente)")

# Esempio di utilizzo
#create_yolo_dataset(
#    test_path="test",
#    test_labels_path="testLabels",
#    synth_path="synth",
#    real_path="real",
#    synth_labels_path="synthLabels",
#    real_labels_path="realLabels",
#    output_path="mixedNoAdapt25Dataset",
#    real_percentage=0.25,  # Usa il 25% delle immagini reali
#    train_split=0.8       # 80% train, 20% val
#)

#create_yolo_dataset(
#    test_path="test",
#    test_labels_path="testLabels",
#    synth_path="adaptedSynth/adaptedSynth",
#    real_path="real",
#    synth_labels_path="synthLabels",
#    real_labels_path="realLabels",
#    output_path="mixedAdapted25Dataset",
#    real_percentage=0.25,  # Usa il 25% delle immagini reali
#    train_split=0.8       # 80% train, 20% val
#)

#create_yolo_dataset(
#    test_path="test",
#    test_labels_path="testLabels",
#    synth_path="adaptedSynthV2/adaptedSynthV2",
#    real_path="real",
#    synth_labels_path="synthLabels",
#    real_labels_path="realLabels",
#    output_path="mixedAdapted25V2Dataset",
#    real_percentage=0.25,  # Usa il 25% delle immagini reali
#    train_split=0.8       # 80% train, 20% val
#)

create_yolo_dataset(
    test_path="test",
    test_labels_path="testLabels",
    synth_path="synth",
    real_path="real",
    synth_labels_path="synthLabels",
    real_labels_path="realLabels",
    output_path="mixed50Dataset",
    real_percentage=0.5,  # Usa il 25% delle immagini reali
    train_split=0.8       # 80% train, 20% val
)