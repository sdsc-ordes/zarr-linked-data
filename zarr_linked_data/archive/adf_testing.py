import json
import h5py
import pandas as pd
import numpy as np
from pkg_resources import resource_filename

data_path = resource_filename("cat_plus", "data/")

# ex_json_path = data_path + "ExampleJSON.json"

# with open(ex_json_path) as ex_json:
#     ex_json = json.load(ex_json)

# print(ex_json.keys())

adf_path = data_path + "ExampleADF.ADF"

adf = h5py.File(adf_path, "r")

print(list(adf.keys()))

print(adf["data-cubes"].keys())

print(
    adf["data-cubes"]["dc-VWD1B-782a8be1-245e-4640-9c76-165962f0de92"]["measures"][
        "07741aa6-08b5-4387-834d-6153a1b76a81"
    ]
)

# subset ?
df = pd.DataFrame(
    np.array(
        adf["data-cubes"]["dc-VWD1B-782a8be1-245e-4640-9c76-165962f0de92"]["measures"][
            "07741aa6-08b5-4387-834d-6153a1b76a81"
        ]
    )
)
print(df)

print(adf["data-description"].keys())
print(adf["data-description"]["dictionary"])

print(adf["data-description"]["quads"])
quads = pd.DataFrame(np.array(adf["data-description"]["quads"]))
print(quads)
# print(adf["data-description"]['dictionary']['keys'][0:10])
