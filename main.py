import sqlite3
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import wheatherAPI


from sensors import *

global root

with open('credentials.txt', 'r') as file:
    lines = file.readlines()
    admin_user = lines[0].strip()
    admin_pass = lines[1].strip()


photos = [] # List where photos will be stored to avoid garbage collection

class Vase(tk.Frame):
        def __init__(self, parent, vase_name, plant="Empty", **kwargs):
            super().__init__(parent, **kwargs)
            self.name = vase_name
            self.plant = plant
            self.humidity_data = humidity_sensor()
            self.humidity = self.humidity_data.humidity[-30]
            self.sunlight_data = sunlight_sensor()
            self.sunlight = self.sunlight_data.sunlight[-30]
            self.salinity_data = salinity_sensor()
            self.salinity = round(self.salinity_data.salinity[-30],3)
            self.ph_data = ph_sensor()
            self.ph = self.ph_data.ph[-30]
            self.bind("<Button-1>", self.on_click_frame)
            self.configure(height=430, width=300, bg="#557b83")
            

            def add_plant_click():
                def file_dialog():
                    global file_path
                    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
                    print("Selected file:", file_path)
                
                print(f"adding plant in vase {self.name}")     
                     
                add_plant_win = tk.Toplevel()
                add_plant_win.geometry("250x450")
                heading = tk.Label(add_plant_win,text="Adding plant",font=("Arial",15))
                heading.grid(row=0,column=1)
                name = tk.Label(add_plant_win,text="Name",pady=20)
                name.grid(row=1,column=0)
                photo = tk.Label(add_plant_win,text="Photo:",pady=20)
                photo.grid(row=2,column=0)
                humidity = tk.Label(add_plant_win,text="Humidity",pady=20)
                humidity.grid(row=3,column=0)
                sunlight = tk.Label(add_plant_win,text="Sunlight",pady=20)
                sunlight.grid(row=4,column=0)
                sustrate = tk.Label(add_plant_win,text="Substrate",pady=20)
                sustrate.grid(row=5,column=0)
                location = tk.Label(add_plant_win,text="Location",pady=20)
                location.grid(row=6,column=0)

                name_entry = tk.Entry(add_plant_win)
                name_entry.grid(row=1,column=1)
                photo_button = tk.Button(add_plant_win,text="Browse..",command=file_dialog)
                photo_button.grid(row=2,column=1)
                humidity_entry = tk.Entry(add_plant_win)
                humidity_entry.grid(row=3,column=1)
                sunlight_entry = tk.Entry(add_plant_win)
                sunlight_entry.grid(row=4,column=1)
                sustrate_entry = tk.Entry(add_plant_win)
                sustrate_entry.grid(row=5,column=1)
                location_entry = tk.Entry(add_plant_win)
                location_entry.grid(row=6,column=1)
                
                
                
                def save_plant_click(location_entry):
                    global root
                    conn = sqlite3.connect("plants.db")
                    c = conn.cursor()
                    c.execute(
                                '''INSERT INTO plants (picture, name, vase_name, sunlight_amount, soil_humidity, substrate_recommendation, location)
                                VALUES (?, ?, ?, ?, ?, ?,?)''',
                            (file_path,name_entry.get(),self.name,sunlight_entry.get(),humidity_entry.get(),sustrate_entry.get(),location_entry.get()))
                    conn.commit()
                    conn.close()

                    self.name = location_entry.get()
                    print(f"lokacija {self.name}")
                    
                    print("created a plant and added it to a database")
                    add_plant_win.destroy()

                    root.destroy()
                    root = tk.Tk()
                    root.geometry("1600x950")
                    vase_list(root)


                add_button = tk.Button(add_plant_win,height=2,text="Add plant",bg="#557b83",fg="white",width=60, command=lambda: save_plant_click(location_entry),font=("Ink Free", 15))
                add_button.grid(row=7,column=0)
                add_button.grid(columnspan=3)

                add_plant_win.grid_columnconfigure(0,weight=1)
                add_plant_win.grid_columnconfigure(1,weight=1)




            self.button_add = tk.Button(self,text="add a plant to a vase",command=add_plant_click)


            def delete_plant_click():
                    global root
                    conn = sqlite3.connect("plants.db")
                    c = conn.cursor()
                    c.execute(f"DELETE FROM plants WHERE vase_name = '{self.name}'")
                    conn.commit()
                    conn.close()

                    print(f"lokacija {self.name}")
                    
                    print("deleted a plant from database")
                    root.destroy()
                    root = tk.Tk()
                    root.geometry("1600x950")
                    vase_list(root)

            def edit_plant_click():
                def file_dialog():
                    global file_path
                    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
                    print("Selected file:", file_path)
                
                print(f"editing plant in vase {self.name}")     
                     
                edit_plant_win = tk.Toplevel()
                edit_plant_win.geometry("300x550")
                heading = tk.Label(edit_plant_win,text="Editing a plant",font=("Ink Free", 20))
                heading.grid(row=0,column=0)
                name = tk.Label(edit_plant_win,text="Name",pady=20,font=("Ink Free", 15))
                name.grid(row=1,column=0)
                photo = tk.Label(edit_plant_win,text="Photo:",pady=20,font=("Ink Free", 15))
                photo.grid(row=2,column=0)
                humidity = tk.Label(edit_plant_win,text="Humidity",pady=20,font=("Ink Free", 15))
                humidity.grid(row=3,column=0)
                sunlight = tk.Label(edit_plant_win,text="Sunlight",pady=20,font=("Ink Free", 15))
                sunlight.grid(row=4,column=0)
                sustrate = tk.Label(edit_plant_win,text="Substrate",pady=20,font=("Ink Free", 15))
                sustrate.grid(row=5,column=0)

                name_entry = tk.Entry(edit_plant_win)
                name_entry.insert(0,self.plant.name)
                name_entry.grid(row=1,column=1)
                photo_button = tk.Button(edit_plant_win,text="Browse..",command=file_dialog)
                photo_button.grid(row=2,column=1)
                humidity_entry = tk.Entry(edit_plant_win)
                humidity_entry.insert(0,self.plant.humidity)
                humidity_entry.grid(row=3,column=1)
                sunlight_entry = tk.Entry(edit_plant_win)
                sunlight_entry.insert(0,self.plant.sunlight)
                sunlight_entry.grid(row=4,column=1)
                substrate_entry = tk.Entry(edit_plant_win)
                substrate_entry.grid(row=5,column=1)
                substrate_entry.insert(0,self.plant.substrate)

                location = tk.Label(edit_plant_win,text="Location",pady=20,font=("Ink Free", 15))
                location.grid(row=6,column=0)
                location_entry = tk.Entry(edit_plant_win)
                location_entry.grid(row=6,column=1)
                location_entry.insert(0,f"{self.plant.location}")
                
                
                
                
                def save_edited_plant_click(location_entry):
                    global root
                    conn = sqlite3.connect("plants.db")
                    c = conn.cursor()
                    c.execute(
                                f'''UPDATE plants 
                                    SET name = "{name_entry.get()}",
                                    picture = "{file_path}",
                                    vase_name = "{self.name}",
                                    soil_humidity = "{humidity_entry.get()}",
                                    sunlight_amount = "{sunlight_entry.get()}",
                                    substrate_recommendation = "{substrate_entry.get()}",
                                    location = "{location_entry.get()}"
                                    WHERE vase_name = "{self.name}"''')
                    print(f"{self.name}")
                    conn.commit()
                    conn.close()

                    self.name = location_entry.get()
                    print(f"lokacija {self.name}")
                    
                    print("edited a plant in database")
                    edit_plant_win.destroy()

                    root.destroy()
                    root = tk.Tk()
                    root.geometry("1600x950")
                    vase_list(root)            

                edit_button = tk.Button(edit_plant_win,height=2,text="Edit plant",bg="#557b83",fg="white",width=60, command=lambda: save_edited_plant_click(location_entry),font=("Ink Free", 15))
                edit_button.grid(row=7,column=0)
                edit_button.grid(columnspan=3)

                edit_plant_win.grid_columnconfigure(0,weight=1)
                edit_plant_win.grid_columnconfigure(1,weight=1)


            self.button_delete = tk.Button(self,text="Delete a plant from vase",command=delete_plant_click)
            self.button_edit = tk.Button(self,text="Edit a plant",command=edit_plant_click)
            

            

                
        
        def on_click_frame(self,event):
            print(f"{self.name} was clicked!")

            if self.plant == "Empty":
                pass
            else:
                more_info = tk.Toplevel()
                more_info.configure(bg="#557b83")
                more_info.geometry("575x950")
                heading = tk.Label(more_info,text="Information about a plant",font=("Ink Free", 20),bg="#557b83")
                heading.grid(row=0,column=0)
                name = tk.Label(more_info,text=f"Name:\t{self.plant.name}",pady=20,font=("Ink Free", 25),bg="#557b83")
                name.grid(row=1,column=0)
                photo = tk.Label(more_info,text="Photo: ",pady=20,font=("Ink Free", 15),bg="#557b83")
                photo.grid(row=2,column=0)

                plant_picture = Image.open(self.plant.photo)
                plant_picture = plant_picture.resize((200,200),Image.ANTIALIAS)

                plant_photo = ImageTk.PhotoImage(plant_picture)
                photos.append(plant_photo)
                label_photo = tk.Label(more_info, image=plant_photo)
                label_photo.grid(row=3,column=0)
                

                curr_humidity = tk.Label(more_info,text=f"Current humidity:\t{self.humidity}%",pady=20,font=("Ink Free", 15),bg="#557b83")
                curr_humidity.grid(row=4,column=0)
                curr_sunlight = tk.Label(more_info,text=f"Current sunlight:\t {self.sunlight} lm",pady=20,font=("Ink Free", 15),bg="#557b83")
                curr_sunlight.grid(row=5,column=0)
                curr_salinity = tk.Label(more_info,text=f"Current salinity:\t{self.salinity}",pady=20,font=("Ink Free", 15),bg="#557b83")
                curr_salinity.grid(row=6,column=0)
                curr_ph = tk.Label(more_info,text=f"Current Ph:\t{self.ph}",pady=20,font=("Ink Free", 15),bg="#557b83")
                curr_ph.grid(row=7,column=0)
                recom_substrate = tk.Label(more_info,text=f"Recomended substrate:\t{self.plant.substrate}",pady=20,font=("Ink Free", 15),bg="#557b83")
                recom_substrate.grid(row=8,column=0)

                req_humidity = tk.Label(more_info,text=f"Required humidity:\t{self.plant.humidity}%",pady=20,font=("Ink Free", 15),bg="#557b83")
                req_humidity.grid(row=4,column=1)
                req_sunlight = tk.Label(more_info,text=f"Required sunlight:\t {self.plant.sunlight} lm",pady=20,font=("Ink Free", 15),bg="#557b83")
                req_sunlight.grid(row=5,column=1)
                req_salinity = tk.Label(more_info,text=f"Required salinity:\t{self.plant.salinity}",pady=20,font=("Ink Free", 15),bg="#557b83")
                req_salinity.grid(row=6,column=1)
                req_ph = tk.Label(more_info,text=f"Required Ph:\t{self.plant.ph}",pady=20,font=("Ink Free", 15),bg="#557b83")
                req_ph.grid(row=7,column=1)

                button_graph_humidity = tk.Button(more_info,text="show humidity history graph",command=lambda:self.humidity_data.plot_line(int(self.plant.humidity)),font=("Ink Free", 15))
                button_graph_humidity.grid(row=9,column=0,pady=10)

                button_graph_sunlight = tk.Button(more_info,text="show sunlight history graph",command=lambda:self.sunlight_data.plot_line(int(self.plant.sunlight)),font=("Ink Free", 15))
                button_graph_sunlight.grid(row=10,column=0,pady=10)

                button_graph_salinity = tk.Button(more_info,text="show salinity history graph",command=lambda:self.salinity_data.plot_line(float(self.plant.salinity)),font=("Ink Free", 15))
                button_graph_salinity.grid(row=11,column=0,pady=10)                



             
          
