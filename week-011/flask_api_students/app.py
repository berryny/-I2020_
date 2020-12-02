from flask import Flask, request, jsonify

app = Flask(__name__)

d =[ 
    {
        'id': 1,
        'name': 'jane doe',
    },
    {
        'id': 2,
        'name': 'jake doe',
    },
    {
        'id': 3,
        'name': 'mary anne',
    }
]

@app.route('/', methods=['GET'])
def get_records():
    print(d)
    return jsonify(d)

@app.route('/', methods=['POST'])
def create_record():
    added = dict(request.args)
    dataS = {}
    for k,v in request.args.items():
        print('k,v',k,v)
        for i in d['id']:
            print('i',i)
            
#     for k,v in request.args.items():
#         dataS['id'] = k
#         dataS['name'] = v
#     d.append(dataS)
#     return jsonify({"added": added, "current": d})
    return jsonify({"status": 'ok'})

@app.route('/', methods=['DELETE'])
def delete_record():
    deleted = {}
    for k,v in request.args.items():
        try:
            d.pop(k)
            deleted[k] = v
        except:
            continue
    return jsonify({"deleted": deleted, "current": d})
                
if __name__ == '__main__':
    app.run(debug=True)