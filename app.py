from flask import Flask, request, jsonify, redirect
import requests
import json

app = Flask(__name__)

# Load ItemData.json into memory once
with open('itemData.json', 'r') as file:
    item_data = json.load(file)

# Constants
API_KEY = "ILOVES3X"
BASE_URL = "https://ff.deaddos.online/api/data"
IMAGE_BASE_URL = "https://ff.deaddos.online/api/images"

def get_icon_by_item_id(item_id):
    for item in item_data:
        if item.get("itemID") == item_id:
            return item.get("icon")
    return None

def fetch_player_data(region, uid):
    try:
        response = requests.get(
            BASE_URL,
            params={"region": region, "uid": uid, "key": API_KEY}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

@app.route('/avatar')
def avatar():
    region = request.args.get("region")
    uid = request.args.get("uid")

    if not region or not uid:
        return jsonify({"error": "Missing region or uid"}), 400

    data = fetch_player_data(region, uid)
    if not data or "basicInfo" not in data:
        return jsonify({"error": "Failed to fetch player data"}), 500

    head_pic_id = data["basicInfo"].get("headPic")
    if head_pic_id is None:
        return jsonify({"error": "headPic not found in data"}), 404

    icon_name = get_icon_by_item_id(head_pic_id)
    if not icon_name:
        return jsonify({"error": "Icon not found for headPic ID"}), 404

    # Redirect to the actual image URL
    image_url = f"{IMAGE_BASE_URL}?iconName={icon_name}&key={API_KEY}"
    return redirect(image_url)

@app.route('/banner')
def banner():
    region = request.args.get("region")
    uid = request.args.get("uid")

    if not region or not uid:
        return jsonify({"error": "Missing region or uid"}), 400

    data = fetch_player_data(region, uid)
    if not data or "basicInfo" not in data:
        return jsonify({"error": "Failed to fetch player data"}), 500

    banner_id = data["basicInfo"].get("bannerId")
    if banner_id is None:
        return jsonify({"error": "bannerId not found in data"}), 404

    icon_name = get_icon_by_item_id(banner_id)
    if not icon_name:
        return jsonify({"error": "Icon not found for bannerId"}), 404

    image_url = f"{IMAGE_BASE_URL}?iconName={icon_name}&key={API_KEY}"
    return redirect(image_url)

if __name__ == '__main__':
    app.run(debug=True)
