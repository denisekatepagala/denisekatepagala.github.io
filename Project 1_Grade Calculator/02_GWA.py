from customtkinter import *
import re, json, os

app = CTk()
app.title("Grade Calculator")
app.geometry("1080x700")
app.configure(fg_color="#F4F2F2")
app.minsize(1100, 400)
app.maxsize(1450, 700)

home_frame = CTkFrame(app)
gwa_frame = CTkFrame(app)
course_frame = CTkFrame(app)

FILE = "grades.json"


#! ===================================== BACKEND =====================================
def show_home():
    home_frame.pack(fill="both", expand=True)
    gwa_frame.pack_forget()
    course_frame.pack_forget()

def show_gwa():
    home_frame.pack_forget()
    gwa_frame.pack(fill="both", expand=True)
    course_frame.pack_forget()

def show_grade():
    home_frame.pack_forget()
    gwa_frame.pack_forget()
    course_frame.pack(fill="both", expand=True)

def create_header(parent, title):
    header = CTkLabel(parent, text = title,                 
                font=('Playfair Display',34,'italic'), 
                text_color = "white", fg_color='#215E61', 
                height=70)
    header.pack(fill="x")

def create_label_frame(parent):
    #* Label Frames
    label_frame = CTkFrame(parent, fg_color = "white", corner_radius=15)
    label_frame.pack(fill="x", padx=25, pady=(20,10))
    return label_frame

def create_middle_frame(parent):
    #* Middle Frame
    content_frame = CTkFrame(parent, fg_color="transparent", width = 1080)
    content_frame.pack(fill="both", expand=True, padx=25, pady=(5,20))

    #* Border Frame
    border_frame = CTkFrame(content_frame, fg_color="#CFCFCF", corner_radius=10)
    border_frame.pack(side="right", fill="both", expand=True)

    #* Side Frame
    side_frame = CTkFrame(content_frame, width=230, fg_color='#215E61', corner_radius = 20)
    side_frame.pack(side="left", fill="y", padx=(0,20))
    side_frame.pack_propagate(False)

    return border_frame, side_frame

def create_sidebar_button(parent, title, command):
    CTkButton(parent, text=title, font=('Roboto', 15),
            width=180, height=40, corner_radius=10, 
            fg_color="#CDE8E5", text_color="#1D2128", 
            command=command).pack(side="top", padx=15, pady=20)

def create_sidebar(parent):
    create_sidebar_button(parent, "🏠 HOME", show_home)
    create_sidebar_button(parent, "🖥 GWA", show_gwa)
    create_sidebar_button(parent, "📃 GRADE", show_grade)

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as file:
            return json.load(file)

    return {"terms" : [], 
            "target": 0.0,
            "grades" : []
            }

def save_data(data):
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_statistics():
    data = load_data()

    target_GWA.configure(text=f"Target GWA: {data['target']}")

    highest = None
    lowest = None
    

    for term in data["terms"]:
        gwa = term.get("gwa")
        if gwa is None:
            continue

        if highest is None or gwa < highest:
            highest = gwa

        if lowest is None or gwa > lowest:
            lowest = gwa

    highest_GWA.configure(text=f"Highest GWA: {highest}")
    lowest_GWA.configure(text=f"Lowest GWA: {lowest}")

def load_terms():
    global term_row

    data = load_data()

    #* FOR ADD_TERM()
    for term in data["terms"]:
        school_yr_str = term["school_year"]
        term_str = term["term"]

        school_yr_text = CTkLabel(home_window_frame, text=school_yr_str, font=("Courier New", 15))
        term_text = CTkLabel(home_window_frame, text=term_str, font=("Courier New", 15))
        view_grade=CTkButton(home_window_frame, text= "View Grade", width=70, height=20,
                            font=("Courier New", 15), command=lambda sy=school_yr_str, t=term_str: view_gwa(sy,t),
                            fg_color="transparent",
                            text_color="black", corner_radius=5,
                            border_width=1, border_color="black")
                                    
        school_yr_text.grid(row=term_row, column=0, padx=20, pady=5)
        term_text.grid(row=term_row, column=1, padx=20, pady=3)
        view_grade.grid(row=term_row, column=2, padx=20, pady=3)

        terms.append({
            "school_year" : school_yr_str, 
            "term": term_str,
            "school_label": school_yr_text,
            "term_label" : term_text,
            "view_grade": view_grade,
            "entries" : [],
            "gwa": None})
        term_row += 1

        terms_saved.configure(text = f"Terms Saved: {term_row-1}")

        choices = []
        for term in data["terms"]:
            choices.append(f"{term['school_year']} | {term['term']}")
        term_dropdown.configure(values = choices)        

