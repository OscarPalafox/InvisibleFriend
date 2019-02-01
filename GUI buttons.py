# Program to be executed for the GUI to appear
import tkinter, pickle, time
import SelectPeople
import SendEmail


def start():
	global email

	email = tkinter.StringVar()

	for widget in window.winfo_children():
			widget.grid_forget()

	welcome_Label = tkinter.Label(window, text = "Select your name.", font = ("Courier", 20))
	welcome_Label.grid(row = 0, column = 1, columnspan = 2, sticky = "w")

	index_col = 0
	index_row = 1

	for person in relations:
		name_Button = tkinter.Button(window, text = person, command = lambda person = person: send_page(person))

		if person in sent:
			name_Button.config(fg = "grey")

		name_Button.grid(row = index_row, column = index_col)

		if index_col in range(3):
			index_col += 1

		else:
			index_row += 1
			index_col = 0


def send_page(person):
	global name_to_send

	name_to_send = person

	for widget in window.winfo_children():
			widget.grid_forget()

	welcome_Label = tkinter.Label(window, text = "Hey {}, write your email and click send.".format(person))
	welcome_Label.grid(row = 0, column = 0, columnspan = 2, sticky = "w")


	email_Label = tkinter.Label(window, text = "Email:")
	email_Label.grid(row = 2, column = 0, sticky = "e")
	email_widget = tkinter.Entry(window, width = 30, textvariable = email)
	email_widget.grid(row = 2, column = 1, sticky = "w")

	enter_Button = tkinter.Button(window, text = "SEND", command = send_email)
	enter_Button.grid(row = 3, column = 1, sticky = "e")

	back_Button = tkinter.Button(window, text = "BACK", command = start)
	back_Button.grid(row = 3, column = 0, sticky = "w")


def send_email():
	global sent
	global email

	email_to_send = email.get()

	try:
		email_error_Label.grid_forget()

		gifted = relations[name_to_send]
		if "@" not in email_to_send or "." not in email_to_send:
			raise SendEmail.smtplib.SMTPRecipientsRefused(email_to_send)

		SendEmail.send_email(email_to_send, gifted)
		
		if name_to_send not in sent:
			sent.append(name_to_send)

		email = tkinter.StringVar()

		for widget in window.winfo_children():
			widget.grid_forget()

		sent_Label = tkinter.Label(window, text = "EMAIL SENT", fg = "black", bg = "green")
		sent_Label.grid(row = 1, column = 0, sticky = "w")

		back_Button = tkinter.Button(window, text = "BACK", command = start)
		back_Button.grid(row = 2, column = 0, sticky = "w")

	
	except SendEmail.smtplib.SMTPRecipientsRefused:
		email_error_Label.grid(row = 4, column = 1)


with open("Gifts.pck", "rb") as gift_file:
	relations = pickle.load(gift_file)

to_send = set(relations.keys())
sent = []

window = tkinter.Tk()
window.title("Invisible Friend")
window.geometry("400x125")

email = tkinter.StringVar()
email_error_Label = tkinter.Label(window, text = "INCORRECT EMAIL", fg = "white", bg = "red")

start()
window.mainloop()