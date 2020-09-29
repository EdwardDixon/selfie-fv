# Takes an attributes CSV (from pseudonomize) and a filename->face vectors mapping (in a json), outputs pickled train and test dfs
from argparse import ArgumentParser
import pickle
import json 
import pandas as pd


def build_train_and_test_set(attributes_csv, filename_to_vectors_json):
    df_attributes = pd.read_csv(attributes_csv)
    df_attributes = df_attributes.drop(columns=["id"])

    fh_vecs = open(filename_to_vectors_json, "r")
    face_to_vecs = json.load(fh_vecs)

    filenames = []
    vecs = []

    for k in face_to_vecs.keys():
        filenames.append(k)
        vecs.append(face_to_vecs[k])

    df_fname_vecs = pd.DataFrame({"filename":filenames, "embedding":vecs})

    df_merged = pd.merge(df_attributes, df_fname_vecs, on=['filename','filename'])

    df_train = df_merged[df_merged.testset == False]
    df_test = df_merged[df_merged.testset == True]

    f_train = open("selfie_train.pkl", "wb")
    f_test = open("selfie_test.pkl", "wb")
    
    pickle.dump(df_train, f_train)
    pickle.dump(df_test, f_test)
    



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--attributes", type=str, help="CSV file with dataset attributes (subject id, age, filename)")
    parser.add_argument("--vectors", type=str, help="Path to face vectors JSON")
    
    args = parser.parse_args()

    build_train_and_test_set(args.attributes, args.vectors)