def load_courses():
    global current_row
    total_units = 0

    if selected_term is None:
        return

    while entries:
        delete_course()

    current_row = 1

    data = load_data()

    for term in data["terms"]:

        if term["school_year"] == selected_term["school_year"] and \
           term["term"] == selected_term["term"]:

            for entry in term["entries"]:
                total_units += entry["units"]

            for saved_course in term["entries"]:

                course = CTkEntry(gwa_window_frame, width=200,
                                  font=("Courier New",15),
                                  text_color="black")

                units = CTkEntry(gwa_window_frame, width=80,
                                 font=("Courier New",15),
                                 text_color="black")

                grade = CTkEntry(gwa_window_frame, width=80,
                                 font=("Courier New",15),
                                 text_color="black")

                course.grid(row=current_row,column=0,padx=10,pady=10)
                units.grid(row=current_row,column=1,padx=10,pady=10)
                grade.grid(row=current_row,column=2,padx=10,pady=10)

                course.insert(0, saved_course["course"])
                units.insert(0, saved_course["units"])
                grade.insert(0, saved_course["grade"])

                entries.append((course, units, grade))

                current_row += 1

            total_grades_label.configure(
                text=f"GWA: {term['gwa']:.4f}"
                if term["gwa"] is not None
                else "GWA:"
            )

        total_units_label.configure(text=f"Total Units: {total_units}")
        total_courses_label.configure(text=f"Total Courses: {len(term["entries"])}")

def load_grades():
    print("x")            


#! ================================ BACKEND (Home_Frame) ================================
selected_term = None

def view_gwa(school_yr_str, term_str):
    global selected_term

    selected_term = {"school_year": school_yr_str,
                     "term": term_str}

    dropdown_var.set(f"{selected_term['school_year']} | {selected_term['term']}")
    current_term_label.configure(text= f"Current Term: {selected_term['school_year']} | {selected_term['term']}")

    show_gwa()
    load_courses()

terms = []
term_row = 1

def add_term():
    global term_row
    school_yr_str = school_yr_entry.get().replace(" ", "")
    term_str = term_entry.get().upper()
    duplicate = False
  
    if school_yr_str != "" and term_str != "":
        if re.fullmatch(r"\d{4}-\d{4}", school_yr_str) is None:
            error_label.configure(text= "Format must be YYYY-YYYY")
            return

        start_year, end_year = school_yr_str.split("-")
        start_year = int(start_year)
        end_year = int(end_year)

        if start_year < end_year and end_year == start_year+1:
            for saved_terms in terms:
                if saved_terms["school_year"] == school_yr_str and saved_terms["term"] == term_str:
                    duplicate = True
                    break

            if duplicate == True:
                error_label.configure(text = "School Year & Term Existing Already!")          
                    

            else:
                school_yr_text = CTkLabel(home_window_frame, text=school_yr_str, font=("Courier New", 15))
                term_text = CTkLabel(home_window_frame, text=term_str, font=("Courier New", 15))
                view_grade=CTkButton(home_window_frame, text= "View Grade", width=70, height=20,
                                    font=("Courier New", 15), command=lambda sy=school_yr_str, t=term_str: view_gwa(sy,t),
                                    fg_color="transparent",
                                    text_color="black", corner_radius=5,
                                    border_width=1, border_color="black")
                                            
                school_yr_text.grid(row=term_row, column=0, padx=20, pady=5)
                term_text.grid(row=term_row, column=1, padx=20, pady=3)
                view_grade.grid(row=term_row, column=2, padx=20, pady=3)

                terms.append({
                    "school_year" : school_yr_str, 
                    "term": term_str,
                    "school_label": school_yr_text,
                    "term_label" : term_text,
                    "view_grade": view_grade,
                    "entries" : [],
                    "gwa": None})
                term_row += 1
                error_label.configure(text="")

                data = load_data()

                data["terms"].append({
                    "school_year" : school_yr_str,
                    "term": term_str,
                    "entries" : [],
                    "gwa" : None
                })

                choices = []
                for term in data["terms"]:
                    choices.append(f"{term['school_year']} | {term['term']}")
                term_dropdown.configure(values = choices)

                save_data(data)

                terms_saved.configure(text = f"Saved terms: {term_row - 1}")

        else:
            error_label.configure(text="Invalid School Year!")

    school_yr_entry.delete(0, "end")
    term_entry.delete(0, "end")

