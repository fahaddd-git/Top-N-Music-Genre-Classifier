import numpy as np
from genre_classification_model import GenreClassificationModel
from neural_network.data_ingestion_helpers import train_test_split
from neural_network.util import get_labels, image_to_array

spectrogram_data = train_test_split()
data = image_to_array(spectrogram_data.train_data[0])
print(data)
print(data.shape)

foo = np.array([image_to_array(s) for s in spectrogram_data.train_data])
print(foo.shape)

labels = get_labels()

model = GenreClassificationModel(spectrogram_data, labels)
model.model.build(foo.shape)
model.model.summary()

model._fit(10)
#
