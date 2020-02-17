from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from main import Model
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, resources=r'/*')
# deal with the cross-domain problem

@app.route('/core/track', methods=['POST'])
def text_match():
    """

    :return:
    """
    json_data = request.get_data()
    info = dict()
    try:
        raw_data = json.loads(json_data)
        patients = raw_data["patientList"]
        model = Model(raw_data["spaceTimeDataList"])
        model.find_community_label()
        info['code'] = 0
        info['data'] = list()
        if len(patients) != 0:
            patient_list = [x["user_id"] for x in patients]
            print("patient_list: ", patient_list)
            for patient in patient_list:
                search_result = model.search(patient)
                print("search_result: ", search_result)
                contact_list = list(set(search_result.keys()))
                print("contact_list: ", contact_list)
                for contact in contact_list:
                    if contact not in patient_list: # 对于患者，无需记录其为接触者
                        contact_dict = dict()
                        contact_dict['use_id'] = contact
                        for record in search_result[contact]:
                            if len(record):
                                print(record)
                                contact_dict['time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(record[1]))
                                break
                        info['data'].append(contact_dict)

    except (json.decoder.JSONDecodeError, TypeError):
        info['code'] = 1
        info['data'] = list()

    print(model.community_dict)
    print(model.community_result)
    print('function: track')
    return jsonify(info)

if __name__ == '__main__':
    app.run()