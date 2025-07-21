from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

with open('itemData.json') as f:
    item_data = json.load(f)

@app.route('/', methods=['GET'])
def get_icon():
    item_id = request.args.get('id', type=int)
    if item_id is None:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    for item in item_data:
        if item.get("Id") == item_id:
            icon_name = item.get("Icon")

            # Replace prefix if needed
            if icon_name.startswith("Icon_callsign_storebg"):
                icon_name = icon_name.replace("Icon_callsign_storebg", "Icon_callsign_basebg", 1)

            image_url = f"https://freefiremobile-a.akamaihd.net/common/Local/PK/FF_UI_Icon/{icon_name}.png"
            return jsonify({
                "Id": item_id,
                "Icon": icon_name,
                "Image": image_url
            })

    return jsonify({"error": f"No item found with Id {item_id}"}), 404

if __name__ == '__main__':
    app.run(debug=True)
