from flask import Flask, render_template,flash,redirect, url_for
import os
import glob
from flask import send_file
from fileinput import filename
from flask import request

import myModule
 
app = Flask(__name__)
app.secret_key = "super secret key"
upload_path='static/uploaded file/'
merge_path='static/merged file/' 
 
# @app.route("/")
# def index():
#     return render_template("layout.html")

    
@app.route("/")
def home():
    return render_template("home.html")
    


@app.route('/load-file',methods=['POST'])
def load_file():
    if request.method == 'POST':
        res=myModule.clearPath(upload_path)   
        if(res!=True):
            return "Error in clearing uploaded file path" 
        res=myModule.clearPath(merge_path)    
        if(res!=True):
            return "Error in clearing uploaded file path" 

        # files = request.files.getlist('file[]')
        files = request.files.getlist('file')
        uploaded_file_names=[]
        extension=['.xlsx']


        for file in files:
            file_name=file.filename   #name
            
            if file_name != '':
                file_extension = myModule.getExtension(file_name)

                if file_extension not in extension:
                    flash('Invalid Extension','bg-danger')
                    return redirect(url_for('home'))
                else:
                    try:
                        file.save(upload_path+file.filename) #uploaded
                        uploaded_file_names.append(file_name)
                    except:
                        flash('Error in file uploading')
                        return redirect(url_for('home'))
            else:
                flash('Invalid File','bg-danger')
                return redirect(url_for('home'))
        
        if(len(uploaded_file_names)):
            new_semester=myModule.mergeUploadedFile(uploaded_file_names)
            new_semester.to_csv(merge_path+"new_semester.csv",index=False)
            flash('System Loaded Successfully','bg-success')
            return redirect(url_for('loaded_file'))



@app.route("/loaded-file")
def loaded_file():
    

    file_path = glob.glob(upload_path+'*')
    file_names=[]
    try:
        for f in file_path:
            file_names.append(f)

        import pandas as pd
        semester=pd.read_csv(merge_path+'new_semester.csv')
        semester=semester.to_dict('records')
        return render_template("loaded_file.html",files=file_names,semester=semester)
    except:
        return render_template("loaded_file.html")


@app.route("/get-gpa")
def get_gpa():
    return render_template("find_gpa.html")

@app.route("/find-attendance",methods=['POST'])
def find_attendance():
    if request.method == 'POST':
        res=myModule.isLoaded()
        if(res!=True):
            flash('System not Loaded','bg-danger')
            return redirect(url_for('home'))

        student_id = request.form['student_id']
        try:
            new_result=myModule.getResult(student_id)
            result=new_result['new_student_result'].to_dict('records')
            gpa=new_result['gpa']
        except:
            flash('The student does not exist','bg-danger')
            return render_template("find_gpa.html",student_id=student_id)

    return render_template("find_gpa.html",result=result,student_id=student_id,gpa=gpa)

@app.route('/demo-download')
def demo_download():
    return send_file(
        'static/demo/demo.xlsx',
        mimetype='text/xlsx',
        download_name='demo.xlsx',
        as_attachment=True
    )
@app.route('/get-semester')
def get_semester():
    import pandas as pd
    semester=pd.read_csv('merged file/new_semester.csv')
    semester=semester.to_dict('records')
    return render_template("loaded_file.html",semester=semester)



@app.route('/reset-system')
def reset_system():
    res=myModule.clearPath(upload_path)   
    if(res!=True):
        return "Error in clearing uploaded file path" 
    res=myModule.clearPath(merge_path)    
    if(res!=True):
        return "Error in clearing uploaded file path" 
    flash('System Reseted Successfully','bg-success')
    return redirect(url_for('loaded_file'))




 


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run()