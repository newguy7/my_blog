from flask import Flask, render_template
import requests
from datetime import date


app = Flask(__name__)

blog_url = "https://api.npoint.io/e6f33017fd9af4fb3cfb"
blog_response = requests.get(blog_url)
all_posts = blog_response.json()
#print(all_posts)

all_posts_list = []

for post in all_posts:
    
    post_dict = {
        'post_title' : post.get('title'),
        'post_subtitle' : post.get('subtitle'),
        'post_id' : post.get('id'),
        'post_body' : post.get('body'),
        'post_date' : post.get('date'),
        'post_image' : post.get('image'),
        'post_author' : post.get('author')
    }
    
    all_posts_list.append(post_dict)
    
    
    

@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts = all_posts_list)

@app.route("/post/<int:blog_id>")
def get_post(blog_id):
    today = date.today()
    current_year = today.year
    requested_post = None
    for blog_post in all_posts_list:
        
        if blog_post['post_id'] == blog_id:
            requested_post = blog_post    
            print(requested_post['post_image'])
    return render_template("post.html", post=requested_post, image=requested_post['post_image'],year=current_year)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



if __name__ == "__main__":
    app.run(debug=True)