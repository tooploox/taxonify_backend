import time

from flask_restful import Resource


class Export(Resource):
    def get(self):
        time.sleep(3)
        return dict(url='https://sample-videos.com/csv/Sample-Spreadsheet-100-rows.csv')
