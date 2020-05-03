from pyautogui import press, keyDown, keyUp


class Key:
	def __init__(self, key, is_hold=True):
		self.key = key
		self.is_hold = is_hold
		if is_hold:
			self.pressing_function = keyDown
			self.unpressing_function = keyUp
		else:
			self.pressing_function = press
			self.unpressing_function = empty_function

	def switch_pressing_function(self):
		if self.is_hold:
			self.pressing_function = press
			self.unpressing_function = empty_function
		else:
			self.pressing_function = keyDown
			self.unpressing_function = keyUp
		self.is_hold = not self.is_hold

	def __repr__(self):
		return (self.key if self.key != ' ' else '<space>') + ' ' + ('<Hold>' if self.is_hold else '<Press>')

	def __str__(self):
		return repr(self)

	def press(self):
		self.pressing_function(self.key)

	def unpress(self):
		self.unpressing_function(self.key)

	def get_serialized_key(self):
		return self.key, self.is_hold


def empty_function(*_):
	pass
