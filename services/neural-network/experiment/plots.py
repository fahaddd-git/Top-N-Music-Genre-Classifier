import csv
from ast import literal_eval

import matplotlib.pyplot as plt
import pandas as pd


def read_file(filename: str) -> dict:
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


def plot_accuracy(data: dict, title: str, fname: str, show: bool = False) -> None:
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    p = ax.scatter(
        data["first_filters"],
        data["second_filters"],
        data["third_filters"],
        c=data["accuracy"],
        cmap="gnuplot_r",
        marker=".",
        # linewidth=0.5,
    )
    fig.colorbar(p, location="left", label="accuracy")
    ax.set_xlabel("Filters In First Layer")
    ax.set_ylabel("Filters In Second Layer")
    ax.set_zlabel("Filters In Third Layer")
    ax.set_title(title)

    plt.savefig(fname, dpi=300)
    if show:
        plt.show()


def plot_loss(data: dict, title: str, fname: str, show: bool = False) -> None:
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    p = ax.scatter(
        data["first_filters"],
        data["second_filters"],
        data["third_filters"],
        c=data["loss"],
        cmap="gnuplot_r",
        marker=".",
        # linewidth=0.5,
    )
    fig.colorbar(p, location="left", label="loss")
    ax.set_xlabel("Filters In First Layer")
    ax.set_ylabel("Filters In Second Layer")
    ax.set_zlabel("Filters In Third Layer")
    ax.set_title(title)

    plt.savefig(fname, dpi=300)
    if show:
        plt.show()


if __name__ == "__main__":
    data = read_file("./test_results.txt")
    df = pd.DataFrame(data)

    plot_accuracy(df, "All Kernal Size", "accuracy_all_kernal_sizes.png", False)
    plot_loss(df, "All Kernal Sizes", "loss_all_kernal_sizes.png", False)

    plot_accuracy(
        df[df["first_kernal"] == 1], "All Kernal Sizes = 1", "accuracy_kernal_size_1.png", False
    )
    plot_loss(df[df["first_kernal"] == 1], "All Kernal Sizes", "loss_kernal_size_1.png", False)

    plot_accuracy(
        df[df["first_kernal"] == 3], "All Kernal Sizes = 3", "accuracy_kernal_size_3.png", False
    )
    plot_loss(df[df["first_kernal"] == 3], "All Kernal Sizes", "loss_kernal_size_3.png", False)

    plot_accuracy(
        df[df["first_kernal"] == 5], "All Kernal Sizes = 5", "accuracy_kernal_size_5.png", False
    )
    plot_loss(df[df["first_kernal"] == 5], "All Kernal Sizes", "loss_kernal_size_5.png", False)
