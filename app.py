from flask import Flask, send_file
from apscheduler.schedulers.background import BackgroundScheduler
import time
from feed_edits import freepressokc_feededit
from feed_edits import nondoc_feededit
from feed_edits import okenergytoday_feededit
from feed_edits import oudaily_feededit

# Flask app to serve the RSS feeds
app = Flask(__name__)

# Scheduler to periodically update the RSS feeds
scheduler = BackgroundScheduler()

# Function to update the RSS feeds
def update_feeds():
    print("Updating feeds at", time.strftime("%Y-%m-%d %H:%M:%S"))
    freepressokc_feededit.update_feed()
    nondoc_feededit.update_feed()
    okenergytoday_feededit.update_feed()
    oudaily_feededit.update_feed()

# Initial feed update
update_feeds()

# Schedule periodic updates every 20 minutes
scheduler.add_job(func=update_feeds, trigger="interval", hours=2)
scheduler.start()

# Routes to serve the RSS feeds
@app.route('/new_freepressokc.rss')
def serve_freepressokc():
    return send_file('static/new_freepressokc.rss', mimetype='application/rss+xml')

@app.route('/new_nondoc.rss')
def serve_nondoc():
    return send_file('static/new_nondoc.rss', mimetype='application/rss+xml')

@app.route('/new_okenergytoday.rss')
def serve_okenergytoday():
    return send_file('static/new_okenergytoday.rss', mimetype='application/rss+xml')

@app.route('/new_oudaily.rss')
def serve_oudaily():
    return send_file('static/new_oudaily.rss', mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
