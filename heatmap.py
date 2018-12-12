def create_heatmap(heatmap_img, pixels):

	colors = dict()
	i=0
	for g in range(0, 255, 25):
		colors[i] = (0, 255-g, 255)
		i += 1


	interval = len(set(pixels.values()))/10.0

	for px in pixels.keys():

		pixel_value = pixels[px]
		try:
			heatmap_img[px] = colors[int(pixel_value/interval)]
		except KeyError:
			heatmap_img[px] = colors[10]
		except IndexError:
			pass

	return heatmap_img