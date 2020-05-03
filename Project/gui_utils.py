import tkinter as tk
from time import sleep
from tkinter import filedialog

import PIL
import numpy as np
from PIL import ImageTk, Image
from pyHook import HookManager  # catch every key stroke

import Key
import config_handler
import image_proc

FLAG_KEY = '~'


# create lines
def frame_cords_callback(event):
	canvas.create_line(0, event.y, width, event.y, fill="red")  # left to right
	canvas.create_line(event.x, 0, event.x, height, fill="red")  # up to down

	clicks_cords.append((event.x, event.y))
	if len(clicks_cords) == 2:
		sleep(0.3)
		window.destroy()


def get_frame_cords(text, np_img, data, data_key):
	global canvas, height, width
	global window
	global clicks_cords  # keep screen cords
	clicks_cords = []

	window = create_window("game_config", text)
	height = np_img.shape[0]
	width = np_img.shape[1]

	# crate new canvas
	canvas = tk.Canvas(window, width=width, height=height)
	canvas.pack()

	photo = PIL.ImageTk.PhotoImage(master=canvas, image=Image.fromarray(np_img))
	canvas.create_image(0, 0, image=photo, anchor=tk.NW)
	canvas.bind("<Button-1>", frame_cords_callback)
	# keep gui running
	window.mainloop()
	# arrange points according to top left and down right
	clicks_cords = [[min(clicks_cords[0][0], clicks_cords[1][0]), min(clicks_cords[0][1], clicks_cords[1][1])],
					[max(clicks_cords[0][0], clicks_cords[1][0]), max(clicks_cords[0][1], clicks_cords[1][1])]]
	data[data_key] = clicks_cords


# get the game's keys
def get_keys_callback(event):
	if event.char == '`':
		window.destroy()
		return
	if not (event.char in game_keys) and type(listbox.focus_get()) is tk.Listbox:
		key = Key.Key(event.char)
		game_keys.append(key)
		listbox.insert(tk.END, key)


def onselect_callback(event):
	w = event.widget
	if len(w.curselection()) == 0:
		return
	index = int(w.curselection()[0])
	if not game_keys[index].is_hold:
		w.delete(index)
		del game_keys[index]
	else:
		game_keys[index].switch_pressing_function()
		w.delete(index)
		w.insert(index, game_keys[index])


def restart_key_changed_callback(*_):
	if len(restart_key.get()) > 1:
		restart_key.set(restart_key.get()[-1])


def get_game_keys(data):
	global window
	global game_keys
	global listbox, restart_key
	game_keys = []

	window = create_window("game_config", "please insert all game keys and then press: " + FLAG_KEY)
	# bind to any key
	window.bind("<Key>", get_keys_callback)
	mouse_var = tk.IntVar()
	tk.Checkbutton(window, text="Mouse", variable=mouse_var).pack(anchor=tk.W)

	restart_key = tk.StringVar()
	restart_key.trace_add("write", restart_key_changed_callback)
	tk.Entry(window, textvariable=restart_key, width=1).pack(anchor=tk.W, padx=5, side='left')
	tk.Label(window, text='Starting Key').pack(anchor=tk.W, side='left')

	listbox = tk.Listbox(window)
	listbox.bind('<<ListboxSelect>>', onselect_callback)
	listbox.pack()
	window.mainloop()  # keep gui running

	data["game_keys"] = [game_keys, mouse_var.get(), restart_key.get()]


def end_game_callback(event):
	if event.Key == "Oem_3":  # the char: ~
		window.focus_force()
		hm.UnhookKeyboard()  # relese the hook
		window.destroy()
	return 1  # reList the char


def wait_for_end_game():
	global hm
	global window

	# create a hook manager
	hm = HookManager()
	# watch for all mouse events
	hm.KeyDown = end_game_callback
	# set the hook
	hm.HookKeyboard()
	# wait for window
	window = create_window("game_config", "now start the game and when you fail press: " + FLAG_KEY)
	window.mainloop()


# on click call back for get_restart_cords
def restart_callback(event):
	global restart_cords

	restart_cords = [event.x, event.y]
	sleep(0.5)
	window.destroy()


def get_restart_cords(np_imp, data):
	global canvas, height, width
	global window
	global restart_cords  # keep screen cords

	window = create_window("game_config", "Now click the restart button")
	shape = np_imp.shape
	height = shape[0]
	width = shape[1]
	# crate new canvas
	canvas = tk.Canvas(window, width=width, height=height)
	canvas.pack()

	# convert to ImageTk object for canvas
	photo = PIL.ImageTk.PhotoImage(image=Image.fromarray(np_imp))
	canvas.create_image(0, 0, image=photo, anchor=tk.NW)
	canvas.bind("<Button-1>", restart_callback)

	# keep gui running
	window.mainloop()

	data["restart_cords"] = restart_cords


def create_window(class_name, text):
	new_window = tk.Tk(className=class_name)
	tk.Label(new_window, text=text, width=100, height=0).pack()
	return new_window


def read_button_callback():
	global choice
	choice = "Read"
	win.destroy()


def write_button_callback():
	global choice
	choice = "New"
	win.destroy()


