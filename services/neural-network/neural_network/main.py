# import numpy as np
# from pathlib import Path
from genre_classification_model import GenreClassificationModel
from neural_network.data_ingestion_helpers import train_test_split

spectrogram_data = train_test_split()
data = spectrogram_data.train_data[0]
# print(data)
# print(data.shape)

# foo = np.array(spectrogram_data.train_data)
# print(foo.shape)

model = GenreClassificationModel(spectrogram_data)
# model._model.build()
# model._model.summary()

model.fit(20)
print(model.evaluate())
# model.save(Path.home() / "model")
