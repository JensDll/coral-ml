import tarfile
import pathlib
import os
from typing import List, Tuple
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import preprocessing
from tensorflow.python.ops.gen_math_ops import select

DATASET_URL = "http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar"
ANNOTATION_URL = "http://vision.stanford.edu/aditya86/ImageNetDogs/annotation.tar"

AUTOTUNE = tf.data.AUTOTUNE


def len_iter(iter):
    return sum(1 for _ in iter)


def fetch_data(extract_dir=pathlib.Path().parent.resolve().joinpath("data")) -> Tuple[pathlib.Path, pathlib.Path]:
    image_dir = keras.utils.get_file(
        'stanford_dogs_data', origin=DATASET_URL)
    anno_dir = keras.utils.get_file(
        "stanford_dogs_annotation", origin=ANNOTATION_URL)

    image_extract = extract_dir.joinpath("Images")
    if not image_extract.is_dir():
        with tarfile.open(image_dir) as tar:
            tar.extractall(extract_dir)

    anno_extract = extract_dir.joinpath("Annotation")
    if not anno_extract.is_dir():
        with tarfile.open(anno_dir) as tar:
            tar.extractall(extract_dir)

    return image_extract, anno_extract


class StanfordDogLoader:
    class_names: List[str] = []
    norm_class_names: List[str] = []
    train_size = 0
    val_size = 0
    test_size = 0

    def __init__(self) -> None:
        data_dir, anno_dir = fetch_data()

        self.data_dir = data_dir
        self.anno_dir = anno_dir

    def load(self, val_split=0.2, test_split=0.1, verbose=1):
        class_names = np.array([item.name for item in self.data_dir.glob('*')])
        count_per_class = [len_iter(pathlib.Path(path).glob("*"))
                           for path in self.data_dir.glob("*")]
        norm_class_names = [
            name.split("-")[1].replace("_", " ") for name in class_names
        ]

        self.class_names = class_names
        self.norm_class_names = norm_class_names

        train_ds, val_ds, test_ds = self.__split_train_val_test(
            self.data_dir, count_per_class, val_split, test_split)

        self.train_size = train_ds.cardinality()
        self.val_size = val_ds.cardinality()
        self.test_size = test_ds.cardinality()

        train_ds = train_ds \
            .shuffle(self.train_size) \
            .map(self.process_path, num_parallel_calls=AUTOTUNE)

        val_ds = val_ds \
            .shuffle(self.val_size) \
            .map(self.process_path, num_parallel_calls=AUTOTUNE)

        test_ds = test_ds \
            .shuffle(self.test_size, seed=42, reshuffle_each_iteration=False) \
            .map(self.process_path, num_parallel_calls=AUTOTUNE) \

        if verbose > 0:
            print(f"[INFO] Fetched {sum(count_per_class)} images")
            print(f"[INFO] Found {len(count_per_class)} classes")
            print("[INFO] The first ten classes are")
            print(class_names[:10])
            print("[INFO] Image count per class")
            print(count_per_class)
            print("[INFO] The dataset split is")
            print(f"- Train {self.train_size}")
            print(f"- Val {self.val_size}")
            print(f"- Test {self.test_size}")

        return train_ds, val_ds, test_ds

    def get_label(self, file_path):
        parts = tf.strings.split(file_path, os.sep)
        one_hot = parts[-2] == self.class_names
        return tf.argmax(one_hot)

    def decode_img(self, img):
        return tf.io.decode_jpeg(img, channels=3)

    def process_path(self, file_path):
        label = self.get_label(file_path)
        img = tf.io.read_file(file_path)
        img = self.decode_img(img)
        return img, label

    def __split_train_val_test(self, data_dir, count_per_class, val_split, test_split):
        train_ds = None
        val_ds = None
        test_ds = None

        for i, path in enumerate(data_dir.glob("*")):
            path_ds = tf.data.Dataset.list_files(
                os.path.join(path, "*"), shuffle=False)

            val_size = int(count_per_class[i] * val_split)
            test_size = int(count_per_class[i] * test_split)

            val_take = path_ds.take(val_size)
            test_take = path_ds.skip(val_size).take(test_size)
            train_take = path_ds.skip(val_size + test_size)

            if i == 0:
                train_ds = train_take
                val_ds = val_take
                test_ds = test_take
            else:
                train_ds = train_ds.concatenate(train_take)
                val_ds = val_ds.concatenate(val_take)
                test_ds = test_ds.concatenate(test_take)

        return train_ds, val_ds, test_ds
