from stone_recognition import ImagePro

img1 = ImagePro('stone_detection3.png')
img1.get_marking_param()
img1.mark_found_objects()
print("number of objects found is: ", len(img1.found_list))
img1.show_marked()
