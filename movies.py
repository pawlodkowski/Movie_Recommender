# Imports
import pandas as pd
import tkinter as tkt

def get_data():
    # function that returns a dataframe of movies
    PATH = "data/OMDB.csv"
    df = pd.read_csv(PATH)
    return df

df = get_data()

#GUI
wd = tkt.Tk()
wd.title("Movie Recommender") #window header
wd.geometry("350x200") #window size width x height

#wd.iconbitmap("pz_ECv_icon.ico") #change icon in header
       
#define variable types 
scr = tkt.StringVar() #metascore
kwd = tkt.StringVar() #key words
dur = tkt.IntVar()

#Define button functions
#button close
def closew():
    wd.destroy()
    
#Labels & Widgets    
tkt.Label(wd, text = "Welcome to the best movie recommender on this planet.").place(x = 10,y = 10) #label
#key words
tkt.Label(wd, text = "Key words").place(x = 10,y = 40) #label
e1 = tkt.Entry(wd, width=20, textvariable=kwd, bd = 2) #entry field
e1.place(x = 100,y = 40)
e1.focus_set() #set cursor to this entry when loading screen


tkt.Label(wd, text = "Score").place(x=10,y=70)
tkt.Entry(wd, width=5, textvariable=scr,bd=2).place(x=100,y=70)

tkt.Label(wd, text = "max duration").place(x=10,y=100)
tkt.Radiobutton(wd, text = "1.5h", variable = dur, value = 1).place(x=100,y=100)
tkt.Radiobutton(wd, text = "2h", variable = dur, value = 2).place(x=150,y=100)
tkt.Radiobutton(wd, text = "2.5h", variable = dur, value = 3).place(x=100,y=120)
tkt.Radiobutton(wd, text = "3h", variable = dur, value = 4).place(x=150,y=120)
tkt.Radiobutton(wd, text = "3.5h", variable = dur, value = 5).place(x=100,y=140)
tkt.Radiobutton(wd, text = ">3.5h", variable = dur, value = 6).place(x=150,y=140)


#Buttons
#B = tkt.Button(wd, bg='pink', activebackground="green", text = "calculate", command = getE).place(x = 60,y = 80)
cls = tkt.Button(wd, bg='green', text = "Exit", command = closew).place(x = 300,y = 60)

wd.mainloop() #'infinite loop' that runs until main window is destroyed

#print("Welcome to the best movie recommender on this planet.")

#genre = input("enter a genre (or leave it blank): ")
#reviewer = input("your favourite reviewer: ")


#if genre:
#    g = df[df["Genre"] == genre]
#else:
#    g = df


#if g.shape[0] > 0:
#    result = g.sort_values(["Metascore"], ascending = False)

    #(result.head(3).sample(1))
#    print(result.head(3).sample(1))
#else:
#    print("Sorry, no results! No movies in the {} genre.".format(genre))

