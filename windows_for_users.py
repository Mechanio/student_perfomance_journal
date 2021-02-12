from tkinter import *
from tkinter.ttk import Notebook
import sqlite3
import tkinter.messagebox
import re
import os

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()


def adding_date(title_of_class_entry, title_of_subject_entry, add_root, teacher_id, date_entry):
    cur.execute('SELECT id FROM Subjects WHERE title = ? ', (title_of_subject_entry.get(),))
    subject_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM Classes WHERE title = ? ', (title_of_class_entry.get(),))
    class_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM Students WHERE class_id = ? ', (class_id,))
    student_ids = cur.fetchall()
    student_ids2 = []
    for i in range(len(student_ids)):
        student_ids2.append(student_ids[i][0])
    student_ids = student_ids2
    print(student_ids)
    for i in student_ids:
        print(i)
        cur.execute('''INSERT INTO Marks
                                (subject_id, teacher_id,student_id,class_id,dating) 
                                VALUES ( ?, ?, ?, ?, ? )''',
                    (subject_id, teacher_id, i, class_id, date_entry))

    tkinter.messagebox.showinfo("Great", "You have added a new date")
    add_root.destroy()
    conn.commit()


def add_date(teacher_id):
    add_root = Toplevel()
    add_root.title("Adding new date")
    add_root.geometry("250x200+50+300")
    add_root.resizable(width=False, height=False)

    frame1 = Frame(add_root)
    frame1.pack()

    title_of_subject_label = Label(frame1, text="Enter name of a subject:")
    title_of_subject_label.pack()

    title_of_subject_entry = Entry(frame1)
    title_of_subject_entry.pack(padx=5, pady=5)

    title_of_class_label = Label(frame1, text="Enter name of a group:")
    title_of_class_label.pack()

    title_of_class_entry = Entry(frame1)
    title_of_class_entry.pack(padx=5, pady=5)

    date_label = Label(frame1, text="Enter date:")
    date_label.pack()

    date_entry = Entry(frame1)
    date_entry.pack(padx=5, pady=5)

    button_add_date_final = Button(frame1, text="Add",
                                   command=lambda: adding_date(title_of_class_entry, title_of_subject_entry,
                                                               add_root, teacher_id, date_entry.get()))
    button_add_date_final.pack(padx=5, pady=5)


def restart(tablayout, tabs, root, data, list_of_entries):
    final_list_of_entries = []
    entry_temp = 0
    for entry in list_of_entries:
        if entry.get() == '':
            final_list_of_entries.append(None)
        else:
            final_list_of_entries.append(int(entry.get()))
    for i in range(tablayout.index("end")):
        subject_names = re.search(r'\((.*?)\)', str(tablayout.tab(i)))
        subject_name = subject_names.group(1)
        class_names = re.search(r'\'([А-Я].*?)\(', str(tablayout.tab(i)))
        class_name = class_names.group(1)
        cur.execute('SELECT id FROM Classes WHERE title = ? ', (class_name,))
        class_id = cur.fetchone()[0]
        cur.execute('SELECT id FROM Subjects WHERE title = ? ', (subject_name,))
        subject_id = cur.fetchone()[0]
        cur.execute('SELECT fullname FROM Students WHERE class_id = ? ', (class_id,))
        names = cur.fetchall()
        name_temp = 0
        cur.execute('SELECT dating FROM Marks WHERE subject_id = ? AND class_id=? ', (subject_id, class_id))
        dates = cur.fetchall()
        datestemp = []
        for k in range(len(dates)):
            datestemp.append(dates[k][0])
        dates = []
        date_temp = 0
        for q in datestemp:
            if q not in dates:
                dates.append(q)
        col_count, row_count = tabs[i].grid_size()
        for row in range(row_count):
            for column in range(col_count):
                if column == 0 and row == 0:
                    pass
                elif column == 0 and row != 0:
                    name_temp += 1
                    pass
                elif column != 0 and row == 0:
                    date_temp += 1
                    pass
                elif column != 0 and row != 0:

                    date = dates[column - 1]
                    cur.execute(
                        '''SELECT id FROM Students  WHERE fullname = ? ''',
                        (names[name_temp - 1][0],))
                    student_id = cur.fetchone()[0]
                    print(final_list_of_entries[entry_temp], subject_id, data[0], student_id, class_id, date)
                    cur.execute(
                        '''UPDATE Marks SET mark = ? WHERE subject_id = ? AND teacher_id=? AND student_id=? AND class_id=? AND dating=? ''',
                        (final_list_of_entries[entry_temp], subject_id, data[0], student_id, class_id, date))
                    entry_temp += 1
    conn.commit()
    root.destroy()
    Teacher_window(data)