def delete_term():
    global term_row
    school_yr_str = school_yr_entry.get().replace(" ", "")
    term_str = term_entry.get().upper()

    for saved_terms in terms:
        if saved_terms["school_year"] == school_yr_str and saved_terms["term"] == term_str:
            saved_terms["school_label"].destroy()
            saved_terms["term_label"].destroy()
            saved_terms["view_grade"].destroy()

            terms.remove(saved_terms)           
            term_row -= 1
            terms_saved.configure(text = f"Terms Saved: {term_row-1}")
            error_label.configure(text="")
            break
        else:
            error_label.configure(text = "Term Not Found!")
        
    data = load_data()

    for term in data["terms"]:
        if term["school_year"] == school_yr_str and term["term"] == term_str:
            data["terms"].remove(term)
            break

    save_data(data)
    load_statistics()
    school_yr_entry.delete(0, "end")
    term_entry.delete(0, "end")

def save_target():
    data = load_data()
    data["target"] = float(target_gwa_entry.get())
    target_GWA.configure(text=f"Target GWA: {data['target']}")
    save_data(data)
    target_gwa_entry.delete(0, "end")


#! ================================ BACKEND (GWA_Frame) ================================
entries = []
current_row = 1

def dropdown_selected_term(choices):
    global selected_term

    school_yr, term = choices.split("|")
    selected_term = {"school_year" : school_yr.replace(" ",""), 
                     "term" : term.replace(" ", "")}
    current_term_label.configure(text= f"Current Term: {selected_term['school_year']} | {selected_term['term']}")

    load_courses()
    
def get_selected_term():
    data = load_data()

    for term in data["terms"]:
        if term["school_year"] == selected_term["school_year"] and \
            term["term"] == selected_term["term"]:
                return term
        
    return None

def add_course():
    global current_row

    course = CTkEntry(gwa_window_frame, width = 200, font=('Courier New', 15), 
                      text_color="black")
    units = CTkEntry(gwa_window_frame, width = 80, font=('Courier New', 15), 
                     text_color="black")
    grade = CTkEntry(gwa_window_frame, width = 80, font=('Courier New', 15), 
                     text_color="black")

    course.grid(row=current_row, column=0, padx=10, pady=10)
    units.grid(row=current_row, column=1, padx=10, pady=10)
    grade.grid(row=current_row, column=2, padx=10, pady=10)

    entries.append((course, units, grade))
    current_row += 1

    data = load_data()
    term = get_selected_term()

    term["entries"] = []

    for row in entries:
        term["enrtries"].append({
            "courses": row[0].get(),
            "units": int(row[1].get()),
            "grade": float(row[2].get())
        })
        break
        
    save_data(data)

def delete_course():
    global current_row

    if entries:
        last = entries.pop()

        for widget in last:
            widget.destroy()
        
        current_row -= 1

def compute():
    total_units = 0
    total_grades = 0
    total_weighted_grades = 0
    
    for row in entries:
        units = row[1].get()
        grades = row[2].get()

        if units == "" or grades == "":
            continue

        units = int(units)
        total_units += units 

        grades = float(grades)
        total_grades += grades
        total_weighted_grades += grades * units

    if total_units > 0:
        gwa = float((total_weighted_grades)/ total_units)
    else:
        gwa = 0
        
    data = load_data()

    for term in data["terms"]:
        if term["school_year"] == selected_term["school_year"] and term["term"] == selected_term["term"]:
            term["entries"] = []

            for row in entries:
                if row[1].get() == "" or row[2].get() == "":
                    continue

                term["entries"].append({
                    "course" : row[0].get(),
                    "units" : int(row[1].get()),
                    "grade" : float(row[2].get())
                })

            term["gwa"] = gwa

    total_units_label.configure(text=f"Total Units: {total_units}")
    total_courses_label.configure(text=f"Total Courses: {current_row-1}")
    total_grades_label.configure(text=f"GWA: {gwa:.4f}")  

    save_data(data)
    
#! =============================== BACKEND (Grade_Frame) ===============================

grades = []
component_row = 1

