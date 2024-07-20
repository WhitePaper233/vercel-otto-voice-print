import uuid
from flask import Flask, request, send_file

from api.otto import OTTO

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api():
    # 读取参数
    content = request.args.get('content', '')
    raw_mode = request.args.get('raw_mode', True)
    pitch = request.args.get('pitch', 1.0)
    speed = request.args.get('speed', 1.0)
    norm = request.args.get('norm', True)
    if not content:
        return
    
    # 生成音频
    otto = OTTO()
    otto.generate(content, raw_mode, pitch, speed, norm)

    # 导出文件
    file_name = uuid.uuid4().hex
    otto.export_file(f'/tmp/{file_name}.wav')

    return send_file(f'/tmp/{file_name}.wav', as_attachment=True)