def edit(button_add_date, button_edit, tablayout, tabs, root, data, dict):
    large_list = []
    list_of_entries = []
    for key in dict:
        large_list.append(dict[key])
    button_edit.configure(text='End edit',
                          command=lambda: restart(tablayout, tabs, root, data, list_of_entries))
    for i in range(tablayout.index("end")):
        col_count, row_count = tabs[i].grid_size()
        for row in range(row_count):
            for column in range(col_count):
                if column == 0 and row == 0:
                    pass
                elif column == 0 and row != 0:
                    pass
                elif column != 0 and row == 0:
                    pass
                elif column != 0 and row != 0:
                    cell = Entry(tabs[i], bg='#D3D3D3')
                    temp = large_list[i][row][column - 1]
                    if temp != None:
                        cell.insert(0, large_list[i][row][column - 1])
                    cell.grid(row=row, column=column)
                    tabs[i].grid_columnconfigure(column, weight=1)
                    list_of_entries.append(cell)
        tablayout.pack(fill=X, padx=5, expand=True)


def adding_subject(teacher_id, title_of_class_entry, subject_name_entry, add_root):
    cur.execute('''INSERT OR IGNORE INTO Subjects (title) 
                    VALUES ( ? )''', (subject_name_entry.get(),))

    cur.execute('SELECT id FROM Subjects WHERE title = ? ', (subject_name_entry.get(),))
    subject_id = cur.fetchone()[0]

    cur.execute('SELECT subject_id1 FROM Teachers WHERE id = ? ', (teacher_id,))
    subject_id1 = cur.fetchone()[0]
    if subject_id1 != None:
        cur.execute('SELECT subject_id2 FROM Teachers WHERE id = ? ', (teacher_id,))
        subject_id2 = cur.fetchone()[0]
        if subject_id2 != None:
            cur.execute('SELECT subject_id3 FROM Teachers WHERE id = ? ', (teacher_id,))
            subject_id3 = cur.fetchone()[0]
            if subject_id3 != None:
                cur.execute('SELECT subject_id4 FROM Teachers WHERE id = ? ', (teacher_id,))
                subject_id4 = cur.fetchone()[0]
                if subject_id == subject_id1 or subject_id == subject_id2 or subject_id == subject_id3 or subject_id == subject_id4:
                    pass
                elif subject_id4 != None:
                    tkinter.messagebox.showerror("Warning", "Maximum amount of subjects for one teacher is reached")
                    return
                else:
                    cur.execute('''UPDATE Teachers SET subject_id4 = ? WHERE id = ? ''',
                                (subject_id, teacher_id))
            elif subject_id == subject_id1 or subject_id == subject_id2:
                pass
            else:
                cur.execute('''UPDATE Teachers SET subject_id3 = ? WHERE id = ? ''',
                            (subject_id, teacher_id))
        elif subject_id == subject_id1:
            pass
        else:
            cur.execute('''UPDATE Teachers SET subject_id2 = ? WHERE id = ? ''',
                        (subject_id, teacher_id))
    else:
        cur.execute('''UPDATE Teachers SET subject_id1 = ? WHERE id = ? ''',
                    (subject_id, teacher_id))

    conn.commit()

    cur.execute('SELECT id FROM Classes WHERE title = ? ', (title_of_class_entry.get(),))
    class_id = cur.fetchone()[0]

    cur.execute('SELECT class_id1 FROM Subjects WHERE title = ? ', (subject_name_entry.get(),))
    class_id1 = cur.fetchone()[0]
    if class_id1 != None:
        cur.execute('SELECT class_id2 FROM Subjects WHERE title = ? ', (subject_name_entry.get(),))
        class_id2 = cur.fetchone()[0]
        if class_id2 != None:
            cur.execute('SELECT class_id3 FROM Subjects WHERE title = ? ', (subject_name_entry.get(),))
            class_id3 = cur.fetchone()[0]
            if class_id3 != None:
                cur.execute('SELECT class_id4 FROM Subjects WHERE title = ? ', (subject_name_entry.get(),))
                class_id4 = cur.fetchone()[0]
                if class_id4 != None:
                    tkinter.messagebox.showerror("Warning", "Maximum amount of groups for one subjects is reached")
                    return
                elif class_id == class_id1 or class_id == class_id2 or class_id == class_id3:
                    pass
                else:
                    cur.execute('''UPDATE Subjects SET class_id4 = ? WHERE title = ? ''',
                                (class_id, subject_name_entry.get()))
            elif class_id == class_id1 or class_id == class_id2:
                pass
            else:
                cur.execute('''UPDATE Subjects SET class_id3 = ? WHERE title = ? ''',
                            (class_id, subject_name_entry.get()))
        elif class_id == class_id1:
            pass
        else:
            cur.execute('''UPDATE Subjects SET class_id2 = ? WHERE title = ? ''',
                        (class_id, subject_name_entry.get()))
    else:
        cur.execute('''UPDATE Subjects SET class_id1 = ? WHERE title = ? ''',
                    (class_id, subject_name_entry.get()))

    tkinter.messagebox.showinfo("Great", "You have added a new subject")
    add_root.destroy()
    conn.commit()


