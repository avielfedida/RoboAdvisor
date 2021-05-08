import json

from werkzeug.datastructures import FileStorage


def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)

        return callHelper

    return repeatHelper


def get_study_in_sample_oos_files():
    in_sample = FileStorage(
        stream=open("demo_in_sample.txt", "rb"),
        filename="demo_in_sample.txt",
        content_type="text/plain",
    )
    oos = FileStorage(
        stream=open("demo_oos.txt", "rb"),
        filename="demo_oos.txt",
        content_type="text/plain",
    )
    return in_sample, oos

def get_alg_report_file():
    return FileStorage(
        stream=open("demo_alg.xlsx", "rb"),
        filename="demo_alg.xlsx",
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

def json_resp(rv):
    return json.loads(rv.data.decode('utf-8').replace("'", "\""))
