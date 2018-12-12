import m3u8
import urllib
import time
import numpy as np
import imutils
import cv2
from inz.rectangles import extract_bottom_pixel as extract
from things import get_now_string
from inz.heatmap import create_heatmap


def download_new_segments():
    try:
        time.sleep(1)
        current_playlist = m3u8.load('https://cdn-3-go.toya.net.pl:8081/kamery/krak_mostdebnicki.m3u8')
        current_playlist = str(current_playlist.segments)
        playlist_lines = current_playlist.split()
        playlist_ts_files = []
        for i in range(1, len(playlist_lines), 2):
            playlist_ts_files.append(playlist_lines[i])
        return sorted(playlist_ts_files)
    except:
        return -1 #if connection lost


ts_files_set_before = set()
j = 0

segments_counter = 0

bg_subtractor = cv2.createBackgroundSubtractorMOG2()
kernel_o = np.ones((2,2),np.uint8)
kernel_c = np.ones((10,10),np.uint8)
occupied_pixels = dict()
heatmap_img = np.zeros((400,800,1), np.uint16) #full heatmap
#kernel_heatmap = np.ones((3,3),np.uint8)

start = time.time()

while True:
    if j == 0:
        set_before = set(download_new_segments())
        time.sleep(2)
        j = 1

    #set_current = set(download_new_segments())
    set_current = download_new_segments()
    if isinstance(set_current, int):
        print 'connection lost'
        continue
    set_current = set(set_current)
    diff = set_current.difference(set_before)
    print diff
    # print len(diff)
    diff_length = len(diff)
    set_before = set_current

    for segment in list(diff):
        try:
            dwn_link = 'https://cdn-3-go.toya.net.pl:8081/kamery/{}'.format(segment)
            file_name = 'trial_video_x.mp4'
            urllib.urlretrieve(dwn_link, file_name)
        except IOError:
            time.sleep(30)
            print 'handling io error'
            continue
        cap = cv2.VideoCapture(file_name)
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is None:
                break

            frame = imutils.resize(frame, width=800)
            frame = frame[200:, :]

            #video.write(frame)

            frame_fg = bg_subtractor.apply(frame)
            frame_fg_o = cv2.morphologyEx(frame_fg, cv2.MORPH_OPEN, kernel_o)
            frame_fg_o_c = cv2.morphologyEx(frame_fg_o, cv2.MORPH_CLOSE, kernel_c)

            contours = cv2.findContours(frame_fg_o_c.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]

            #forloop_time_start = time.time()
            for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)

                if cv2.contourArea(c) > 400 or cv2.contourArea(c) < 5 or h < 10 or w > 10:
                    continue

                left_top_corner = (x, y)
                right_top_corner = (x + w, y + h)

                cv2.rectangle(frame, left_top_corner, right_top_corner, (0, 255, 0), 2)

                rectangle_bottom_pixel = extract(left_top_corner, right_top_corner)
                heatmap_img[rectangle_bottom_pixel] += 1 #<--------------------------

            #cv2.imshow('frame', frame_fg_o_c)
            #cv2.imshow('frame2', frame)
            # cv2.imshow('heatmap', heatmap_img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break

    print diff_length
    #segments_counter += diff_length
    # if diff_length > 20:
    #     j = 0

    end = time.time()
    print '--------', heatmap_img.max()
    if end - start > 600:
        #heatmap_counter += 1
        #heatmap_img = create_heatmap(heatmap_img, occupied_pixels)
        #heatmap_after = cv2.morphologyEx(heatmap_img, cv2.MORPH_OPEN, kernel_heatmap)
        #cv2.imwrite('heatmap_1720_1920_no_{}_after.png'.format(heatmap_counter), heatmap_after)
        #cv2.imwrite('heatmap_1720_1920_no_{}.png'.format(heatmap_counter), heatmap_img)
       # print 'saving heatmap no {}'.format(heatmap_counter)
        #print segments_counter
        print heatmap_img.max()
        heatmap_img = cv2.convertScaleAbs(heatmap_img)
        heatmap = cv2.applyColorMap(heatmap_img, cv2.COLORMAP_HOT)
        # file_numpy = open('heatmap_numpy_array', 'a')
        # file_numpy.write(heatmap)
        # file_numpy.close()
        heatmap_name = get_now_string()

        cv2.imwrite(heatmap_name, heatmap)

        print heatmap.max()
        start = time.time()
    if heatmap_img.max() > 60000:
        break


heatmap = cv2.applyColorMap(heatmap_img, cv2.COLORMAP_HOT)
cv2.imshow('res', heatmap)
cv2.imwrite('heatmap2.png', heatmap)
cv2.waitKey(0)
print heatmap.max()