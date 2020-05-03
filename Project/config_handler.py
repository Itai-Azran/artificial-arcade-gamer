import json
import numpy as np
import Key


def read_options(filename):
	with open(str(filename.name), 'r') as json_file:
		data = json.load(json_file)
	if "end_game_img" in data.keys():
		data["end_game_img"] = np.array(data["end_game_img"])
	if "game_keys" in data.keys():
		for i in range(len(data["game_keys"][0])):
			data["game_keys"][0][i] = Key.Key(data["game_keys"][0][i][0], data["game_keys"][0][i][1])
	return data


def write_options(filename, data):
	filtered_data = data.copy()
	if "end_game_img" in filtered_data.keys():
		filtered_data["end_game_img"] = data["end_game_img"].tolist()
	if "game_keys" in filtered_data.keys():
		print(filtered_data["game_keys"])
		filtered_data["game_keys"] = [[''] * len(data["game_keys"][0])] + data["game_keys"][1:]
		for i in range(len(data["game_keys"][0])):
			filtered_data["game_keys"][0][i] = data["game_keys"][0][i].get_serialized_key()
		print(filtered_data)
	with open(filename + ('' if filename.endswith('.json') else '.json'), 'w') as outfile:
		json.dump(filtered_data, outfile)
