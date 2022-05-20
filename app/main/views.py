from flask import render_template, redirect,url_for, abort, request
from flask_login import login_required, current_user
from . import main
from .. import db,photos
from .forms import UpdateProfile, CategoryForm, CommentForm, PostForm
from ..models import User, PhotoProfile, Post, Comment, Category, Subscribers, Votes
from ..request import get_quote

@main.route('/')
def index():
    
    all_posts = Post.query.all()
    all_category = Category.get_categories()
    quote = get_quote()
    print(all_posts)
    
    if request.method == "POST":
        new_subscriber = Subscriber(email = request.form.get("subscriber"))
        db.session.add(new_subscriber)
        db.session.commit()
        welcome_message("Thank you for subscribing to the justcode", 
                        "email/welcome", new_subscriber.email)
    
    title = 'Blog Post'
    return render_template('index.html',posts= all_posts, categories = all_category, title=title, quote=quote)

@main.route('/category/new-post/<int:id>',methods = ['GET','POST'])
@login_required
def new_post(id):
    form = PostForm()
    category = Category.query.filter_by(id=id).first()
    
    if category is None:
        abort(404)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post= Post(title=title, content=content, category_id = category.id, user_id = current_user.id)
        new_post.save_post()
        
        subs = Subscribers.query.all()
        for sub in subs:
            notification_message(post_title, 
                            "email/notification", sub.email, new_post = new_post)
            pass
        return redirect(url_for('.category', id=category.id))

    
    return render_template('new_post.html',post_form = form, category = category)

@main.route('/categories/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)

    posts=Post.query.filter_by(id=category.id).all()
    return render_template('category.html', posts=posts, category=category)
    
@main.route('/add/category',methods = ['GET','POST'])
@login_required
def new_category():
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name = name)
        new_category.save_category()

        return redirect(url_for('.index'))

    
    title = 'New Category'
    
    return render_template('new_category.html',title = title, category_form = form)

@main.route('/see-post/<int:id>',methods = ['GET','POST'])
@login_required
def see_post(id):
    
    all_category = Category.get_categories()
    posts = Post.query.get(id)
    
    if posts is None:
        abort(404)
    
    comment = Comment.query.filter_by(id=id)
    count_likes = Votes.query.filter_by(posts_id=id, vote=1).all()
    count_dislikes = Votes.query.filter_by(posts_id=id, vote=2).all()
    return render_template('see_post.html', posts = posts, comment = comment, count_likes=len(count_likes), count_dislikes=len(count_dislikes), category_id = id, categories=all_category)
    

@main.route('/write_comment/<int:id>', methods = ['GET','POST'])
@login_required
def post_comment(id):
    
    form = CommentForm()
    title = 'post comment'
    posts = Post.query.filter_by(id=id).first()
    
    if posts is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comment(opinion = opinion, user_id = current_user.id, post_id = posts.id)
        new_comment.save_comment()
        return redirect(url_for('.see_post', id = posts.id))
    
    return render_template('post_comment.html', title = title, comment_form = form)

@main.route("/post/<int:id>/<int:comment_id>/delete")
def delete_comment(id, comment_id):
    post = Post.query.filter_by(id = id).first()
    comment = Comment.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("main.post", id = post.id))

@main.route('/post/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id,vote_type):
    votes = Votes.query.filter_by(user_id=current_user.id).all()
    print(f'The new vote is {votes}')
    to_str=f'{vote_type}:{current_user.id}:{id}'
    print(f'The current vote is {to_str}')

    if not votes:
        new_vote = Votes(vote=vote_type, user_id=current_user.id, posts_id=id)
        new_vote.save_vote()
        print('YOU HAVE VOTED')

    for vote in votes:
        if f'{vote}' == to_str:
            print('YOU CANNOT VOTE MORE THAN ONCE')
            break
        else:   
            new_vote = Votes(vote=vote_type, user_id=current_user.id, posts_id=id)
            new_vote.save_vote()
            print('YOU HAVE VOTED')
            break
    return redirect(url_for('.see_post', id=id)) 

# profile
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

main.errorhandler(404)
def page_not_found(e):
    return render_template('fourOwfour.html'),404