from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
	allPost = Post.query.all()
	allPost.reverse()
	return render_template('home.html', user=current_user, allPost=allPost)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if request.method == 'POST':
		title = request.form.get('title')
		desc = request.form.get('desc')

		if len(title) < 2:
			flash('Post is too short!', category='error')

		if len(desc) < 2:
			flash('Post is too short!', category='error')

		else:
			new_post = Post(title=title, data=desc, username=current_user.first_name, user_id=current_user.id)
			db.session.add(new_post)
			db.session.commit()
			flash('Post created!', category='success')


	return render_template('profile.html', user=current_user)


@views.route('/delete-post', methods=['POST'])
def delete_post():
	post = json.loads(request.data)
	postId = post['postId']
	post = Post.query.get(postId)
	if post:
		if post.user_id == current_user.id:
			db.session.delete(post)
			db.session.commit()

	return jsonify({})


@views.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
	post = Post.query.filter_by(id=post_id).first_or_404()
	if action == 'like':
		current_user.like_post(post)
		db.session.commit()
	if action == 'unlike':
		current_user.unlike_post(post)
		db.session.commit()
		
	return redirect(request.referrer)
