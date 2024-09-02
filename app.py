from flask import Flask, send_file
from apscheduler.schedulers.background import BackgroundScheduler
import time
from feed_edits import freepressokc_feededit
# from feed_edits import ksbiupdates_feededit

app = Flask(__name__)

# Scheduler to periodically update the RSS feeds
scheduler = BackgroundScheduler()

def update_feeds():
    print("Updating feeds at", time.strftime("%Y-%m-%d %H:%M:%S"))
    freepressokc_feededit.update_feed()
    # ksbiupdates_feededit.update_feed()

update_feeds()
scheduler.add_job(func=update_feeds, trigger="interval", minutes=20)
scheduler.start()

# Routes to serve the RSS feeds
@app.route('/rss/freepressokc')
def serve_freepressokc():
    return send_file('static/new_freepressokc.rss', mimetype='application/rss+xml')

# @app.route('/rss/ksbiupdates')
# def serve_ksbiupdates():
#     return send_file('static/new_ksbiupdates.rss', mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
