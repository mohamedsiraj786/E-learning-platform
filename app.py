from contextlib import nullcontext
from flask import Flask, jsonify, request, render_template, redirect, url_for,session
import os
from flask_wtf import FlaskForm
import mysql.connector
from tabulate import tabulate
from werkzeug.utils import secure_filename
import secrets
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField
from wtforms.validators import InputRequired
import cloudinary
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.api import resources as cloudinary_resources



conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
cursor = conn.cursor()

# Generate a secret key (32 bytes) as a hexadecimal string
secret_key = secrets.token_hex(32)
# Print the generated secret key
print(secret_key)

# Get the absolute path of the directory containing this script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = '72f6728c9fb135a30f6ff3ca4436333f79b1d2c8e0f15d570e4004770390650f'
# Configure Cloudinary with your credentials
cloudinary.config(
    cloud_name="desfmkg2f",
    api_key="358228458767548",
    api_secret="4P1KuIc7kUjTvCMh1_uvuyB88gg"
)

course_data = []
select_course_data = []

set(course_data)

video_url = ''


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        user_keyword = request.form.get('serach')
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
        cursor = conn.cursor()
        query = "SELECT * FROM courses WHERE course_name LIKE %s"
        cursor.execute(query, ('%' + user_keyword + '%',))
        search_content = list(cursor.fetchall())
        print(search_content, "search")
        video_url = [url[1].replace('static/video\\', '') for url in search_content]
        print(video_url, 'searched_video')
        conn.close()

        # Zip the two lists before passing them to the template
        video_and_content = zip(video_url, search_content)

        return render_template('searched_video.html', video_and_content=video_and_content)

# Rest of your Flask app code...

       
@app.route('/secondpage.html')
def secondpage():
       return render_template('secondpage.html')
       
       

@app.route('/notes.html')
def notes():
      return render_template('notes.html')    
     
@app.route('/play_video/getnotes.html')
def getnote():
      return render_template ('getnotes.html')
  
@app.route('/usergetnotes',methods=["POST"])
def getnotes():
    if 'username' in session:
        username = session.get('username')
        titlename = request.form.get('title')
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
        cursor = conn.cursor()
        query = "SELECT usernotes from usernotes WHERE notestitle = %s AND username = %s"
        cursor.execute(query,(titlename,username))
        result = cursor.fetchone()
        print(result,"usernotesandname")
        conn.close()
        
    if result is not None:
        result_list = list(result)
    else:
       result_list = "There Is No Data Found "
        
    
    return render_template('getnotes.html',data = result_list)
        
        
        
@app.route('/search_result',methods=['POST'])     
def searched_images():
    if request.method == "POST":
      searched_data =  request.form.get('serach')
      conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
      cursor = conn.cursor()
      query = "SELECT * FROM images WHERE program_name like  %s"
      cursor.execute(query,(searched_data,))
      result = cursor.fetchall()
      print(result,"result_image")
      return render_template('searched_images.html',searched_data = result)
        
  
@app.route('/usernotes', methods=['POST'])
def usernotes():
    title = request.form.get('title')
    notes = request.form.get('notes')
    username = session.get("username")
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
    cursor = conn.cursor()
    query = "INSERT INTO usernotes (username,notestitle,usernotes) values (%s ,%s, %s)"  
    data = (username,title,notes)
    cursor.execute(query, data)
    conn.commit()
    conn.close()
    return f"{username}"    
      

@app.route('https://sleepy-sheath-dress-colt.cyclic.app/')
def index():
  
    
    if 'username' in session:
         video_files = [f for f in os.listdir('static/video') if f.endswith('.mp4')]  # Adjust file extension as needed
         print(video_files,"array of video")
         conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
         cursor = conn.cursor()
         course_details = "SELECT * from courses" 
         cursor.execute(course_details)
         details = list(cursor.fetchall())
         print(list(details),"mew")
         filenames = [t[1].replace('static/video\\', '') for t in details]
         
      
         cursor.close()
         print(filenames,"example")
         print(video_url,"example1")
         print(details,"example3")
         return render_template('index.html', details = details, video_name = filenames)
    else:
     return render_template('register.html')
 
@app.route('/index.html')
def home():
  
    
    if 'username' in session:
         video_files = [f for f in os.listdir('static/video') if f.endswith('.mp4')]  # Adjust file extension as needed
         print(video_files,"array of video")
         conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
         cursor = conn.cursor()
         course_details = "SELECT * from courses" 
         cursor.execute(course_details)
         details = list(cursor.fetchall())
         print(list(details),"mew")
         filenames = [t[1].replace('static/video\\', '') for t in details]
         
      
         cursor.close()
         print(filenames,"example")
         print(video_url,"example1")
         print(details,"example3")
         return render_template('index.html', details = details, video_name = filenames)
    else:
     return render_template('register.html')
 
 
@app.route('/quiz_form.html') 
def quiz():
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
    cursor = conn.cursor()
    query = "SELECT id FROM courses"
    cursor.execute(query)
    id_data = cursor.fetchall()
    id_array = [item[0] for item in id_data]
    print(id_array)
    conn.close()
    
    return render_template('quiz_form.html',course_id_data = id_array)

