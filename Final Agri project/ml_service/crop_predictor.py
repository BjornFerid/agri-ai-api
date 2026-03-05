import time
import joblib
from supabase import create_client

url = "https://ztoszlsrpjebggynvywh.supabase.co"
key = "sb_publishable_7pAXKxkAOT0KGUpY7NdR3g_U_Bgh20-"

supabase = create_client(url, key)

model = joblib.load("../models/crop_model.pkl")

print("Crop prediction service started...")

while True:

    response = supabase.table("soil_data").select("*").execute()
    rows = response.data

    for row in rows:

        if row["crop_label"] is None:

            data = [[
                row["nitrogen"],
                row["phosphorus"],
                row["potassium"],
                row["temperature"],
                row["moisture"],
                row["ph"]
            ]]

            prediction = model.predict(data)[0]

            supabase.table("soil_data").update({
                "crop_label": prediction
            }).eq("id", row["id"]).execute()

            print("Predicted crop:", prediction)

    time.sleep(5)