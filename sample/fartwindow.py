import os, sys
from tkinter import *
from PIL import ImageTk, Image

def main():
    # Path we ran from
    program_directory = sys.path[0]

    # Create our window
    root = Tk()
    root.title('FART (Foggy Album Rename Tool)')
    #root.iconphoto(True, PhotoImage(file=os.path.join(program_directory, 'pycon.png')))

    # Entry frame
    entry_frame = LabelFrame(root, padx=10, pady=10)
    entry_frame.pack()

    # Artist name text box
    artist_name_label = Label(entry_frame, text='Artist Name', anchor=E)
    artist_name_label.grid(row=0, column=0, padx=5)
    artist_name_box = Entry(entry_frame, width=30, borderwidth=3)
    artist_name_box.grid(row=0, column=1, padx=5, pady=5)

    # Album name text box
    album_name_label = Label(entry_frame, text='Album Name', anchor=E)
    album_name_label.grid(row=0, column=2, padx=5)
    album_name_box = Entry(entry_frame, width=30, borderwidth=3)
    album_name_box.grid(row=0, column=3, padx=5, pady=5, columnspan=2)

    # Youtube link
    link_label = Label(entry_frame, text='Youtube Link', anchor=E)
    link_label.grid(row=1, column=0, padx=5)
    link_box = Entry(entry_frame, width=30, borderwidth=3)
    link_box.grid(row=1, column=1, padx=5, pady=5)

    # Min-match box
    min_match_label = Label(entry_frame, text='Min Match', anchor=E)
    min_match_label.grid(row=1, column=2, padx=5)
    min_match_box = Entry(entry_frame, width=30, borderwidth=3)
    min_match_box.delete(0, END)
    min_match_box.insert(0, '75')
    min_match_box.grid(row=1, column=3, padx=5, pady=5, columnspan=2)

    # Music root box
    music_root_label = Label(entry_frame, text='Music Root', anchor=E)
    music_root_label.grid(row=2, column=0, padx=5)
    music_root_box = Entry(entry_frame, width=30, borderwidth=3)
    music_root_box.delete(0, END)
    music_root_box.insert(0, '/home/aogden/Music')
    music_root_box.grid(row=2, column=1, padx=5, pady=5)

    # Music root button
    music_root_button = Button(entry_frame, text='Browse', padx=10)
    music_root_button.grid(row=2, column=2)

    # Report only
    report_only_check = Checkbutton(entry_frame, text='Report Only')
    report_only_check.select()
    report_only_check.grid(row=2, column=3)

    # Ignore warnings
    ignore_warn_check = Checkbutton(entry_frame, text='Ignore Warnings')
    ignore_warn_check.grid(row=2, column=4)

    # display frame
    display_frame = LabelFrame(root, text='Matches', padx=5, pady=5)
    display_frame.pack()

    # test entry for display frame
    test_entry = Entry(display_frame, width=20, borderwidth=3)
    test_entry.pack()

    # Control frame
    control_frame = LabelFrame(root, padx=10, pady=10)
    control_frame.pack()

    # Control buttons
    go_button = Button(control_frame, text='Rename', padx=10)
    go_button.grid(row=0, column=0)
    go_button = Button(control_frame, text='Quit', padx=10)
    go_button.grid(row=0, column=1)

    root.mainloop()

if __name__ == "__main__":
    main()