from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db

bp = Blueprint('main', __name__)

@bp.route('/users')
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@bp.route('/users/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email']
        )
        db.session.add(user)
        try:
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating user. Email might be duplicate.', 'error')
    
    return render_template('users/create.html')

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('Error updating user. Email might be duplicate.', 'error')
    
    return render_template('users/edit.html', user=user)

@bp.route('/users/<int:id>/delete', methods=['POST'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('main.index'))