def add_component():
    global component_row

    component_str = component_entry.get().upper()
    percentage_str = percentage_entry.get().strip()
    duplicate = False
    total_percentage = 0

    if component_str == "":
        error_label_grade.configure(text="Enter a component.")
        return

    if percentage_str == "":
        error_label_grade.configure(text="Enter a percentage.")
        return

    if not percentage_str.isdigit():
        error_label_grade.configure(text="Percentage must be a number.")
        return

    percentage = int(percentage_str)

    if percentage < 1 or percentage > 100:
        error_label_grade.configure(text="Percentage must be between 1 and 100.")
        return

    for saved_component in grades:
        if saved_component["component"] == component_str:
            duplicate = True
            break

    if duplicate:
        error_label_grade.configure(text="Component Already Exists.")
        return

    data = load_data()

    for component in data["grades"]:
        total_percentage += component["percentage"]

    total_percentage += percentage

    if total_percentage > 100:
        error_label_grade.configure(text="Total percentage cannot exceed 100%.")
        return

    component_text = CTkLabel(top_left_window_frame, text=component_str,
        font=("Courier New", 15))
    percentage_text = CTkLabel(top_left_window_frame, text=f"{percentage}%",
        font=("Courier New", 15))
    component_text.grid(row=component_row, column=0, padx=20, pady=5)
    percentage_text.grid(row=component_row, column=1, padx=20, pady=5)

    grades.append({
        "component": component_str,
        "percentage": percentage
    })

    data["grades"].append({
        "component": component_str,
        "percentage": percentage
    })

    save_data(data)
    component_row += 1

    component_entry.delete(0, "end")
    percentage_entry.delete(0, "end")
    error_label_grade.configure(text="")

def delete_component():
    print("x")


#! ====================================== FRONTEND ======================================
#* Header
create_header(home_frame, "Homepage")
create_header(gwa_frame, "GWA Calculator" )
create_header(course_frame, "Grade Calculator")

#* Label Frame
home_label_frame = create_label_frame(home_frame)
gwa_label_frame = create_label_frame(gwa_frame)
course_label_frame = create_label_frame(course_frame)

#* Middle Frame
home_border, home_sidebar = create_middle_frame(home_frame)
gwa_border, gwa_sidebar = create_middle_frame(gwa_frame)
course_border, course_sidebar = create_middle_frame(course_frame)

#* Sidebar
create_sidebar(home_sidebar)
create_sidebar(gwa_sidebar)
create_sidebar(course_sidebar)


#! ================================= FRONTEND (Homepage) =================================
#* Labels Statistics
target_GWA = CTkLabel(home_label_frame, text = "Target GWA: None ",
                       font = ('Courier New', 20), text_color = "black",)
target_GWA.pack(side= "left", padx = 45, pady = 15)
highest_GWA = CTkLabel(home_label_frame, text = "Highest GWA: None ",
                       font = ('Courier New', 20), text_color = "black",)
highest_GWA.pack(side= "left", padx = 45, pady = 15)
lowest_GWA = CTkLabel(home_label_frame, text = "Lowest GWA: None ",
                       font = ('Courier New', 20), text_color = "black",)
lowest_GWA.pack(side= "left", padx = 45, pady = 15) 
terms_saved = CTkLabel(home_label_frame, text = "Terms Saved: None ",
                       font = ('Courier New', 20), text_color = "black",)
terms_saved.pack(side= "left", padx = 45, pady = 15) 

#* Content Frame/ Right Pannel
home_window_frame = CTkScrollableFrame(home_border, height=400,
                                       fg_color="#F4F2F2", corner_radius=8)
home_window_frame.pack(side="right", pady=10, padx=(10,20), expand=True, fill="both")

school_yr_label = CTkLabel(home_window_frame, text = "School Year: ", font=('Courier New', 15))
school_yr_label.grid(row=0, column=0, padx=20, pady=10)
term_label = CTkLabel(home_window_frame, text = "Term: ", font=('Courier New', 15))
term_label.grid(row=0, column=1, padx=30, pady=10)

#* Left Pannel
left_pannel_window_frame = CTkFrame(home_border, fg_color="transparent")
left_pannel_window_frame.pack(side="left", padx=(20,10), pady=10)

#* Form Frame
add_term_window_frame = CTkFrame(left_pannel_window_frame, width=250, height=200, 
                                 fg_color="#F4F2F2", corner_radius=8)
add_term_window_frame.pack(fill="both", pady=(0,10))