def add_subject(teacher_id):
    add_root = Toplevel()
    add_root.title("Adding a new subject")
    add_root.geometry("250x200+50+300")
    add_root.resizable(width=False, height=False)

    frame1 = Frame(add_root)
    frame1.pack()

    subject_name_label = Label(frame1, text="Enter name of a subject:")
    subject_name_label.pack()

    subject_name_entry = Entry(frame1)
    subject_name_entry.pack(padx=5, pady=5)

    title_of_class_label = Label(frame1, text="Enter group in which subject will be learnt:")
    title_of_class_label.pack()

    title_of_class_entry = Entry(frame1)
    title_of_class_entry.pack(padx=5, pady=5)

    button_add_subject_final = Button(frame1, text="Add",
                                      command=lambda: adding_subject(teacher_id, title_of_class_entry,
                                                                     subject_name_entry, add_root))
    button_add_subject_final.pack(padx=5, pady=5)


def adding_student(title_of_class_entry, student_name_entry, add_root):
    cur.execute('''INSERT OR IGNORE INTO Classes (title) 
                    VALUES ( ? )''', (title_of_class_entry.get(),))

    cur.execute('SELECT id FROM Classes WHERE title = ? ', (title_of_class_entry.get(),))
    class_id = cur.fetchone()[0]

    cur.execute('''INSERT INTO Students
                        (fullname, class_id) 
                        VALUES ( ?, ? )''',
                (student_name_entry.get(), class_id))
    tkinter.messagebox.showinfo("Great", "You have added a new student")
    add_root.destroy()
    conn.commit()


def add_student():
    add_root = Toplevel()
    add_root.title("Adding a new student")
    add_root.geometry("250x200+50+300")
    add_root.resizable(width=False, height=False)

    frame1 = Frame(add_root)
    frame1.pack()

    student_name_label = Label(frame1, text="Enter name of astudent:")
    student_name_label.pack()

    student_name_entry = Entry(frame1)
    student_name_entry.pack(padx=5, pady=5)

    title_of_class_label = Label(frame1, text="Enter group of a student:")
    title_of_class_label.pack()

    title_of_class_entry = Entry(frame1)
    title_of_class_entry.pack(padx=5, pady=5)

    button_add_student_final = Button(frame1, text="Add",
                                      command=lambda: adding_student(title_of_class_entry, student_name_entry,
                                                                     add_root))
    button_add_student_final.pack(padx=5, pady=5)


def exiting(root):
    root.destroy()
    os.system('python authorization.py')