class Plant:
    def __init__(self,plant_name,photo_path,needed_humidity,needed_light,substrate_recom,location,salinity,ph):
        self.id = 0
        self.name = plant_name
        self.photo = photo_path
        self.humidity = needed_humidity
        self.sunlight = needed_light
        self.substrate = substrate_recom
        self.location = location
        self.salinity = salinity
        self.ph = ph

def database():
  conn = sqlite3.connect('plants.db')  # create a connection to the database
  c = conn.cursor()
  print("conencting to database..")
  # create a table to store the plant data
  c.execute('''CREATE TABLE IF NOT EXISTS plants
                    (id INTEGER PRIMARY KEY,
                    name TEXT,
                    picture TEXT,
                    vase_name TEXT,
                    soil_humidity TEXT,
                    sunlight_amount TEXT,
                    substrate_recommendation TEXT,
                    location TEXT,
                    salinity TEXT,
                    ph TEXT)''')

  print("creatinng database...")
  
  c.execute("SELECT count(*) FROM plants")
  result = c.fetchone()
  
  if result[0] == 0:
    c.execute(
      '''INSERT INTO plants ( vase_name, name, picture, soil_humidity, sunlight_amount, substrate_recommendation, location, salinity,ph)
                    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)''',
              ("Vase 1", "orhideja", "pictures\\orhideja.jpg",  30, 20, 20,"kitchen",0.02,8))
  print("insreting a plant into database")
  conn.commit()
  conn.close()


