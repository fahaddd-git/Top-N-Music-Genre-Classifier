import time

from neural_network.data_ingestion_helpers import train_test_split
from neural_network.genre_classification_model import GenreClassificationModel

epochs = 7
test_cases = []
for _ in range(3):
    for kernal_size in [3, 5, 7, 9, 11, 13]:
        filters_i, filters_j, filters_k = 8, 8, 16
        test_cases.append(
            ((filters_i, kernal_size), (filters_j, kernal_size), (filters_k, kernal_size))
        )


with open("test_results.txt", "w") as f:
    f.write("loss\taccurracy\tparams\n")
    i = 0
    start = time.time()
    for test in test_cases:
        spectrogram_data = train_test_split()
        spectrogram_model = GenreClassificationModel(spectrogram_data)
        spectrogram_model._add_convolutional_layers(test[0], test[1], test[2])
        spectrogram_model._compile()
        spectrogram_model.fit(epochs)

        results = spectrogram_model.evaluate()
        print(results)
        f.write(f"{results['loss']}\t{results['accuracy']}\t{str(test)}\n")
        i += 1
        print(f"{i} of {len(test_cases)} completed")
        now = time.time()
        print("Seconds elapsed: ", now - start)