@app.route('/created_quiz', methods=['GET', 'POST'])
def quiz_created():
    if request.method == 'POST':
        # Get form data
        question = request.form['question']
        options = [request.form[f'option{i}'] for i in range(1, 5)]
        answer = request.form['answer']
        course_id = request.form['course_id']

        # Print the values (you can replace this with your desired processing)
        print(f"Question: {question}")
        print(f"Options: {options}")
        print(f"Answer: {answer}")
        print(f"Course ID: {course_id}")
        
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
            cursor = conn.cursor()
            query = "INSERT INTO quiz_questions (question, option_one, option_two, option_three, option_four, answer, course_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (question, options[0], options[1], options[2], options[3], answer, course_id))
            conn.commit()
            print("Data inserted successfully!")
        except Exception as e:
            # Handle the exception, log it, etc.
            print(f"Error: {e}")
        finally:
            # It's good practice to close the cursor and connection in the finally block
            cursor.close()
            conn.close()


    # Render the form template
    return render_template('profile.html')

@app.route('/login')
def login():
    
   if  'username' in session:
       return redirect(url_for('index'))
   return  render_template('login.html')

@app.route('/logout.html')
def logout():
    session.pop('username')
    return render_template('login.html')
    

@app.route('/test.html')
def test():
    return render_template('test.html')

@app.route('/courses.html')
def courses():

    enumerated_data = list(enumerate(zip(course_data, select_course_data)))
    print(enumerated_data,"enumuration")
    return render_template('courses.html', enumerated_data=enumerated_data)

@app.route('/process_form/<int:id>', methods=['POST'])
def process_form(id):
    if request.method == "POST":
        # Handle the POST request here
        return render_template('course_added_loader.html')
    else:
        # Handle GET request (if needed) or redirect to another route
        # You can render a different template or perform other actions for GET requests
        return render_template('profile.html')


    

    # You can also access other form data using request.form
    # For example, if you have form fields like <input type="text" name="field_name">,
    # you can access them using request.form['field_name']
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_responses = request.json  # Assuming the frontend sends a JSON payload with user responses
    # Perform actions with user_responses (e.g., save to database)
    course_id = user_responses.get('c_id')
    responses = user_responses.get('userResponses')
    print(user_responses,"userres")
    print(course_id,"cid")
    print(responses,"response")
    
    list_of_lists = [[d['answer']] for d in responses]
    print(list_of_lists)
    
    correct_answers_count = 0
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
    cursor = conn.cursor()
    
    query = "SELECT answer FROM quiz_questions WHERE course_id = %s"
    cursor.execute(query,(course_id,))
    result = cursor.fetchall()
    print(result,"dbres")
    cursor.close()
    
    
    count = 0

    for i in range(min(len(list_of_lists), len(result))):
        if list_of_lists[i][0] == result[i][0]:
            count += 1
            
    print(count)       

    return jsonify({"message": f"Quiz responses submitted successfully! {count} correct answers"})



@app.route('/videoid/<videoId>/mcq.html')
def question(videoId):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
    cursor = conn.cursor()
    query ="SELECT * FROM quiz_questions WHERE course_id = %s"
    cursor.execute(query,(videoId,))
    result = cursor.fetchall()
    print(result,"questions")
  
        
    return render_template('mcq.html', quiz_data=result)

    
@app.route('/save_notes', methods=['POST'])
def save_notes():
    notes_content = request.form.get('notesContent')
    video_id = request.form.get('videoId')  
    NotesTitle = request.form.get('notesTitle')  
    username = session.get('username')
    print(notes_content,video_id,NotesTitle,"botharesame")
    
    query = "INSERT into usernotes (username,notestitle,usernotes,course_id) values (%s, %s, %s, %s)"
    data = (username,NotesTitle,notes_content,video_id)
    cursor.execute(query,data)
    conn.commit()
    conn.close()
    
    return f"{notes_content} and {video_id}"
    
@app.route('/play_video/<course_id>')
def play_video(course_id):
    query = "SELECT * from courses WHERE id = %s"
    data = (course_id,)
    cursor.execute(query, data)
    result = cursor.fetchone()

    # Check if the result is not None
    if result:
        # Extract relevant information
        video_id, video_path, video_description, video_title = result
        print(video_id,"video_id")

        # Extract filename from the path
        filename = video_path.replace('static/video\\', '')

        # Print or use the filename as needed
        print(filename)

        # You can pass these values to the template
        return render_template('video.html', video_id=video_id, filename=filename, description=video_description, title=video_title)

    else:
        # Handle the case where the course ID is not found
        return render_template('courses.html')


@app.route('/api/update_courses', methods=['POST'])
def update_courses():
    
    data = request.get_json()
    selectedCourses = data.get('selectedCourses')
    print('selected courses', selectedCourses)
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
    cursor = conn.cursor()
    
    for course_id in selectedCourses:
        query = 'SELECT vide_url,course_name,id from courses where id = %s'
        cursor.execute(query, (course_id,))
        res = list(cursor.fetchone())
        select_course_data.append(res)
        print(res,"result ed")
        
        if res:
            url = res[0]
            filename = os.path.basename(url)
            print(filename,"filename")
        if filename  not in course_data:    
            course_data.append(filename)
           
    return render_template('test.html', course_data=course_data)
    
    

    