def sign_in_screen(root):
    print("sign_in_screen_funkcija")
    global username_input
    global password_input
    global resume
    resume = tk.StringVar()
    
    clear_screen(root)
    prijava_label = tk.Label(root,
                            text="Prijava",
                            font=("Ink Free", 30),
                            foreground="#557b83")
    prijava_label.grid(row=0,column=0)
    prijava_label.grid(columnspan=2,pady=20)
    username_label = tk.Label(root,
                                text="username:",
                                font=("Ink Free", 20),
                                foreground="#557b83")
    username_label.grid(row=1,column=0,padx=10)

    password_label = tk.Label(root,
                                text="password:",
                                font=("Ink Free", 20),
                                foreground="#557b83")
    password_label.grid(row=2,column=0,padx=10)

    username_input = tk.Entry(root, width=20)
    password_input = tk.Entry(root, width=20, show="*")
    username_input.grid(row=1,column=1,padx=10)
    password_input.grid(row=2,column=1,padx=10)


    sign_in_button = tk.Button(root,
                                text="SIGN IN",
                                font=("Ink Free", 20),
                                command=lambda: SignInTry(root))
    
    change_login_data_button = tk.Button(root,
                                    text="CHANGE LOGIN DATA",
                                    font=("Ink Free", 20),
                                    command=ChangeLoginData)
    sign_in_button.grid(row=3,column=0)
    sign_in_button.grid(columnspan=2,pady=20)

    change_login_data_button.grid(row=4,column=0)
    change_login_data_button.grid(columnspan=2,pady=20)

    root.wait_variable(resume)
  