def create_read_write_window():
	global win


def get_game_window_name():
	win_name = "google"
	return win_name


def button_press_callback(func_to_call):
	global main_window
	main_window.destroy()
	func_to_call()
	create_main_menu(g_data)


def done_click_callback():
	main_window.destroy()


def save_click_callback():
	filename = filedialog.asksaveasfilename(title="Save config", filetypes=[("config file", "*.json")])
	config_handler.write_options(filename, g_data)


def load_click_callback():
	global g_data
	filename = filedialog.askopenfile(title="Load config", filetypes=[("config file", "*.json")])
	temp_data = config_handler.read_options(filename)
	for key in temp_data.keys():
		g_data[key] = temp_data[key]
	main_window.destroy()
	create_main_menu(g_data)


def create_main_menu(data):
	global main_window
	global g_data
	g_data = data
	main_window = tk.Tk(className=' Main Menu')
	main_window.configure(bg='#336699')
	data["win_name"] = get_game_window_name()
	win_np_img = np.array(image_proc.get_screen_image(win_name=data["win_name"]))
	# game frame
	game_border_button = tk.Button(main_window, text="Set game's border", command=lambda: button_press_callback(
		lambda: get_frame_cords("click on the game's border corners", win_np_img, data, 'frame_cords')), bg='red')
	game_border_button.grid(row=0, pady=3, padx=2)
	if "frame_cords" in data.keys():
		game_image = ImageTk.PhotoImage(Image.fromarray(image_proc.crop_image(win_np_img, data["frame_cords"])))
		panel = tk.Label(main_window, image=game_image)
		panel.grid(row=1, pady=3, padx=2)
		game_border_button.configure(bg='green')

	# game keys
	keys_button = tk.Button(main_window, text="Set game's keys",
							command=lambda: button_press_callback(lambda: get_game_keys(data)), bg='red')
	keys_button.grid(row=0, column=1, pady=3, padx=2)
	if "game_keys" in data.keys():

		keys_listbox = tk.Listbox(main_window)
		keys_listbox_height = len(data["game_keys"][0])
		for key in data["game_keys"][0]:
			keys_listbox.insert(tk.END, key)
		if data["game_keys"][1]:
			keys_listbox.insert(tk.END, '<Mouse>')
			keys_listbox_height += 1
		if data["game_keys"][2] != '':
			keys_listbox.insert(tk.END, 'starting  key: ' + (
				data["game_keys"][2] if data["game_keys"][2] != ' ' else '<space>'))
			keys_listbox_height += 1
		keys_listbox.configure(height=keys_listbox_height)
		keys_listbox.grid(row=1, column=1, pady=3, padx=2)
		keys_button.configure(bg='green')

	# end game image and cords
	end_game_button = tk.Button(main_window, text="Set end game's border", command=lambda: button_press_callback(
		lambda: get_frame_cords("click on the unique end game border corners", win_np_img, data, "end_game_cords")),
								bg='red')
	end_game_button.grid(row=2, pady=3, padx=4)
	if "end_game_cords" in data.keys():
		end_game_image_temp = image_proc.crop_image(win_np_img, data["end_game_cords"])
		data["end_game_img"] = end_game_image_temp
		end_game_image = ImageTk.PhotoImage(Image.fromarray(end_game_image_temp))
		end_game_panel = tk.Label(main_window, image=end_game_image)
		end_game_panel.grid(row=3, pady=3, padx=2)
		end_game_button.configure(bg='green')

	# score board cords
	score_button = tk.Button(main_window, text="Set score board's border", command=lambda: button_press_callback(
		lambda: get_frame_cords("click on the score border corners", win_np_img, data, "score_board_cords")), bg='red')
	score_button.grid(row=2, column=1, pady=3, padx=4)
	if "score_board_cords" in data.keys():
		score_image = ImageTk.PhotoImage(Image.fromarray(image_proc.crop_image(win_np_img, data["score_board_cords"])))
		score_panel = tk.Label(main_window, image=score_image)
		score_panel.grid(row=3, column=1, pady=3, padx=2)
		score_button.configure(bg='green')

	# restart cords
	restart_button = tk.Button(main_window, text="Set restart button cords",
							   command=lambda: button_press_callback(lambda: get_restart_cords(win_np_img, data)),
							   bg='red')
	restart_button.grid(row=4, column=0, pady=3, padx=4)
	if "restart_cords" in data.keys():
		restart_button.configure(bg='green')

	# save button
	save_button = tk.Button(main_window, text="Save Config", command=save_click_callback)
	save_button.grid(row=6, column=1, pady=3, padx=4)

	# load button
	load_button = tk.Button(main_window, text="Load Config", command=load_click_callback)
	load_button.grid(row=6, column=0, pady=3, padx=4)

	# done button
	done_button = tk.Button(main_window, text="Done", bg='red')
	done_button.grid(row=7, column=0, columnspan=2, pady=3, padx=4)
	if set(["restart_cords", "score_board_cords", "end_game_cords", "game_keys", "frame_cords"]).issubset(
			set(data.keys())):
		done_button.configure(bg='green', command=done_click_callback)

	main_window.mainloop()
