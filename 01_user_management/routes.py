from flask import render_template, request, redirect, url_for, flash, jsonify
from models import db, User

def register_routes(app):
    # --------------------------
    # HTML routes (browser)
    # --------------------------
    @app.route('/')
    def index():
        users = User.query.all()
        return render_template('index.html', users=users)

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('create.html')

    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):
        user = User.query.get_or_404(id)
        if request.method == 'POST':
            user.name = request.form['name']
            user.email = request.form['email']
            user.password = request.form['password']

            db.session.commit()
            flash('User updated successfully!', 'info')
            return redirect(url_for('index'))

        return render_template('update.html', user=user)

    @app.route('/delete/<int:id>')
    def delete(id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'danger')
        return redirect(url_for('index'))


    # --------------------------
    # API routes (Postman)
    # --------------------------
    @app.route('/api/users', methods=['GET'])
    def api_get_users():
        users = User.query.all()
        users_list = [
            {"id": u.id, "name": u.name, "email": u.email, "joined_on": u.joined_on.strftime('%Y-%m-%d')}
            for u in users
        ]
        return jsonify(users_list)

    @app.route('/api/users/<int:id>', methods=['GET'])
    def api_get_user(id):
        user = User.query.get_or_404(id)
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "joined_on": user.joined_on.strftime('%Y-%m-%d')
        })

    @app.route('/api/users', methods=['POST'])
    def api_create_user():
        data = request.json
        new_user = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201

    @app.route('/api/users/<int:id>', methods=['PUT'])
    def api_update_user(id):
        user = User.query.get_or_404(id)
        data = request.json
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})

    @app.route('/api/users/<int:id>', methods=['DELETE'])
    def api_delete_user(id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
