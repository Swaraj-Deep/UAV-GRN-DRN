from flask import Flask, render_template, request, redirect, session, make_response, jsonify, send_from_directory, abort
import os
import json
import os.path

app = Flask(__name__)
app.secret_key = 'kldjlkmxcvioermklxjos90873489*&86*&I09'
app.config['FILE_UPLOADS'] = os.getcwd() + '/visualize_output/static/uploads'


@app.route('/')
def dash_board() -> 'html':
    return render_template('input.html', the_title='Visualize Here')


@app.route('/__verify_upload__', methods=['POST'])
def verify_upload() -> 'json':
    uploaded_file = request.files['file']
    try:
        file_data = json.load(uploaded_file)
        response = {
            'Data': file_data,
            'Message': 'Success'
        }
    except Exception as e:
        print(e)
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    app.run(debug=True)