CTkLabel(add_term_window_frame, text = "School Year: ").pack(pady=(20,5))
school_yr_entry = CTkEntry(add_term_window_frame, width = 150,                      
                           placeholder_text="ex.:2025-2026", placeholder_text_color="grey")
school_yr_entry.pack(pady=10)
CTkLabel(add_term_window_frame, text = "Term: ").pack(pady=10)
term_entry = CTkEntry(add_term_window_frame, width = 150,
                      placeholder_text="ex.: 1T", placeholder_text_color="grey")
term_entry.pack(pady=(10,3))
error_label = CTkLabel(add_term_window_frame, text=" ", text_color="red", font=('Roboto', 11, 'italic'))
error_label.pack()

target_gwa_window_frame = CTkFrame(left_pannel_window_frame, width=250, height = 200,
                                   fg_color = "#F4F2F2", corner_radius=8)
target_gwa_window_frame.pack(fill="both")
target_gwa_window_frame.pack_propagate(False)
CTkLabel(target_gwa_window_frame, text = "Target Highest GWA: ").pack(pady=(20,5))
target_gwa_entry = CTkEntry(target_gwa_window_frame, width = 150, 
                            placeholder_text="ex.: 1.50", placeholder_text_color = "grey")
target_gwa_entry.pack(pady=(5,5))


#* Buttons
CTkButton(add_term_window_frame, text = "Add a term", width=130, height=30,
          fg_color="#1D2128", text_color="#F4F2F2", 
          corner_radius=10, font=('Roboto', 12),
          command=add_term).pack(pady=(20,10))

CTkButton(add_term_window_frame, text = "Delete a term", width=130, height=30,
          fg_color="#1D2128", text_color="#F4F2F2", 
          corner_radius=10, font=('Roboto', 12),
          command=delete_term).pack(pady=10)

CTkButton(target_gwa_window_frame, text = "Save", width=130, height=30,
          fg_color="#1D2128", text_color="#F4F2F2", 
          corner_radius=10, font=('Roboto', 12),
          command=save_target).pack(pady=10)


#! ============================== FRONTEND (GWA_Frame) ==============================
#* Labels Statistics
total_courses_label = CTkLabel(gwa_label_frame, text = "Total Courses: 0",
                    font=('Courier New', 20), text_color = "black")
total_courses_label.pack(side = "left", padx = 40, pady=15)

total_units_label = CTkLabel(gwa_label_frame, text = "Total Units: 0",
                    font=('Courier New', 20), text_color = "black")
total_units_label.pack(side = "left", padx = 40, pady=15)

total_grades_label = CTkLabel(gwa_label_frame, text = "GWA: 0.0000", font=('Courier New', 20))
total_grades_label.pack(side = "left", padx = 40, pady=15)

current_term_label = CTkLabel(gwa_label_frame, text = "Current Term: N/A", font=('Courier New', 20))
current_term_label.pack(side = "left", padx = 40, pady=15)

#* Dropdown
dropdown_var = StringVar(value="Selected Term")

term_dropdown = CTkOptionMenu(gwa_label_frame, values = [], variable = dropdown_var,
                              command = dropdown_selected_term, fg_color = "#1D2128", button_color = "#1D2128")                              
term_dropdown.pack(side = "right", padx=20, pady=15)

#* Content Frame
gwa_window_frame = CTkScrollableFrame(gwa_border, width=450, height=400, 
                                  fg_color="#F4F2F2", corner_radius=8)
gwa_window_frame.pack(padx=3,pady=3, expand=True)
gwa_window_frame.grid_columnconfigure(0, minsize=220)
gwa_window_frame.grid_columnconfigure(1, minsize=100)
gwa_window_frame.grid_columnconfigure(2, minsize=100)

CTkLabel(gwa_window_frame, text = "Course: ", font=('Courier New', 15)).grid(row=0, column=0, padx=10, pady=10)
CTkLabel(gwa_window_frame, text = "Units: ", font=('Courier New', 15)).grid(row=0, column=1, padx=10, pady=10)
CTkLabel(gwa_window_frame, text = "Grade: ", font=('Courier New', 15)).grid(row=0, column=2, padx=10, pady=10)

#* Button Frame
button_frame = CTkFrame(gwa_frame, fg_color="transparent")
button_frame.pack(pady=(5,20))

#* Buttons
CTkButton(button_frame, text = "Add a course", width=160, height=40,
          fg_color="#1D2128", text_color="#F4F2F2", 
          corner_radius=10, font=('Roboto', 15),
          command=add_course).pack(side = "left", padx=10)
