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


def plot(data: dict, show: bool = False) -> None:
    df = pd.DataFrame(data)
    df = df.groupby("first_kernal").agg(["mean", "std"])

    # fig = plt.figure()
    ax = plt.axes()

    ax.errorbar(df.index, df["accuracy"]["mean"], yerr=df["accuracy"]["std"], label="accuracy")
    ax.errorbar(df.index, df["loss"]["mean"], yerr=df["accuracy"]["std"], label="loss")
    ax.set_xlabel("Kernal Sizes")
    ax.set_title("Three Trials Mean and Std.")
    ax.legend()

    plt.savefig("bar.png", dpi=300)
    if show:
        plt.show()


if __name__ == "__main__":
    data = read_file("./test_results.txt")

    plot(data, True)
    df = pd.DataFrame(data)
    df = df.groupby("first_kernal").agg(["mean", "std"])
    print(df)
