from flask import render_template, request, redirect, url_for, flash, jsonify
from models import db, Post

def register_routes(app):
    # HTML Routes
    @app.route('/')
    def index():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('index.html', posts=posts)

    @app.route('/create', methods=['GET','POST'])
    def create():
        if request.method == 'POST':
            post = Post(
                title=request.form['title'],
                content=request.form['content'],
                author=request.form['author']
            )
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('create.html')

    @app.route('/edit/<int:id>', methods=['GET','POST'])
    def edit(id):
        post = Post.query.get_or_404(id)
        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            post.author = request.form['author']
            db.session.commit()
            flash('Post updated successfully!', 'info')
            return redirect(url_for('index'))
        return render_template('edit.html', post=post)

    @app.route('/delete/<int:id>')
    def delete(id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'danger')
        return redirect(url_for('index'))

    # API Routes for Postman
    @app.route('/api/posts', methods=['GET'])
    def api_get_posts():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return jsonify([{
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.author,
            "created_at": p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for p in posts])

    @app.route('/api/posts/<int:id>', methods=['GET'])
    def api_get_post(id):
        p = Post.query.get_or_404(id)
        return jsonify({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.author,
            "created_at": p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    @app.route('/api/posts', methods=['POST'])
    def api_create_post():
        data = request.json
        p = Post(title=data['title'], content=data['content'], author=data['author'])
        db.session.add(p)
        db.session.commit()
        return jsonify({"message":"Post created"}),201

    @app.route('/api/posts/<int:id>', methods=['PUT'])
    def api_update_post(id):
        p = Post.query.get_or_404(id)
        data = request.json
        p.title = data.get('title', p.title)
        p.content = data.get('content', p.content)
        p.author = data.get('author', p.author)
        db.session.commit()
        return jsonify({"message":"Post updated"})

    @app.route('/api/posts/<int:id>', methods=['DELETE'])
    def api_delete_post(id):
        p = Post.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return jsonify({"message":"Post deleted"})
