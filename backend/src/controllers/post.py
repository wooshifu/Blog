from app import app
from flask import jsonify

from services import post_service


@app.route('/api/posts')
def posts():
    return jsonify(posts=post_service.all_posts())
