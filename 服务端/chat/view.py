# _*_ coding: utf-8 _*_

#业务模块
import openai
from django.shortcuts import HttpResponse
import json
from django.shortcuts import render


#密钥
openai.api_key = "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"


def chatgpt(request):
    """
       chatgpt聊天
    """
    keys = [
     "xskj666"
    ]
    
    question = request.GET.get('q')
    key      = request.GET.get('key')
    
    if key not in keys:
        data = "密钥有误！"
    else:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
        data = completion.choices[0].message.content
        
    res = {
        "code": 200,
        "content": data
    }
    
    return HttpResponse(json.dumps(res, ensure_ascii=False))

def index(request):
    
    
    return render(request, 'index.html')


def uploadFile(request):
    
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
    
    