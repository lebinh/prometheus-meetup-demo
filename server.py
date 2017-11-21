import random
import time

from prometheus_client import Counter, Histogram, generate_latest
from flask import Flask, Response, request, g


app = Flask(__name__)
requests_total = Counter('http_requests_total', 'HTTP response total', ['path', 'code'])
request_duration = Histogram('http_request_duration_seconds', 'Request processing time', ['path', 'code'])


@app.before_request
def before():
    g.start_time = time.time()


@app.after_request
def after(resp):
    duration = time.time() - g.start_time
    request_duration.labels(request.path, resp.status_code).observe(duration)
    requests_total.labels(request.path, resp.status_code).inc()
    return resp


@app.route('/ping')
def ping():
    if random.random() < 0.9:
        # simulate a long tail distribution of response time
        time.sleep(random.lognormvariate(-1.6, 1.6) / 10.0)
        return 'pong\n'
    return Response('oops!\n', status=500)


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain; charset=utf-8')

