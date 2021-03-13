import json
import random
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

        p1 = random.choice(consolidatedData['allPrunedPara_0'])
        p2 = random.choice(consolidatedData['allPrunedPara_1'])
        p3 = random.choice(consolidatedData['allPrunedPara_2'])
        
        return json.dumps({"msg": "success", 
                           "paras": {"p1": p1, "p2": p2, "p3": p3}})

    except Exception as e:
        return json.dumps({"msg": f"server encountered an error: {e}", "paras": None})


if __name__ == "__main__":
    main()