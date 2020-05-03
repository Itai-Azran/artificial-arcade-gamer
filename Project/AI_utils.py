import os
import neat
import visualize
from pyautogui import click, press, keyDown, keyUp, mouseDown, mouseUp
import image_proc
import gui_utils
import numpy as np
from time import sleep
from pyHook import HookManager

NUM_OF_GENERATIONS = 30
PRESS_THRESHOLD = 0.5

PRESSING_COUNTER_TOTAL = 0
PRESSING_COUNTER_PRESSED = 1


# eval fitness for each genome
def eval_genomes(genomes, config):
	global pressing_counter
	index = 0
	image_proc.open_win(win_name)
	for genome_id, genome in genomes:
		pressing_counter = [1, 1]
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		restart()
		while True:
			curr_img = image_proc.get_screen_image(win_name=win_name)
			if is_end_game(curr_img):
				fitness = get_score()
				if fitness is None:
					print('Invalid Score, rerunning last genome')
					restart()
					continue
				genome.fitness = fitness
				print(str(index) + ": ", genome.fitness)
				index += 1
				break

			outputs = net.activate(image_proc.get_filtered_screen_image(image_proc.crop_image(curr_img, frame_cords)))
			press_buttons(outputs)


def run(data):
	global frame_cords, game_keys, end_game_cords, end_game_img, score_board_cords, restart_cords, is_mouse, win_name, start_key
	frame_cords = data["frame_cords"]
	game_keys = data["game_keys"][0]
	print(data["game_keys"])
	is_mouse = data["game_keys"][1]
	end_game_cords = data["end_game_cords"]
	end_game_img = data["end_game_img"]
	score_board_cords = data["score_board_cords"]
	restart_cords = data["restart_cords"]
	win_name = data["win_name"]
	start_key = data["game_keys"][2]
	print('creating file')
	# save configuration      calculating the size                                                         len of keys
	create_config_file((frame_cords[1][0] - frame_cords[0][0]) * (frame_cords[1][1] - frame_cords[0][1]),
					   len(game_keys) + 3 * is_mouse)
	print('done')

	print('loading file')
	# Load configuration.
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 get_full_file_path('config'))
	print('done')

	print('creating pop')
	# Create the population, which is the top-level object for a NEAT run.
	p = neat.Population(config)
	print('done')

	# Add a stdout reporter to show progress in the terminal.
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	stop_game()

	print('running')
	# Run for up to constant num of generations.
	winner = p.run(eval_genomes, NUM_OF_GENERATIONS)

	# Display the winning genome.
	print('\nBest genome:\n{!s}'.format(winner))
	visualize.draw_net(config, winner, True)


def create_config_file(num_of_inputs, num_of_outputs):
	config_template_file = open('config_template', 'r')
	config_template_file_str = config_template_file.read()
	config_template_file.close()

	config_template_file_str = config_template_file_str.replace('%%inputs%%', str(num_of_inputs))
	config_template_file_str = config_template_file_str.replace('%%outputs%%', str(num_of_outputs))
	config_file = open('config', 'w')
	config_file.write(config_template_file_str)
	config_file.close()


def get_full_file_path(file_name):
	local_dir = os.path.dirname(__file__)
	return os.path.join(local_dir, file_name)


def restart(click_start_game_cords=None):
	sleep(0.5)
	click(restart_cords[0], restart_cords[1])
	if click_start_game_cords:
		sleep(1)
		click(click_start_game_cords[0], click_start_game_cords[1])
	if start_key != '':
		sleep(0.4)
		press(start_key)


def get_score():
	curr_score = image_proc.get_string_from_image(np.array(image_proc.get_screen_image(points=score_board_cords)))
	if curr_score == "":
		sleep(0.2)
		curr_score = image_proc.get_string_from_image(
			image_proc.change_white_to_black(np.array(image_proc.get_screen_image(points=score_board_cords))))
		if curr_score == "":
			return None
	score = int(curr_score) * (
	1 - (pressing_counter[PRESSING_COUNTER_PRESSED] / pressing_counter[PRESSING_COUNTER_TOTAL] / 10))
	return score


def is_end_game(curr_image):
	np_img = np.array(image_proc.crop_image(curr_image, end_game_cords))
	return image_proc.compare_images(end_game_img, np_img)


def press_buttons(outputs):
	pressing_counter[PRESSING_COUNTER_TOTAL] += 1
	for i in range(len(outputs) - 3 * is_mouse):
		if outputs[i] > PRESS_THRESHOLD:
			game_keys[i].press()
			pressing_counter[PRESSING_COUNTER_PRESSED] += 1
		else:
			game_keys[i].unpress()

	if is_mouse:
		x = outputs[-3] * (frame_cords[1][0] - frame_cords[0][0]) + frame_cords[0][0]  # width
		y = outputs[-2] * (frame_cords[1][1] - frame_cords[0][1]) + frame_cords[0][1]  # height
		if outputs[-1] > PRESS_THRESHOLD:
			mouseDown(x=x, y=y)
			pressing_counter[PRESSING_COUNTER_PRESSED] += 1
		else:
			mouseUp(x=x, y=y)


def destroy_stop_window_callback():
	global stop_win, pressing_counter
	stop_win = None
	pressing_counter = [0, 0]
	restart()


stop_win = None


def stop_game_callback(event):
	global stop_win
	if event.Key == "Oem_3":  # the char: ~
		if stop_win is None:
			stop_win = gui_utils.create_window("game_debug", "You can continue AAG by pressing: " + gui_utils.FLAG_KEY)
			stop_win.protocol("WM_DELETE_WINDOW", destroy_stop_window_callback)
			stop_win.mainloop()
		else:
			stop_win.destroy()
	return 1  # reList the char


# waiting for the user to click ~ in order to stop the game (called only once)
def stop_game():
	# create a hook manager
	hm = HookManager()
	# watch for all mouse events
	hm.KeyDown = stop_game_callback
	# set the hook
	hm.HookKeyboard()


def empty_function(*_):
	pass
