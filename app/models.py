from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    """
    User class that will help in creating users
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    posts = db.relationship("Post", backref="user", lazy = "dynamic")
    comment = db.relationship("Comment", backref="user", lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'



class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))



class Subscriber(db.Model):
    __tablename__ = "subscribers"
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, index = True)

class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,category_id, title, content): 
        self.category_id = category.id
        self.title = title
        self.content = content

    def save_post(self):
        """
        Saves posts
        """
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def get_posts(id):
        posts = Post.query.filter_by(category_id=id).all()
        return posts



class Category(db.Model):
    
    __tablename__ = 'categories'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self,id, name):
        self.id = id
        self.name = name

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = Category.query.all()
        return categories



class Comment(db.Model):
    
    __tablename__ = 'comments'     

    
    id = db.Column(db. Integer, primary_key=True)
    opinion = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
     
    def __init__(self, opinion):
        self.opinion = opinion

    def save_comment(self):
        """
        Save the Comments/comments per post
        """
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def delete_comment(cls, id):
       gone = Comment.query.filter_by(id = id).first()
       db.session.delete(gone)
       db.session.commit()   
        
    @classmethod
    def fetch_comments(self, id):
       comment = Comment.query.order_by(Comment.time_posted.desc()).filter_by(posts_id=id).all()
       return comment

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(post_id=id).all()
        return comments



class Quote:
    """
    Blueprint class for quotes consumed from API
    """
    def __init__(self, a, quote):
        self.author = a
        self.quote = quote