@app.route('/profile.html')
def profile():
    username = session.get('username')
    return render_template('profile.html',username=username)

@app.route('/admin.html')
def admin():
    return render_template('admin.html')



# Modify the 'feed' route to render the updated template

UPLOAD_FOLDER = 'static/video'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = 'static/img'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ImageUploadForm(FlaskForm):
    image = FileField('Image', validators=[FileRequired(), FileAllowed(ALLOWED_IMAGE_EXTENSIONS, 'Images only!')])
    description = StringField('Description')
    program_name = StringField('program_name')

@app.route('/feed.html', methods=['GET', 'POST'])
def feed():
    return render_template('feed.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])

def upload_image():
    if request.method == 'POST':
        description = request.form.get('description')
        program_name = request.form.get('program_name')
        file_to_upload = request.files['file']
        
        

        if file_to_upload and allowed_file_img(file_to_upload.filename):
            folder = 'user_record'  # Replace with your desired folder name
            result = cloudinary_upload(file_to_upload, folder=folder)
            image_url = result['secure_url']  # Get Cloudinary URL

            # Check if the image URL already exists in the database
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
            cursor = conn.cursor()
            query = "SELECT image_url FROM images WHERE image_url = %s"
            cursor.execute(query, (image_url,))
            existing_url = cursor.fetchone()

            if not existing_url:  # If URL doesn't exist, insert the record
                query = "INSERT INTO images(image_url, image_description, program_name) VALUES (%s, %s, %s)"
                cursor.execute(query, (image_url, description, program_name))
                conn.commit()

            conn.close()
            
            return f"Image uploaded! URL: {image_url}"

        return "Invalid file format or upload failed"






def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload_video', methods=['POST'])
def upload_video():
    print(request.files,"sample data")
    if 'video_file' not in request.files:
        return "No file part"
    
    video_file = request.files['video_file']
    course_name = request.form.get('course_name')  # Get course name from the form
    description = request.form.get('description')  
    
    print(video_file,"sample")

    if video_file.filename == '':
        return "No selected file"

    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
        cursor = conn.cursor()
        query = "INSERT INTO courses(vide_url, description,course_name) VALUES (%s, %s, %s)"
        cursor.execute(query,(video_path, description,course_name))
        conn.commit()
        conn.close()
        video_file.save(video_path)

        # Generate a unique URL for the uploaded video
        video_url = '/static/img/' + filename

        return f'Video uploaded and can be accessed at: <a href="{video_url}">{video_url}</a>'

    return "Invalid file format. Allowed formats are: mp4"

@app.route('/images.html')
def image_gallery():
    # Fetch distinct image details from the database
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
    cursor = conn.cursor()
    query = "SELECT DISTINCT image_url, image_description, program_name FROM images"
    cursor.execute(query)
    image_details = cursor.fetchall()
    conn.close()

    return render_template('images.html', image_details=image_details)      



    


@app.route('/Home', methods=['POST'])
def login_check():
    
    if request.method == "POST":
        user_email = request.form.get('useremail')
        password = request.form.get('password')

        # Connect to the database
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
        cursor = conn.cursor()

        # Query the database for the user with the provided email and password
        query = "SELECT username,email,userpassword FROM users WHERE email = %s AND userpassword = %s"
        data = (user_email, password)
        cursor.execute(query, data)
        result = cursor.fetchone()  # Fetch the first matching user
        print(result,"result")

    
        
        
        # return render_template('index.html', video_files=video_files)

        if result:
             username = result[0] 
             session['username'] = username 
             course_details = "SELECT * from courses" 
             cursor.execute(course_details)
             details = list(cursor.fetchall())
             print(list(details),"new")
             filenames = [t[1].replace('static/video\\', '') for t in details]
             
            
             return render_template('index.html', details = details, video_name = filenames)
        else:
            # Handle incorrect login credentials here, e.g., display an error message
            return render_template('login.html', error="Incorrect email or password")

    else:
        return redirect(url_for('index.html'))

@app.route('/confirm', methods=['POST', 'GET'])
def confirm():
    if request.method == "POST":
        ue = request.form.get('useremail')
        un = request.form.get('username')
        pwd = request.form.get('password')
        
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="jamil")
        cursor = conn.cursor()
        check = "SELECT email FROM users WHERE email = %s"
        cursor.execute(check, (ue,))
        user = cursor.fetchone()
        exist_email = ''
        if user:
            exist_email ="Already Registered"
            return render_template('register.html', exist_email=exist_email)
        else:    
            query = "INSERT INTO users (username, email, userpassword) VALUES (%s, %s, %s)"
            data = (un, ue, pwd)
            cursor.execute(query, data)
            conn.commit()
            cursor.close()
        return render_template('confirm.html', username=un, useremail=ue, password=pwd, exist_email=exist_email)
        
    else:
        return redirect(url_for('index'))

    
    

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
