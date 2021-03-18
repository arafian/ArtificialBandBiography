import json
import random
from Paragraph_Replacer import replace
from flask import Flask, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def main():

    try:
        with open("data/consolidatedData.json", 'r', encoding='utf-8') as f:
            consolidatedData = json.load(f)

        genMethod = request.args.get("gen")

        if (genMethod == "standard"):
            p = random.choice(consolidatedData['allPrunedParaComplete'])
        else:
           p = [random.choice(consolidatedData['allPrunedPara_1']),
                random.choice(consolidatedData['allPrunedPara_2']),
                random.choice(consolidatedData['allPrunedPara_3'])]

        p, band_name = replace(p)
        keys = ['p1','p2','p3']

        paras = dict(zip(keys, p))
        return json.dumps({"msg": "success", 
                           "gen": genMethod,
                           "band_name": band_name,
                           "paras": paras})

    except Exception as e:
        return json.dumps({"msg": f"server encountered an error: {e}", "paras": None})


if __name__ == "__main__":
    main()
    