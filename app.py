from flask import Flask, request

from classif import recognize_stained_glass

app = Flask(__name__)


@app.route("/classify", methods=["POST"])
def classify():
    try:
        image = request.files["image"]
    except KeyError:
        return {
            "image": "This field is required"
        }, 400
    stained_glass_data = recognize_stained_glass(image)
    return stained_glass_data, 200


app.run()
