from flask import Flask
from flask import Flask, request
from flask import jsonify
import uuid
import os
from flask_cors import CORS, cross_origin


app = Flask(__name__, static_folder='file', static_url_path='/file', template_folder='mytemplate')

@app.route('/uploadFile', methods=['POST'])
@cross_origin()
def uploadFile():
    data = request.files
    file = data['file']
    file_dir = "file"

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建

    ext = file.filename.rsplit('.', 1)[-1]  # 获取文件后缀
    new_filename = str(uuid.uuid4()) + '.' + ext  # 修改文件名
    new_filename = new_filename.replace('.blob', '.wav')
    file.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录

    url = request.host_url + "/" + os.path.join(file_dir, new_filename)
    return url

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)