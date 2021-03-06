from flog.ext import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    comments = db.relationship('Comment', lazy=True)

    def __repr__(self):
        return f'<Post ({self.id}): {self.title[0:50]}>'

    @classmethod
    def testing_create(cls):
        return Post(title='foo', author='bar', body='foo.bar.baz')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey(Post.id, ondelete='cascade'), nullable=False)
    post = db.relationship(Post)

    def __repr__(self):
        return f'<Comment ({self.id}): {self.title[0:50]}>'

    @classmethod
    def testing_create(cls):
        return Comment(title='foo', author='bar', body='baz.bar.foo')
