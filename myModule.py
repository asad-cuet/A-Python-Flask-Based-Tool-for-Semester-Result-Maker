import pandas as pd
import os
import glob
global upload_path
global merge_path
upload_path='static/uploaded file/'
merge_path='static/merged file/'

def getCourseDetails(data):
    
    #course details
    course_code=data.columns[1]
    course_title=data[course_code][0]
    course_credit=data[course_code][1]
    
    #just taking grade
    just_grade_column=list(data.loc[2])[1:]
    
    #removing above course details
    grades=data.loc[3:].copy()
    
    #taking only student id
    just_id_values=grades['Course_code'].values
    
    #taking just attendace values
    just_grades_values=grades.loc[:, grades.columns != 'Course_code'].values
    
    # Create data frame of id index, class column, attandance data
    index=just_id_values
    columns=just_grade_column
    data_set =  just_grades_values

    # Creates pandas DataFrame.
    dataframe = pd.DataFrame(data_set,index,columns)
    
    #reurn all these thing
    return {
        'Course_Title':course_title,
        'Course_Code':course_code,
        'Credit':course_credit,
        'attendance_frame':dataframe
    }



def createSemester():
    _columns=['Cource_Title','Cource_Code','Credit']
    semester_dataframe=pd.DataFrame(columns=_columns)
    return semester_dataframe



def insertToSemester(details):     
    global new_semester
    # Creating the new row 
    data = [                
            {'Cource_Title': details['Course_Title'],
             'Cource_Code': details['Course_Code'],
             'Credit': details['Credit']
            }
           ]  
    new_row = pd.DataFrame(data)
    
    # for appending new_row at the end of semester_dataframe
    new_semester = new_semester.append(new_row, ignore_index = True) 




def mergeUploadedFile(all_uploaded_file):
    global new_semester
    new_semester=createSemester()
    for uploaded_file in all_uploaded_file:
        dataset=pd.read_excel(upload_path+uploaded_file)
        #getting course information and attendance sheet
        details=getCourseDetails(dataset)
        
        #saving the attendance sheet as csv file
        details['attendance_frame'].to_csv(merge_path+details['Course_Code']+".csv")
        
        #inserting course information new semester dataframe
        insertToSemester(details)
    return new_semester



def newStudentResult():
    columns=['Course Title','Course Code','Credit','Grade','Grade Point']

    new_student_result = pd.DataFrame(columns=columns)

    return new_student_result


def getGPA(credit,grade):
    import numpy as np
    
    total_earned_credit=np.matmul(credit,grade)
    total_credit=np.sum(credit)
    
    gpa=total_earned_credit/total_credit
    gpa=round(gpa,3)
    
    return gpa

def getResult(student_id):
    
    #reading new semester dataframe which is saved as csv file
    new_semester=pd.read_csv(merge_path+"new_semester.csv")
    
    #taking all course cose as list
    cource_code=list(new_semester['Cource_Code'])
    
    #create new attendance dataframe
    new_student_result=newStudentResult()

    for code in cource_code:
        
        #taking attendance dataframe of this coutce code
        cource_item_df=pd.read_csv(merge_path+code+".csv",index_col=0)

        #calculating total class, present, absent
        total_class=len(cource_item_df.columns)
        grade=cource_item_df.loc[int(student_id)]['Grade']
        grade_point=cource_item_df.loc[int(student_id)]['Grade Point']

        #taking course title and credit
        course_title=new_semester[new_semester.Cource_Code==code]['Cource_Title'].values[0]
        credit=new_semester[new_semester.Cource_Code==code]['Credit'].values[0]

        #creating new row of above data
        row_data = [              
                {'Course Title': course_title,'Course Code': code,'Credit':credit,'Grade': grade,'Grade Point': grade_point}
               ]  
        new_row = pd.DataFrame(row_data)

        #appending in new_student_result
        new_student_result = new_student_result.append(new_row, ignore_index = True)
    

    gpa=getGPA(list(new_student_result['Credit']),list(new_student_result['Grade Point']))


    
    return {
        'new_student_result':new_student_result,
        'gpa':gpa
    }



def clearPath(path):
    file_path = glob.glob(path+'*')
    if(len(file_path)):
        try:
            for f in file_path:
                os.remove(f)
            return True
        except:
            return False
    return True
    


def getExtension(name):
    return os.path.splitext(name)[1]


def isLoaded():
    path = './static/merged file/new_semester.csv'
    isExist = os.path.exists(path)
    
    if(isExist):
        return True
    else:
        return False