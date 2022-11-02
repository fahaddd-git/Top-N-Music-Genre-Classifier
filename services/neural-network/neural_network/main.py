import numpy as np
from genre_classification_model import GenreClassificationModel
from neural_network.data_ingestion_helpers import get_labels, train_test_split

spectrogram_data = train_test_split()
data = spectrogram_data.train_data[0]
print(data)
print(data.shape)

foo = np.array(spectrogram_data.train_data)
print(foo.shape)

labels = get_labels()

model = GenreClassificationModel(spectrogram_data, labels)
model._model.build(foo.shape)
model._model.summary()

model._fit(10)
#
