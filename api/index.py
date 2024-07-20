from flask import Flask, request, send_file

from api.otto import OTTO

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api():
    # 读取参数
    content = request.args.get('content', '')
    if not content:
        return 
    
    otto = OTTO()
    otto.generate(content)
    otto.export_file('/tmp/output.wav')

    return send_file('/tmp/output.wav', as_attachment=True)