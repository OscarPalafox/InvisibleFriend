# Program to be executed for the GUI to appear
from tkinter import StringVar, Label, Button, Entry, Tk
from pickle import load
from select_people import make_and_save_relations
from send_email import create_server, send_email_gift
from smtplib import SMTPRecipientsRefused


def start(email, sent_list):
    email = StringVar()

    for widget in window.winfo_children():
        widget.grid_forget()

    welcome_Label = Label(
        window, text='Select your name.', font=('Courier', 20))
    welcome_Label.grid(row=0, column=1, columnspan=2, sticky='w')

    index_col = 0
    index_row = 1

    for person in relations:
        name_Button = Button(
            window, text=person, command=lambda person=person, sent_list=sent_list: send_page(person, sent_list))

        if person in sent_list:
            name_Button.config(fg='grey')

        name_Button.grid(row=index_row, column=index_col)

        if index_col in range(3):
            index_col += 1

        else:
            index_row += 1
            index_col = 0


def send_page(person, sent_list):
    gifter = person

    for widget in window.winfo_children():
        widget.grid_forget()

    welcome_Label = Label(
        window, text='Hey {}, write your email and click send.'.format(person))
    welcome_Label.grid(row=0, column=0, columnspan=2, sticky='w')

    email_Label = Label(window, text='Email:')
    email_Label.grid(row=2, column=0, sticky='e')
    email_widget = Entry(window, width=30, textvariable=email)
    email_widget.grid(row=2, column=1, sticky='w')

    enter_Button = Button(
        window, text='SEND', command=lambda email=email, person=gifter, sent_list=sent_list: send_email(gifter, email, sent_list))
    enter_Button.grid(row=3, column=1, sticky='e')

    back_Button = Button(window, text='BACK',
                         command=lambda email=email, sent_list=sent_list: start(email, sent_list))
    back_Button.grid(row=3, column=0, sticky='w')


def send_email(gifter, email, sent_list):

    email_to_send = email.get()

    try:
        email_error_Label.grid_forget()
        gifted = relations[gifter]

        if '@' not in email_to_send or '.' not in email_to_send:
            raise SMTPRecipientsRefused(email_to_send)

        send_email_gift(gmail_user, gmail_password,
                        server, email_to_send, gifted, gifter)

        sent.add(gifter)

        email = StringVar()

        for widget in window.winfo_children():
            widget.grid_forget()

        sent_Label = Label(
            window, text='EMAIL SENT', fg='black', bg='green')
        sent_Label.grid(row=1, column=0, sticky='w')

        back_Button = Button(window, text='BACK',
                             command=lambda email=email, sent_list=sent_list: start(email, sent_list))
        back_Button.grid(row=2, column=0, sticky='w')

    except SMTPRecipientsRefused:
        email_error_Label.grid(row=4, column=1)


if __name__ == '__main__':
    make_and_save_relations()

    with open('gifts.pck', 'rb') as gift_file:
        relations = load(gift_file)

    to_send = set(relations.keys())
    sent = set()
    gmail_user, gmail_password, server = create_server()

    window = Tk()
    window.title('Invisible Friend')
    window.geometry('400x150')

    email = StringVar()
    email_error_Label = Label(
        window, text='INCORRECT EMAIL', fg='white', bg='red')

    start(email, sent)
    window.mainloop()
