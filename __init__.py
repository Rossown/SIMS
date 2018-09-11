import os
from flask import Flask
from flask import render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_mapping(SECRET_KEY='dev', DATABASE="")

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.congif.from_pyfile('config.py',silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    
    # # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template('index.html')

    return app
   


if __name__ == '__main__':
    app = create_app()
    app.run()