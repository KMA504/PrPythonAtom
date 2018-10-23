from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/get_classifier_result/<version>", methods=['GET', 'POST'])
def return_classifier_result(version):
    answer = request.get_json()
    vers=int(version)
    if vers==1:
        data={'version': 1, "predict": answer['predict']}
        js1=json.dumps(data)
        return json.dumps({'version': 1, "predict": answer['predict']})
    elif vers==0:
        return json.dumps({'version': 0, "predict": answer['old_predict']})
    else:
        return 'You are wrong!'

@app.route("/")
def hello():
    return 'Hello! This server represents a storage of classifier results, so you may return both old and actual predictions. If you would like to return the previous one, you should type \'/get_classifier_result/0\', otherwise type \'/get_classifier_result/1\'. Have a nice day!'

if __name__ == "__main__":
    app.run()
