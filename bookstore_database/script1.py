from tkinter import *
from tkinter import ttk
from backend import Database


database = Database()

window = Tk()
frame = ttk.Frame(window,padding=(12,12,12,12))



window.wm_title("BookTeca")

title_label = Label(frame,text="Title")
author_label = Label(frame,text="Author")
year_label = Label(frame,text="Year")
genre_label = Label(frame,text="Genre")


def view_command():
	list1.delete(0,END)
	for i in database.view():
		list1.insert(END,"{id}.'{title}' by {author}, {year}, {genre}".format(id=i[0],title=i[1],author=i[2],year=i[3],genre=i[4]))


def search_command():
	list1.delete(0,END)
	for i in database.search(title_text.get(),author_text.get(),year_text.get(),genre_text.get()):
		list1.insert(END,"{id}.'{title}' by {author}, {year}, {genre}".format(id=i[0],title=i[1],author=i[2],year=i[3],genre=i[4]))


def insert_command():
	if title_text.get() and author_text.get():
		database.insert(title_text.get(),author_text.get(),year_text.get(),genre_text.get())
		list1.delete(0,END) 
		list1.insert(END,"'{}' by {}, {}, {}".format(title_text.get(),author_text.get(),year_text.get(),genre_text.get()))
	else:
		pass



def get_selected(event):
	try:
		global item
		index = list1.curselection()[0]
		item = database.search_select(list1.get(index).split('.')[0])
		title_entry.delete(0,END)
		author_entry.delete(0,END)
		year_entry.delete(0,END)
		genre_entry.delete(0,END)
		title_entry.insert(END,item[0][1])
		author_entry.insert(END,item[0][2])
		year_entry.insert(END,item[0][3])
		genre_entry.insert(END,item[0][4])
	except IndexError:
		pass
	

def delete_command():
	database.delete(item[0][0])
	view_command()


def update_command():
	database.update(item[0][0],title_text.get(),author_text.get(),year_text.get(),genre_text.get())
	view_command()

title_text = StringVar()
author_text = StringVar()
year_text = StringVar()
genre_text = StringVar()

title_entry = Entry(frame,textvariable=title_text)
author_entry = Entry(frame,textvariable=author_text)
year_entry = Entry(frame,textvariable=year_text)
genre_entry = Entry(frame,textvariable=genre_text)

list1 = Listbox(frame,height=8,width=45)
sb1 = Scrollbar(frame)
sb2 = Scrollbar(frame,orient=HORIZONTAL)

list1.bind('<<ListboxSelect>>',get_selected)

list1.configure(yscrollcommand=sb1.set,xscrollcommand=sb2.set)
sb1.configure(command=list1.yview)
sb2.configure(command=list1.xview)

view_button = Button(frame,text="View all",width=12,command=view_command)
search_button = Button(frame,text="Search entry",width=12,command=search_command)
add_button = Button(frame,text="Add entry",width=12,command=insert_command)
update_button = Button(frame,text="Update",width=12,command=update_command)
delete_button = Button(frame,text="Delete",width=12,command=delete_command)
close_button = Button(frame,text="Close",width=12,command=window.destroy)


#gridding the wdigets
frame.grid(row=0,column=0,sticky=(N,W,E,S))

title_label.grid(row=0,column=0,sticky=E)
author_label.grid(row=0,column=2)
year_label.grid(row=1,column=0,sticky=E)
genre_label.grid(row=1,column=2) 
title_entry.grid(row=0,column=1)
author_entry.grid(row=0,column=3)
year_entry.grid(row=1,column=1)
genre_entry.grid(row=1,column=3)
list1.grid(row=2,column=0,rowspan=6,columnspan=2)
sb1.grid(row=2,column=2,rowspan=6)
view_button.grid(row=2,column=3,pady=(10,0))
search_button.grid(row=3,column=3)
add_button.grid(row=4,column=3)
update_button.grid(row=5,column=3)
delete_button.grid(row=6,column=3)
close_button.grid(row=7,column=3)
sb2.grid(row=7,column=0,columnspan=2,pady=(10,0))


#window.columnconfigure(0, weight=1)
#window.columnconfigure(1, weight=1)
#window.columnconfigure(2, weight=1)
#window.columnconfigure(3, weight=1)

#frame.rowconfigure(0,weight=1)
#frame.rowconfigure(1,weight=1)
#frame.rowconfigure(2,weight=1)
#frame.rowconfigure(3,weight=1)
#frame.rowconfigure(4,weight=1)
#frame.rowconfigure(5,weight=1)
#frame.rowconfigure(6,weight=1)
#frame.rowconfigure(7,weight=1)


window.mainloop()