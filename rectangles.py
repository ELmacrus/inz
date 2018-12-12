import numpy as np
import cv2


def extract_bottom_pixel(left_top, right_bottom):

	distance = right_bottom[0]-left_top[0]

	#print distance
	center_bottom_rectangle_pixel = (right_bottom[1]-1, int(right_bottom[0]-(distance/2)-1))

	#print center_bottom_rectangle_pixel

	return center_bottom_rectangle_pixel







