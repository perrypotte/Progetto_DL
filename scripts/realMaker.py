import os
import shutil
import random

def create_yolo_dataset(real_images_dir, real_labels_dir, output_dir):
    """
    Crea un dataset YOLO nel formato corretto, suddividendo le immagini reali in 80% train e 20% val.
    
    :param real_images_dir: Directory contenente tutte le immagini reali.
    :param real_labels_dir: Directory contenente le annotazioni YOLO.
    :param output_dir: Directory principale in cui verrà creato il dataset YOLO.
    """

    # Definizione delle cartelle YOLO
    train_images_dir = os.path.join(output_dir, "train/images")
    train_labels_dir = os.path.join(output_dir, "train/labels")
    val_images_dir = os.path.join(output_dir, "val/images")
    val_labels_dir = os.path.join(output_dir, "val/labels")
    test_images_dir = os.path.join(output_dir, "test/images")  # Rimane vuota
    test_labels_dir = os.path.join(output_dir, "test/labels")  # Rimane vuota

    # Creazione delle directory
    for d in [train_images_dir, train_labels_dir, val_images_dir, val_labels_dir, test_images_dir, test_labels_dir]:
        os.makedirs(d, exist_ok=True)

    # Lista delle immagini reali
    images = [img for img in os.listdir(real_images_dir) if img.endswith((".jpg", ".png", ".jpeg"))]

    # Mescola casualmente le immagini
    random.shuffle(images)

    # Suddivisione 80% train - 20% val
    num_train = int(len(images) * 0.8)
    train_images = images[:num_train]
    val_images = images[num_train:]

    def copy_files(images_list, src_img_dir, src_lbl_dir, dst_img_dir, dst_lbl_dir):
        """Copia immagini e annotazioni YOLO corrispondenti."""
        for img_file in images_list:
            shutil.copy(os.path.join(src_img_dir, img_file), os.path.join(dst_img_dir, img_file))

            # Trova e copia il file di annotazione YOLO corrispondente
            label_file = os.path.splitext(img_file)[0] + ".txt"
            label_src_path = os.path.join(src_lbl_dir, label_file)
            if os.path.exists(label_src_path):
                shutil.copy(label_src_path, os.path.join(dst_lbl_dir, label_file))

    # Copia i file nei rispettivi set
    copy_files(train_images, real_images_dir, real_labels_dir, train_images_dir, train_labels_dir)
    copy_files(val_images, real_images_dir, real_labels_dir, val_images_dir, val_labels_dir)

    # Creazione del file data.yaml
    yaml_content = f"""train: {os.path.abspath(os.path.join(output_dir, "train"))}
val: {os.path.abspath(os.path.join(output_dir, "val"))}
test: {os.path.abspath(os.path.join(output_dir, "test"))}

nc: NUM_CLASSES  # Sostituisci con il numero di classi
names: ["class_0", "class_1"]  # Modifica con i nomi delle classi
"""

    with open(os.path.join(output_dir, "data.yaml"), "w") as f:
        f.write(yaml_content)

    print(f"✅ {len(train_images)} immagini e annotazioni in train")
    print(f"✅ {len(val_images)} immagini e annotazioni in val")
    print(f"✅ Dataset YOLO creato in '{output_dir}' con la giusta struttura")
    print("⚠️ Ricorda di modificare 'data.yaml' con il numero corretto di classi e i loro nomi.")


#Si può usare sia per fare fullSynth che fullReal
#In entrambi i casi la cartella test la si inserisce manualmente

# Esegui la funzione
real_images_dir = "real"
real_labels_dir = "realLabels"
output_dir = "realDataset"

create_yolo_dataset(real_images_dir, real_labels_dir, output_dir)
