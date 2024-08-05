from flask_restful import Resource, reqparse

class ProductView(Resource):
    @staticmethod
    def post():
        parse = reqparse.RequestParser()
        parse.add_argument('product_id', type=str, help='商品id必传', required=True, trim=True)
        args = parse.parse_args()
        product_id = args.product_id
        return {
            'msg': '商品id是' + product_id,
            'code': 200
        }

    @staticmethod
    def get():
        return {
            'msg': '商品',
            'code': 200
        }