def Teacher_window(data):
    root = Tk()
    root.title("Student Perfomance Journal")
    root.geometry("800x350")
    root.resizable(width=False, height=False)

    frameleft = Frame(root)
    frameleft.pack(side=LEFT, anchor=N)

    frame_upright = Frame(root)
    frame_upright.pack(side=RIGHT, anchor=N, expand=1, fill=X)

    logged_in = Label(frameleft, text='''Welcome
    ''' + data[1])
    logged_in.pack(padx=5, pady=5)

    button_add_student = Button(frameleft, text="Add student", command=add_student)
    button_add_student.pack(padx=5, pady=5)

    button_add_subject = Button(frameleft, text="Add subjects", command=lambda: add_subject(data[0]))
    button_add_subject.pack(padx=5, pady=5)

    button_add_date = Button(frameleft, text="Add date", command=lambda: add_date(data[0]))
    button_add_date.pack(padx=5, pady=5)

    button_edit = Button(frameleft, text="Edit", command=lambda: edit(button_add_date, button_edit, tablayout,
                                                                            tabs_list, root, data, elder_dict))
    button_edit.pack(padx=5, pady=5)

    button_add_date = Button(frameleft, text="Exit", command=lambda: exiting(root))
    button_add_date.pack(padx=5, pady=50)

    tablayout = Notebook(frame_upright)

    elder_dict = {}  # Dictionary for students grades for further usage
    tabs_list = []
    subject_ids = list(data[4:])  # List of teacher's subject's
    for i in subject_ids:
        temp = 0  # Variable for pointing on group
        if i != None:
            cur.execute('SELECT * FROM Subjects WHERE id = ? ', (i,))
            class_ids = cur.fetchall()[0]
            subject_name = class_ids[1]
            class_ids = list(class_ids[2:])  # Groups, which have a current subject
            for j in class_ids:
                if j != None:
                    cur.execute('SELECT fullname FROM Students WHERE class_id = ? '
                                , (class_ids[temp],))
                    names = cur.fetchall()  # names of students in current group
                    name_temp = 0
                    date_temp = 0
                    elder_dict['list%s%s' % (i, j)] = []
                    c = 'tab{}{}'.format(i, j)
                    c = Frame(tablayout)
                    c.pack(side=LEFT)
                    cur.execute('SELECT title FROM Classes WHERE id = ? ', (class_ids[temp],))
                    title_of_class = cur.fetchone()
                    cur.execute('SELECT dating FROM Marks WHERE subject_id = ? AND class_id=? ', (i, class_ids[temp]))
                    dates = cur.fetchall()
                    datestemp = []
                    for k in range(len(dates)):
                        datestemp.append(dates[k][0])
                    dates = []
                    for q in datestemp:
                        if q not in dates:
                            dates.append(q)
                    for row in range(len(names) + 1):
                        child_list = []
                        for column in range(len(dates) + 1):
                            if column == 0 and row == 0:
                                cell = Label(c, text="Name", bg="black", fg='white', width=12)
                                cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                            elif column == 0 and row != 0:  # стовпець ПІБ студентів
                                cell = Label(c, text=names[name_temp][0], bg='grey')
                                name_temp += 1
                                cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                            elif column != 0 and row == 0:  # рядок дат
                                if dates == []:
                                    continue
                                cell = Label(c, text=dates[date_temp], bg='grey')
                                date_temp += 1
                                cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                                c.grid_columnconfigure(column, weight=1)
                            else:
                                date = dates[column - 1]
                                cur.execute(
                                    '''SELECT id FROM Students  WHERE fullname = ? ''',
                                    (names[name_temp - 1][0],))
                                student_id = cur.fetchone()[0]
                                try:
                                    cur.execute(
                                        '''SELECT mark FROM Marks  WHERE subject_id = ? AND teacher_id=? AND student_id=? AND class_id=? AND dating=? ''',
                                        (i, data[0], student_id, class_ids[temp], date))
                                    mark = cur.fetchone()[0]
                                except TypeError:
                                    cur.execute('''INSERT INTO Marks
                                                                    (subject_id, teacher_id,student_id,class_id,dating) 
                                                                    VALUES ( ?, ?, ?, ?, ? )''',
                                                (i, data[0], student_id, class_ids[temp], date))
                                    cur.execute(
                                        '''SELECT mark FROM Marks  WHERE subject_id = ? AND teacher_id=? AND student_id=? AND class_id=? AND dating=? ''',
                                        (i, data[0], student_id, class_ids[temp], date))
                                    mark = cur.fetchone()[0]
                                cell = Label(c, text=mark, bg='#D3D3D3')
                                cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                                c.grid_columnconfigure(column, weight=1)
                                child_list.append(mark)
                        elder_dict['list%s%s' % (i, j)].append(child_list)
                    tablayout.add(c, text='{}({})'.format(title_of_class[0], subject_name))
                    tabs_list.append(c)
                    temp += 1
                    tablayout.pack(fill=X, padx=5, expand=True)
    root.mainloop()


