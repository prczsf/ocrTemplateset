from flask import Flask, send_from_directory
from flask_restful import Api
from controller.paddle_offline_controller import PaddleOfflineOcrView
from controller.product_controller import ProductView

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'filesPic'

api = Api(app)
# 配置静态文件目录

# git 版本控制1
# git 版本控制2

api.add_resource(PaddleOfflineOcrView, '/paddleoffline', endpoint='paddleoffline')
api.add_resource(ProductView, '/product', endpoint='product')

# 添加静态文件路由
@app.route('/filesPic/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)