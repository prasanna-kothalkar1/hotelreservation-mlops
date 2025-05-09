import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request


app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            lead_time = int(request.form["lead_time"])
            no_of_special_requests = int(request.form["no_of_special_requests"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])
            market_segment_type = int(request.form["market_segment_type"])
            no_of_weeknights = int(request.form["no_of_weeknights"])
            no_of_weekendnights = int(request.form["no_of_weekendnights"])
            meal_plan_type = int(request.form["meal_plan_type"])
            room_type = int(request.form["room_type"])
            features = np.array([[lead_time, no_of_special_requests, avg_price_per_room, arrival_month, arrival_date, market_segment_type, no_of_weeknights, no_of_weekendnights, meal_plan_type, room_type]])
            print("features: ",features)
            prediction = loaded_model.predict(features)[0]
            print("prediction: ",prediction)
            return render_template('index.html', prediction=int(prediction))
        except Exception as e:
            return render_template('index.html', prediction=str(e))
    return render_template('index.html',prediction=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5050)