def ChangeLoginData():
    global admin_pass
    global admin_user

    if username_input.get() == admin_user and password_input.get() == admin_pass:
        win_change = tk.Toplevel()
        prijava_label = tk.Label(win_change,
                                text="Change Login \n credentials",
                                font=("Ink Free", 30),
                                foreground="#557b83")
        prijava_label.grid(row=0,column=0)
        prijava_label.grid(columnspan=2,pady=20)
        username_label = tk.Label(win_change,
                                    text="username:",
                                    font=("Ink Free", 20),
                                    foreground="#557b83")
        username_label.grid(row=1,column=0,padx=10)

        password_label = tk.Label(win_change,
                                    text="password:",
                                    font=("Ink Free", 20),
                                    foreground="#557b83")
        password_label.grid(row=2,column=0,padx=10)

        username_change_input = tk.Entry(win_change, width=20)
        password_change_input = tk.Entry(win_change, width=20, show="*")
        username_change_input.grid(row=1,column=1,padx=10)
        password_change_input.grid(row=2,column=1,padx=10)


        sign_in_button = tk.Button(win_change,
                                    text="CHANGE",
                                    font=("Ink Free", 20),
                                    command=lambda: change(win_change))
        
        sign_in_button.grid(row=3,column=0)
        sign_in_button.grid(columnspan=2,pady=20)
    else:
        username_input.delete(0,"end")
        password_input.delete(0,"end")
        try_again_label = tk.Label(root,
                                text="You must enter\ncorrect login\ncredentials\nto be allowed\nto change them",
                                bg="#557b83",
                                font=("Ink Free", 20),
                                foreground="#e5efc1")
        try_again_label.place(x=62, y=170)
        root.after(3000, lambda: try_again_label.destroy())

    def change(win):
        global admin_user
        global admin_pass
        if (len(username_change_input.get()) > 0) and (len(password_change_input.get()) > 0):
            admin_user = username_change_input.get()
            admin_pass = password_change_input.get()
            
            with open('credentials.txt', 'w') as file:
                file.write(admin_user + '\n')
                file.write(admin_pass + '\n')
            
            username_input.delete(0,"end")
            password_input.delete(0,"end")
            win.destroy()

            
        else:
            empty_war = tk.Label(win,
                                text="You need to fill in all the data",
                                font=("Ink Free", 20),
                                foreground="#557b83")
            empty_war.grid(row=4,column=0)
            win.after(2000, lambda: empty_war.destroy())
    
    
