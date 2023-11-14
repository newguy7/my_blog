from flask import Flask, render_template, request
import requests
import smtplib
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

password = os.environ.get('APP_PASSWORD')
to_email = os.environ.get('TO_EMAIL')

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
    
# ----------------------------- SEND EMAIL -----------------------------------#
def send_email(name,email,phone_number,message):
    message=f"Name: {name}\nEmail: {email}\nPhone: {phone_number}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        # to secure our email connection
        connection.starttls()

        # log in to the email provider
        connection.login(user=to_email, password=password)
        connection.sendmail(
            # from_addr=request.form['email'], 
            from_addr=to_email,
            to_addrs=to_email,
            msg=f"Subject:Blog Message\n\n{message}")    
    

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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form        
        name = data['name']
        email = data['email']
        phone_number = data['phone']
        message = data['message']
        print(name)
        print(email)
        print(phone_number)
        print(message)
        send_email(name,email,phone_number,message)
        return render_template("contact.html",confirm_message="Successfully sent message")
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)