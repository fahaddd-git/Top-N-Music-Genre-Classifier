import os
import subprocess
import zipfile
from pathlib import Path
from time import sleep

import gdown

os.environ["SQLITE_DB_PATH"] = "../utilities/resources/data.db"

OUTPUT = Path.home() / "tmp_gtzan.zip"
OUTPUT_EXTRACTED = Path.home() / "tmp_gtzan"
GTZAN_DIR = Path.home() / "gtzan"


def install_services():
    subprocess.run(["./install-services.sh"], cwd="../")


def download_dataset():
    url = "https://drive.google.com/uc?id=19LzzsniBzvpp5UmJ24cXMt4kPY8UxyQC"
    gdown.download(url, OUTPUT, quiet=False)

    with zipfile.ZipFile(OUTPUT, "r") as zip_ref:
        zip_ref.extractall(OUTPUT_EXTRACTED)

    if not GTZAN_DIR.exists():
        GTZAN_DIR.mkdir()

    for file in Path(OUTPUT_EXTRACTED).glob("**/*.wav"):
        file.rename(GTZAN_DIR / file.name)


def start_etl_service():
    return subprocess.Popen(["poetry", "run", "start"], cwd="../etl-service/")


def wait_for_first_round_of_etl_service(etl_service_process):
    while len(list(Path(GTZAN_DIR).glob("*.wav"))) != 0:
        print("waiting for etl_service to finish")
        sleep(1)
    etl_process.kill()


def generate_neural_network_model():
    input = "\n".join(["20", "../prediction-api/prediction_api/model"])
    subprocess.run(
        ["poetry", "run", "generate-model"], input=input.encode(), cwd="../neural-network"
    )


def start_prediction_api():
    return subprocess.Popen(["poetry", "run", "start"], cwd="../prediction-api")


if __name__ == "__main__":
    install_services()
    download_dataset()
    etl_process = start_etl_service()
    wait_for_first_round_of_etl_service(etl_process)
    generate_neural_network_model()
    prediction_api_process = start_prediction_api()
    sleep(15)
    # TODO add some requests to the predicition api here
    prediction_api_process.kill()