def SignInTry(root):

    print("SignInTry_funkcija")
    if username_input.get() == admin_user and password_input.get() == admin_pass:
        print(username_input.get(), password_input.get())
        clear_screen(root)
        resume.set(1)
    else:
        username_input.delete(0,"end")
        password_input.delete(0,"end")
        try_again_label = tk.Label(root,
                                text="Try again",
                                bg="#557b83",
                                font=("Ink Free", 20),
                                foreground="#e5efc1")
        try_again_label.place(x=100, y=200)
        root.after(1000, lambda: try_again_label.destroy())

def clear_screen(window):
    print("clear_screen_funkcija")
    for widget in window.winfo_children():
        widget.destroy()


def vase_list(root):
  
    rows = 2
    columns = 5
    frames = []

    for i in range(rows*columns):
        frames.append(Vase(root,f"Vase {i+1}"))


    for i in range(rows*columns):
                if i < 5:
                    frames[i].grid(row=0,column=i,padx=10,pady=10)
                else:
                     frames[i].grid(row=1,column=i-5,padx=10,pady=10)

    conn = sqlite3.connect("plants.db")
    c = conn.cursor()

    c.execute("SELECT * FROM plants")

    database_rows = c.fetchall()
    print(database_rows)

    for plant in database_rows:
          frames[plant[0]-1].name = plant[3]
          frames[plant[0]-1].plant = Plant(plant[1],plant[2],plant[4],plant[5],plant[6],plant[7],plant[8],plant[9])
        

    for i in range(rows*columns):
            if frames[i].plant == "Empty":
                frames[i].button_add.place(relx=0.5, rely=0.5, anchor="center")
                frames[i].button_add.configure(font=("Ink Free", 20))

            else:
                plant_name_label = tk.Label(frames[i],text=f"{frames[i].plant.name}",font=("Ink Free", 24),bg="#557b83")
                plant_name_label.place(relx=0.1, rely=0.6, anchor="w")
                print(frames[i].plant.photo)
                plant_picture = Image.open(frames[i].plant.photo)
                plant_picture = plant_picture.resize((200,200),Image.ANTIALIAS)

                plant_photo = ImageTk.PhotoImage(plant_picture)
                photos.append(plant_photo)
                label_photo = tk.Label(frames[i], image=plant_photo)
                label_photo.place(relx=0.5,rely=0.3,anchor="center")

                frames[i].button_delete.place(relx=0.05,rely=0.9)
                frames[i].button_edit.place(relx=0.55,rely=0.9)
                                
    def sync_sensors():
        for i in range(len(frames)):
            frames[i].humidity_data =  humidity_sensor()
            frames[i].sunlight_data =  sunlight_sensor()
            frames[i].salinity_data =  salinity_sensor()
            frames[i].ph_data =  ph_sensor()

            frames[i].humidity =  frames[i].humidity_data.humidity[-30]
            frames[i].sunlight =  frames[i].sunlight_data.sunlight[-30]
            frames[i].salinity =  round(frames[i].salinity_data.salinity[-30],3)
            frames[i].ph =  frames[i].ph_data.ph[-30]




    help_label = tk.Label(root,text="For more info about a vase click on it",font=("Ink Free",15))
    help_label.grid(row=3, column=0, columnspan=columns, sticky="n")
    sync_button = tk.Button(root,text="sync sensors",command=sync_sensors)
    sync_button.configure(font=("Ink Free",15))
    sync_button.grid(row=3,column=3)
    outside_temp = wheatherAPI.current_weather_api()
    curr_wheather = tk.Label(root,text=f"Current outside temperature: {outside_temp}",font=("Ink Free",15))
    curr_wheather.grid(row=4,column=0,columnspan=columns,sticky="s")

def main():
    print("main_funkcija")
    global root


    root = tk.Tk()
    root.title("PyFloraPosuda")
    print("entering database function")
    database()
    print("exit database function")
    print("entering signin function")
    sign_in_screen(root)
    
    root.geometry("1600x975")
    print("exit signin function")
    print("enter vase_list funkcija")
    vase_list(root)


    tk.mainloop()


if __name__ == "__main__":
  main()