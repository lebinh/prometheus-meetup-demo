.PHONY: server prometheus alertmanager load-light load-heavy

server:
	FLASK_APP=server.py flask run --host 127.0.0.1 --port 8000 --with-threads 2> /dev/null

prometheus:
	prometheus -web.listen-address=127.0.0.1:9090 -alertmanager.url=http://127.0.0.1:9093

alertmanager:
	alertmanager -web.external-url http://127.0.0.1 -web.listen-address 127.0.0.1:9093 -config.file alertmanager.yml

load-light:
	ab -r -n 1000000 -c 1 127.0.0.1:8000/ping

load-heavy:
	ab -r -n 1000000 -c 10 127.0.0.1:8000/ping

clean:
	rm -rf data
