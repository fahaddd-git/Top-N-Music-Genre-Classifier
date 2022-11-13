import csv
from ast import literal_eval

import matplotlib.pyplot as plt


def read_file(filename):
    results = {
        "loss": [],
        "accuracy": [],
        "first_filters": [],
        "second_filters": [],
        "third_filters": [],
        "first_kernal": [],
        "second_kernal": [],
        "third_kernal": [],
    }
    with open(filename, "r") as f:
        data = csv.reader(f, delimiter="\t")
        next(data)
        for row in data:
            results["loss"].append(float(row[0]))
            results["accuracy"].append(float(row[1]))
            params = literal_eval(row[2])

            results["first_filters"].append(params[0][0])
            results["second_filters"].append(params[1][0])
            results["third_filters"].append(params[2][0])
            results["first_kernal"].append(params[0][1])
            results["second_kernal"].append(params[1][1])
            results["third_kernal"].append(params[2][1])
    return results


data = read_file("./test_results.txt")


def plot_accuracy():
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    p = ax.scatter(
        data["first_filters"],
        data["second_filters"],
        data["third_filters"],
        c=data["accuracy"],
        cmap="gnuplot_r",
        linewidth=0.5,
    )
    fig.colorbar(p, location="left", label="accuracy")
    ax.set_xlabel("Filters In First Layer")
    ax.set_ylabel("Filters In Second Layer")
    ax.set_zlabel("Filters In Third Layer")
    ax.set_title("Trained With 5 Epochs")

    plt.savefig("accuracy.png", dpi=300)


def plot_loss():
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    p = ax.scatter(
        data["first_filters"],
        data["second_filters"],
        data["third_filters"],
        c=data["loss"],
        cmap="gnuplot_r",
        linewidth=0.5,
    )
    fig.colorbar(p, location="left", label="loss")
    ax.set_xlabel("Filters In First Layer")
    ax.set_ylabel("Filters In Second Layer")
    ax.set_zlabel("Filters In Third Layer")
    ax.set_title("Trained With 5 Epochs")

    plt.savefig("loss.png", dpi=300)


plot_accuracy()
plot_loss()
