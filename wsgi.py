from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from main import Model
from risk_assess import risk_model
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, resources=r'/*')
# deal with the cross-domain problem


@app.route('/core/contact', methods=['GET'])
def contact():
    info = dict()
    model = Model()
    model.find_community_label()
    info['code'] = 0
    info['data'] = list()
    if len(model.patients) != 0:
        patient_list = [x["user_id"] for x in model.patients]
        print("patient_list: ", patient_list)
        for patient in patient_list:
            search_result = model.search(patient)
            print("search_result: ", search_result)
            if len(search_result) == 0:
                continue
            contact_list = list(set(search_result.keys()))
            print("contact_list: ", contact_list)
            for contact in contact_list:
                if contact not in patient_list:  # 对于患者，无需记录其为接触者
                    contact_dict = dict()
                    contact_dict['use_id'] = contact
                    for record in search_result[contact]:
                        if len(record):
                            print(record)
                            contact_dict['time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(record[1]))
                            contact_dict["lon"] = record[2]
                            contact_dict["lat"] = record[3]
                            break
                    info['data'].append(contact_dict)
    return jsonify(info)


@app.route('/core/risk', methods=['POST'])
def risk():
    json_data = request.get_data()
    info = dict()
    info['data'] = False
    try:
        info['code'] = 0
        raw_data = json.loads(json_data)
        if type(raw_data['lon']) == str:
            raw_data['lon'] = eval(raw_data['lon'])
            raw_data['lat'] = eval(raw_data['lat'])
        risk = risk_model(raw_data['lon'], raw_data['lat'], raw_data['time'].split()[0])
        if len(risk.data):
            info['data'] = True
    except (json.decoder.JSONDecodeError, TypeError):
        info['code'] = 1
    print('function: risk')
    return jsonify(info)

if __name__ == '__main__':
    app.run()
