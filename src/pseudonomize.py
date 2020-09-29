import pandas as pd
from argparse import ArgumentParser
import glob
import shutil
import os 
import uuid
import random


def main(target_folder, csv_path, out_folder, dry_run = False, train_test_split=0.8):
    filenames = glob.glob(os.path.join(target_folder, "*.jpg"))

    ids = []
    ages = []
    imagenos = []
    uuids = []

    old_filenames = []
    new_filenames = []

    copy_count = 0

    id_to_uuid = dict()
    in_test_set = []
    id_to_test_set_status = dict()

    for f in filenames:
        id, age, imageno = os.path.basename(f).replace(".jpg","").split("_")
        ids.append(id)
        ages.append(float(age))
        imagenos.append(int(imageno))

        cur_id_in_test_set = False
        if id not in id_to_uuid:
            new_id = uuid.uuid4()
            id_to_uuid[id] = new_id
            if random.random() > train_test_split:
                cur_id_in_test_set = True
            id_to_test_set_status[id]  = cur_id_in_test_set

        else:
            new_id = id_to_uuid[id]
            cur_id_in_test_set = id_to_test_set_status[id]

        uuids.append(new_id)
        old_filenames.append(f)
        in_test_set.append(cur_id_in_test_set)

        new_filename = f"{new_id}_{age}_{imageno}.jpg"
        new_filenames.append(new_filename)

        full_new_path = os.path.join(out_folder, new_filename)
        if dry_run is False:
            print(f"Copying {f} to {full_new_path}")

            if os.path.isfile(full_new_path) == False:
                shutil.copyfile(f, full_new_path)
            else:
                print(f"Skipping {f} (already present)")

            copy_count = copy_count + 1
        else:
            print(f"DRYRUN: Pretending to copy {f} to {full_new_path}")


    df = pd.DataFrame({"id":ids, "age":ages, "imageno":imagenos, "uuids":uuids, "filename":new_filenames, "testset":in_test_set})
    df.to_csv(csv_path, index=False)

    print(f"{copy_count} file(s) were copied to {out_folder}, details in {csv_path}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--target", type=str, help="Folder with image set", required=True)
    parser.add_argument("--out_csv", type=str, help="Name of CSV to create with results", default="dataset.csv", required=False)
    parser.add_argument("--out_folder", type=str, help="Where to put pseudonmized images", required=True)
    parser.add_argument("--dryrun", action="store_true", help="Use for a dummy run (no files copied)", required=False, default=False)
    args = parser.parse_args()

    main(args.target, args.out_csv, args.out_folder, args.dryrun)

