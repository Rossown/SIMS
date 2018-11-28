import time

import init

def application(env, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    time.sleep(0.1)
    return "Complete"

if __name__ == '__main__':
    for i in range(527):
        server = make_server('', 5000, application)
        print("Serving on port 5000")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass