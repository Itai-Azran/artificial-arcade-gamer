import gui_utils
import AI_utils

data = {}
try:
	gui_utils.create_main_menu(data)
except Exception as e:
	print("Config error occurred:", e)

try:
	AI_utils.run(data)
except Exception as e:
	print("Run error occurred:", e)

print("End")
