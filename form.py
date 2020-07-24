import tkinter as tk 
from tkinter import ttk 

def save_info():
  firstname_info = firstname.get()
  place_info = place.get()
  language_info = language.get()  
  print(firstname_info,place_info,language_info)



  file = open("user.txt", "w")
  file.write('{} {} {}'.format(firstname_info, place_info,language_info))
  file.close()
  print(" User ", firstname_info, " has been registered successfully")

  firstname_entry.delete(0,tk.END)
  place_entry.delete(0,tk.END)
  language_entry.delete(0,tk.END)



screen = tk.Tk()
screen.minsize(400,400)
screen.title("SpeechAnalyzer")
#heading = tk.Label(text = "Please, submit your information", bg = "grey", fg = "black", width = "500", height = "3")
 
firstname_text = ttk.Label(text = "Firstname : ",)
firstname_text.grid(column = 0, row = 0)

place_text = ttk.Label(text = "Company : ",)
place_text.grid(column = 0, row = 15)

language_text = tk.Label(text = "Language : ",)
language_text.grid(column = 0 , row = 30)

language = tk.StringVar() 
firstname = tk.StringVar()
place = tk.StringVar()


language_entry = ttk.Combobox(screen,width = 27, textvariable = language)  
firstname_entry = ttk.Entry(screen,textvariable = firstname, width = "30")
place_entry = ttk.Entry(screen,textvariable = place, width = "30")

language_entry['values'] = ('Italian',  
                          'English', 
                          'French', 
                          'German', 
                          'Spanish')


firstname_entry.grid(column = 1, row = 0)
place_entry.grid(column = 1, row = 15)
language_entry.grid(column = 1, row = 30)
language_entry.current(1) 

register = ttk.Button(screen,text = "Register", command = save_info)
register.grid(column = 5, row = 30)

screen.mainloop()