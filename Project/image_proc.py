import cv2
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import win32gui
import time
import matplotlib.pyplot as plt


def compare_images(imageA, imageB):
	return np.array_equal(imageA, imageB)


def enum_cb(hwnd, results):
	results.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_filtered_screen_image(img, size=16):
	edges = cv2.Canny(np.array(img), 100, 200)
	places = [0] * (size * size)
	height = edges.shape[0]
	width = edges.shape[1]
	height_ratio = size / height
	width_ratio = size / width
	indexes = np.where(edges == 255)
	height_indexes = indexes[0] * height_ratio
	width_indexes = indexes[1] * width_ratio
	for i, j in zip(height_indexes, width_indexes):
		places[int(i) * size + int(j)] = 1
	return tuple(places)


def crop_image(img, bbox):
	if type(img) is np.ndarray:
		return img[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
	return img.crop(tuple(bbox[0] + bbox[1]))


def get_screen_image(points=None, win_name="google"):
	open_win(win_name)
	curr_bbox = get_bbox()
	if points:
		img = ImageGrab.grab(tuple(points[0] + points[1]))
	else:
		img = ImageGrab.grab()
	return img


def get_bbox(window_name="google"):
	hwnd = open_win(window_name)  # make generic
	return win32gui.GetWindowRect(hwnd)


# open a window to the screen
def open_win(win_name):
	winlist = []
	win32gui.EnumWindows(enum_cb, winlist)
	hwnd = [(hwnd, title) for hwnd, title in winlist if win_name in title.lower()][0][0]
	win32gui.SetForegroundWindow(hwnd)
	time.sleep(0.2)
	return hwnd


def get_string_from_image(np_img):
	gray_np_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
	(thresh, binary_np_img) = cv2.threshold(gray_np_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	binary_np_img = crop_white_paddings(binary_np_img)
	ratio = binary_np_img.shape[1] / binary_np_img.shape[0]
	binary_np_img = cv2.resize(binary_np_img, (int(500 * ratio), 500))
	return pytesseract.image_to_string(binary_np_img, config='-psm 10000 digits')


def crop_white_paddings(np_img):
	indexes = np.where(np_img != 255)
	if indexes is None:
		return None
	min_x = min(indexes[1]) - 2
	min_y = min(indexes[0]) - 2
	max_x = max(indexes[1]) + 2
	max_y = max(indexes[0]) + 2

	crop_img = np_img[min_y:max_y, min_x:max_x]
	return crop_img


def change_white_to_black(np_img):
	gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)

	ret, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
	np_img[thresh == 255] = 0
	np_img[thresh != 255] = 255
	return np_img
