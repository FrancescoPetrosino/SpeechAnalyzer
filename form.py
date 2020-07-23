from tkinter import *

def save_info():
  firstname_info = firstname.get()
  place_info = place.get()
  print(firstname_info,place_info)

  file = open("user.txt", "w")
  file.write('{} {}'.format(firstname_info, place_info))
  file.close()
  print(" User ", firstname_info, " has been registered successfully")

  firstname_entry.delete(0,END)
  place_entry.delete(0,END)



screen = Tk()
screen.geometry("400x250")
screen.title("SpeechAnalyzer")
heading = Label(text = "Please, submit your information", bg = "grey", fg = "black", width = "500", height = "3")
heading.pack()
 
firstname_text = Label(text = "Firstname : ",)
firstname_text.place(x = 15, y = 70)

place_text = Label(text = "Company : ",)
place_text.place(x = 15, y = 120)

firstname = StringVar()
place = StringVar()

firstname_entry = Entry(textvariable = firstname, width = "30")
place_entry = Entry(textvariable = place, width = "30")

firstname_entry.place(x = 15, y = 90)
place_entry.place(x = 15, y = 140)


register = Button(screen,text = "Register", width = "30", height = "2", command = save_info, bg = "grey")
register.place(x = 15, y = 200)

screen.mainloop()