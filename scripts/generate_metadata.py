import os
from pathlib import Path
import json
from brownie import network
from metadata import sample_metadata

IMAGE_BASE_URI = "ipfs://QmdPDN9cxtjjbQHDLMGL4e2DpbeeyYaKUqrNQSMKSf8bEU/"
COLLECTION_NAME = "OtherDeedClone"


def main():
    generate_metadata()


def generate_metadata():
    images = os.listdir("./img")
    for image_number in range(len(images)):
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(image_number) + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            sample_metadata.metadata_template["name"] = (
                COLLECTION_NAME + "#" + str(image_number)
            )

            sample_metadata.metadata_template[
                "description"
            ] = "An adorable {} land!".format(sample_metadata.metadata_template["name"])
            sample_metadata.metadata_template["image"] = (
                IMAGE_BASE_URI + str(image_number) + ".png"
            )

            with open(metadata_file_name, "w") as file:
                json.dump(sample_metadata.metadata_template, file)
