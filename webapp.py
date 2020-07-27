# app.py
from flask import Flask, request, jsonify, render_template
from scrape_sources import *
app = Flask(__name__)


@app.route('/getcontent/', methods=['GET'])
def getcontent():
    src = request.args.get("src", None)
    lim = int(request.args.get("lim", None))

    if "reddit" in src:
        json_dump = get_subreddit(lim=lim)
    else:
        json_dump = get_site_data(url=src, lim=lim)

    print(f"Source: {src} Returning: {lim}")
    print(json_dump)

    response = {}

    if json_dump:
        response["MESSAGE"] = jsonify(json_dump)
    else:
        response["ERROR"] = "Pupper squash bugs"

    return jsonify(json_dump)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


@app.route('/summary', methods=['GET'])
def summary():
    url = request.args.get('url')
    response = summarize_url(url)
    return response, 200, {'Content-Type': 'text/plain'}


@app.route('/')
def index():
    json_dump = get_subreddit(lim=15)
    final_dict = []
    for val in json_dump:
        if val['title'] == None:
            continue
        else:
            final_dict.append(val)
    json_dump2 = get_site_data(url="goodnewsnetwork", lim=15)
    for val in json_dump2:
        final_dict.append(val)
    # print(final_dict)
    return render_template('index.html', mydict=final_dict)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
