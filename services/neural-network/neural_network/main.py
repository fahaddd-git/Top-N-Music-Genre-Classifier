from genre_classification_model import GenreClassificationModel
from train_test_split import train_test_split
from util import get_labels, image_to_array

spectrogram_data = train_test_split()
data = image_to_array(spectrogram_data.train_data[0])
print(data)
print(data.shape)

labels = get_labels()

model = GenreClassificationModel(spectrogram_data, labels)
model.model.build(data.shape)
model.model.summary()

model._evaluate(10)
