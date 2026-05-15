import os
import json
import time
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing import image as keras_image
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# ─── Configuration ──────────────────────────────────────────────
IMG_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)
DATA_DIR = "dataset"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.h5")
META_PATH = os.path.join(MODEL_DIR, "model_meta.json")

# Default Hyperparameters
DEFAULT_EPOCHS = 30
DEFAULT_BATCH  = 16
DEFAULT_LR     = 1e-4

def build_augmentation_layer():
    return models.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.15),
        layers.RandomTranslation(0.1, 0.1),
        layers.RandomContrast(0.1)
    ], name="augmentation")

def build_preprocessing_layer():
    # EfficientNetV2 expects [0, 255] or scaling depending on the version
    # V2-S can take raw [0, 255] but we'll use rescaling for safety
    return layers.Rescaling(1./255, name="rescaling")

def build_model(num_classes):
    print(f"\n[INFO] Building Grandmaster Engine (EfficientNetV2-S)...")
    
    # Base model
    base_model = tf.keras.applications.EfficientNetV2S(
        input_shape=INPUT_SHAPE,
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # Freeze at start
    
    inputs = layers.Input(shape=INPUT_SHAPE, name="input_image")
    x = build_augmentation_layer()(inputs)
    x = build_preprocessing_layer()(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation='relu')(x)
    outputs = layers.Dense(num_classes, activation='softmax', name="predictions")(x)
    
    model = models.Model(inputs, outputs)
    return model, base_model

def load_dataset(data_dir, batch_size):
    print(f"[INFO] Loading data from {data_dir}...")
    
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode='categorical'
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=1337,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode='categorical'
    )
    
    class_names = train_ds.class_names
    return train_ds.prefetch(buffer_size=tf.data.AUTOTUNE), \
           val_ds.prefetch(buffer_size=tf.data.AUTOTUNE), \
           class_names

def train(args):
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    train_ds, val_ds, class_names = load_dataset(DATA_DIR, args.batch)
    num_classes = len(class_names)
    
    model, base_model = build_model(num_classes)
    
    # Callbacks
    early_stop = callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    reduce_lr = callbacks.ReduceLROnPlateau(factor=0.2, patience=5, min_lr=1e-7)
    checkpoint = callbacks.ModelCheckpoint(MODEL_PATH, save_best_weights=True, monitor='val_accuracy')
    
    # Phase 1: Feature Extraction
    print(f"\n[PHASE 1] Training top layers for {args.epochs} epochs...")
    model.compile(
        optimizer=optimizers.Adam(learning_rate=args.lr),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
        metrics=['accuracy']
    )
    
    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=[early_stop, reduce_lr, checkpoint]
    )
    
    # Phase 2: Fine-Tuning
    if args.finetune:
        print(f"\n[PHASE 2] Unfreezing base model for deep adaptation...")
        base_model.trainable = True
        
        # Fine-tune with much lower learning rate
        model.compile(
            optimizer=optimizers.Adam(learning_rate=args.lr / 10),
            loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
            metrics=['accuracy']
        )
        
        history2 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=args.ft_epochs,
            callbacks=[early_stop, reduce_lr, checkpoint]
        )
    
    print(f"\n[INFO] Saving final weights and metadata...")
    # Metadata
    meta = {
        "class_names": class_names,
        "accuracy": float(model.history.history['val_accuracy'][-1]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "architecture": "EfficientNetV2-S"
    }
    with open(META_PATH, 'w') as f:
        json.dump(meta, f, indent=4)
    
    print(f"[INFO] Training Complete. Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grandmaster Steel Defect Training")
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    parser.add_argument("--batch", type=int, default=DEFAULT_BATCH)
    parser.add_argument("--lr", type=float, default=DEFAULT_LR)
    parser.add_argument("--finetune", action="store_true", default=True)
    parser.add_argument("--ft-epochs", type=int, default=20)
    args = parser.parse_args()
    train(args)
