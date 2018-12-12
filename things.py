import numpy as np
import cv2
import datetime


def get_now_string():
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    ret_string = '{}_{}_{}_{}_{}.png'.format(year, month, day, hour, minute)
    return ret_string