def Student_window(data):
    root = Tk()
    root.title("Student Perfomance Journal")
    root.geometry("800x200")
    root.resizable(width=False, height=False)

    frameleft = Frame(root)
    frameleft.pack(side=LEFT, anchor=N)

    frame_upright = Frame(root)
    frame_upright.pack(side=RIGHT, anchor=N, expand=1, fill=X)

    logged_in = Label(frameleft, text='''Welcome
    ''' + data[1])
    logged_in.pack(padx=5, pady=5)

    button_add_date = Button(frameleft, text="Exit", command=lambda: exiting(root))
    button_add_date.pack(padx=5, pady=5)

    tablayout = Notebook(frame_upright)

    class_id = data[2]  # Group of student
    cur.execute('SELECT id FROM Subjects WHERE class_id1 = ? OR class_id2=? OR class_id3=? or class_id4=?'
                , (class_id, class_id, class_id, class_id))
    subject_ids = cur.fetchall()
    subjectstemp = []
    for k in range(len(subject_ids)):
        subjectstemp.append(subject_ids[k][0])
    subjects = []
    for q in subjectstemp:
        if q not in subjects:
            subjects.append(q)
    print(subjects)
    for i in subjects:
        cur.execute('SELECT title FROM Subjects WHERE id = ? ', (i,))
        subject_name = cur.fetchall()[0]
        cur.execute('SELECT id FROM Teachers WHERE subject_id1 = ? OR subject_id2=? OR subject_id3=? or subject_id4=?'
                    , (i, i, i, i))
        teacher_id = cur.fetchall()[0]
        name = data[1]  # names of students in current group
        date_temp = 0
        c = 'tab{}'.format(i, )
        c = Frame(tablayout)
        c.pack(side=LEFT)
        cur.execute('SELECT dating FROM Marks WHERE subject_id = ? AND class_id=? ', (i, class_id))
        dates = cur.fetchall()
        datestemp = []
        for k in range(len(dates)):
            datestemp.append(dates[k][0])
        dates = []
        for q in datestemp:
            if q not in dates:
                dates.append(q)
        for row in range(2):
            for column in range(len(dates) + 1):
                if column == 0 and row == 0:
                    cell = Label(c, text="Name\\Date", bg="black", fg='white', width=12)
                    cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                elif column == 0 and row != 0:  # column of student Name/Surname
                    cell = Label(c, text=name, bg='grey')
                    cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                elif column != 0 and row == 0:  # row of dates
                    if dates == []:
                        continue
                    cell = Label(c, text=dates[date_temp], bg='grey')
                    date_temp += 1
                    cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                    c.grid_columnconfigure(column, weight=1)
                else:
                    date = dates[column - 1]
                    print(i, teacher_id, data[0], class_id, date)
                    cur.execute(
                        '''SELECT mark FROM Marks  WHERE subject_id = ? AND teacher_id=? AND student_id=? AND class_id=? AND dating=? ''',
                        (i, teacher_id[0], data[0], class_id, date))
                    mark = cur.fetchone()[0]
                    cell = Label(c, text=mark, bg='#D3D3D3')
                    cell.grid(row=row, column=column, padx=1, pady=1, sticky='nsew')
                    c.grid_columnconfigure(column, weight=1)
        tablayout.add(c, text='{}'.format(subject_name[0]))
        tablayout.pack(fill=X, padx=5, expand=True)
    root.mainloop()