CTkButton(button_frame, text = "Delete a course", width=160, height=40, 
          fg_color="#1D2128", text_color="#F4F2F2",
          corner_radius=10, font=('Roboto', 15),
          command=delete_course).pack(side = "left", padx = 10)
CTkButton(button_frame, text = "Compute", width=160, height=40, 
          fg_color="#1D2128", text_color="#F4F2F2",
          corner_radius=10, font=('Roboto', 15),
          command=compute).pack(side = "left", padx=10)


#! ============================ FRONTEND (Grade Calculator) ============================
#* Label Statistics
final_grade = CTkLabel(course_label_frame, text = "Final Grade: ",
                       font = ('Courier New', 20), text_color = "black")
final_grade.pack(side="left", padx = 45, pady = 15)

#* Content Frame/ Right Pannel
grade_right_window_frame = CTkFrame(course_border, height = 300,
                              fg_color = "#F4F2F2", corner_radius = 8)
grade_right_window_frame.pack(side = "right", pady=10, padx=(5,10), expand = True, fill="both")

#* Content Frame/ Left Pannel
grade_left_window_frame = CTkFrame(course_border, height = 300, 
                                   fg_color = "transparent", corner_radius = 8)
grade_left_window_frame. pack(side = "left", padx = (10,5), pady = 10, expand = True, fill = "both")
top_left_window_frame = CTkFrame(grade_left_window_frame, fg_color="#F4F2F2")
top_left_window_frame.pack(side="top", pady=10, padx=(10,5), fill="both", expand=True)
bottom_left_window_frame = CTkFrame(grade_left_window_frame, fg_color="#F4F2F2")
bottom_left_window_frame.pack(side="bottom", pady=10, padx=(10,5), fill="both")

#* Content/ Right Pannel


#* Content/ Left Pannel
CTkLabel(top_left_window_frame, text = "COMPONENT", font = ('courier new',15)).grid(row=0, column=0, padx=20, pady=10)
CTkLabel(top_left_window_frame, text = "PERCENTAGE", font = ('courier new',15)).grid(row=0, column=1, padx=20, pady=10)

CTkLabel(bottom_left_window_frame, text = "Component").grid(row=0,column=0, padx=10, pady=(20,10))
component_entry = CTkEntry(bottom_left_window_frame, placeholder_text = "ex.: Quiz",
                           width = 150, placeholder_text_color = "grey")
component_entry.grid(row=0,column=1, padx=10, pady=(20,10))
CTkLabel(bottom_left_window_frame, text = "Percentage").grid(row=1,column=0, padx=10, pady=(20,10))
percentage_entry = CTkEntry(bottom_left_window_frame, placeholder_text = "ex.: 10",
                           width = 150, placeholder_text_color = "grey")
percentage_entry.grid(row=1,column=1, padx=10, pady=(20,10))
error_label_grade = CTkLabel(bottom_left_window_frame, text=" ", text_color="red", font=('Roboto', 11, 'italic'))
error_label_grade.grid(row=2, column = 0, columnspan=2, padx = 10)

#* Buttons
CTkButton(bottom_left_window_frame, text = "Add a Component", width = 130, 
          fg_color = "#1D2128", text_color="#F4F2F2",
          corner_radius=10, font=('Roboto', 12),
          command=add_component).grid(row=3,column=0, padx=20, pady=10)
CTkButton(bottom_left_window_frame, text = "Delete a Component", width = 130, 
          fg_color = "#1D2128", text_color="#F4F2F2",
          corner_radius=10, font=('Roboto', 12),
          command=add_component).grid(row=3, column=1, padx=10, pady=10)


CTkButton(grade_right_window_frame, text = "➕ Add", width = 130, 
          fg_color = "#1D2128", text_color="#F4F2F2",
          corner_radius=10, font=('Roboto', 12),
          command=add_component).grid(row=0,column=0, padx=10, pady=10)
CTkButton(grade_right_window_frame, text = "➖ Delete", width = 130, 
          fg_color = "#1D2128", text_color="#F4F2F2",
          corner_radius=10, font=('Roboto', 12),
          command=add_component).grid(row=0, column=1, padx=10, pady=10)

#! =====================================================================================
load_terms()
load_statistics()
load_courses()
home_frame.pack(fill="both", expand=True)
app.mainloop()


