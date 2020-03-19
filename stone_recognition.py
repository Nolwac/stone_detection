import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

           
def compare(a, b, condition=">"):
    """This static method compares two values which are either list or an integer or float value"""
    try:
        length_a = len(a)
        if condition == ">":
            truth_value = (a>b).all()
        elif condition == "<":
            truth_value = (a<b).all()
    except:
        if condition == ">":
            truth_value = a > b
        elif condition == "<":
            truth_value = a < b
    return truth_value
  
def check_forward(obj, start, end, min_hex_value, found=False):
    """Checks the image for sign of object in a forward direction"""
    if compare(obj[start + 1], min_hex_value) and (len(obj)-1) >= (start +1):
        found = True
        return check_forward(obj, (start + 1), end, min_hex_value, found)
    elif (start < end) and (len(obj)-1) >= (start +1):
        return check_forward(obj, (start + 1), end, min_hex_value, found)
    else:
        return (start, found)
        
def check_backward(obj, start, end, min_hex_value, found=False):
    """Checks the image for sign of object in a forward direction"""
    if compare(obj[start - 1], min_hex_value) and (0 <= (start -1)):
        found = True
        return check_backward(obj, (start - 1), end, min_hex_value, found)
    elif (end < start) and (0 <= (start -1)):
        return check_backward(obj, (start - 1), end, min_hex_value, found)
    else:
        return (start, found)
        
def check_downward(obj, start, end, min_hex_value):
    if compare(obj[start + 1][end], min_hex_value) and ((len(obj)-1) > (start + 1)) and (len(obj[start + 1]-1) > end):
        return True
    else:
        return False
    
class ImagePro(object):
    def __init__(self, image):
        self.image_file = image
        self.image = Image.open(image)
        self.image = np.asarray(self.image)
        self.marked_image = self.image.tolist()#changing to list to allow editing
        self.found_list = []

    def mark(self, start_x, end_x, start_y, end_y, marking_width, marking_color=[0, 255, 0]):
        """This function marks a part of the image that is specified"""
        length_x = end_x - start_x
        length_y = end_y - start_y
        try:
            marking_color_len=len(marking_color)
        except:
            marking_color_len = 2
        if not marking_color_len == len(self.image.shape):
            raise Exception("The color value you provided is not appropriate for the image")
        else:
            static_start_x = start_x #a copy of start_x
            static_start_y = start_y #a copy of start_y
            for n in range(marking_width): #this is a hack to increase marking width
                for i in range(start_y, (start_y + length_y + marking_width)):
                    if len(self.marked_image)-1 >= i:
                        self.marked_image[i][start_x] = marking_color
                        if len(self.marked_image[i])-1 >= (start_x + length_x):
                            self.marked_image[i][(start_x + length_x)] = marking_color
                    else:
                        break
                start_x = start_x + 1
            start_x = static_start_x
            for n in range(marking_width): #a hack to increase marking width
                for i in range(start_x, (start_x + length_x + marking_width)):
                    if len(self.marked_image[start_y])-1 >= i:
                        self.marked_image[start_y][i] = marking_color #changing the rgb color at that point
                        if len(self.marked_image)-1 >= (start_y + length_y):
                            self.marked_image[(start_y + length_y)][i] = marking_color #changing the rgb color at that point
                    else:
                        break
                start_y = start_y + 1 #incrementing so as to increase the marking width
            start_y = static_start_y #returning to the original value
            
    def mark_found_objects(self, marking_width=3, marking_color=[0, 255, 0]):
        for obj in self.found_list:
            self.mark(obj[0], obj[1], obj[2], obj[3], marking_width, marking_color)
        return "Successfully marked"
    
    def get_marking_param(self, min_hex_value=[100,100,100]):
        try:
            hex_color_len=len(min_hex_value)
        except:
            hex_color_len = 2
        if not hex_color_len == len(self.image.shape):
            raise Exception("The color value you provided is not appropriate for the image")
        available = False
        print("initializing object search...")
        for i, y in enumerate(self.image):
            for j, x in enumerate(y):
                if compare(x, min_hex_value):
                    start_x = j
                    start_y = i
                    available = True
                    print(start_x, start_y, "initial points")
                    break
            if available:
                break
        if available == True:
            print("Object search initiated, search started.")
            self.find_params(start_x, start_y, min_hex_value)
            
    def next_object(self, start_x, end_x, start_y, end_y, min_hex_value):
        available = False
        for i, y in enumerate(self.image):
            for j, x in enumerate(y):
                if start_y <= i:
                    if self.is_point_not_in_object_list(j, i):
                    #if ((j < start_x and i > start_y) or (j > end_x and i >= start_y)) or (i > end_y):
                        if compare(x, min_hex_value):
                            newstart_x = j
                            newstart_y = i
                            available = True
                            break
            if available:
                break
        if available == True:
            self.find_params(newstart_x, newstart_y, min_hex_value)
        else:
            print("no more object to find params for")
            
    def is_point_not_in_object_list(self, x, y):
        for i, obj in enumerate(self.found_list):
            start_x, end_x, start_y, end_y = obj[0], obj[1], obj[2], obj[3]
            #if not (((x < start_x and y > start_y) or (x > end_x and y >= start_y)) or (y > end_y)):
            if (((x >= start_x) and (x <= end_x)) and ((y >= start_y) and (y <= end_y))):
                return False
        return True
    
    def find_params4(self, start_x, start_y, min_hex_value):
        end_x, found_forward = check_forward(self.image[start_y], start_x, start_x, min_hex_value)
        present_position = end_x
        start_x, found_backward = check_backward(self.image[start_y], present_position, start_x, min_hex_value)
        present_position = start_x
        found_downward = True
        end_y = start_y
        while found_downward:
            found_downward = check_downward(self.image, end_y, present_position, min_hex_value)
            end_y = end_y + 1
        
        print(found_downward, "is found downward", end_y)
        if not len(self.found_list)>15:
            self.found_list.append([start_x, end_x, start_y, end_y])
            self.next_object(start_x, end_x, start_y, end_y, min_hex_value)
    
    def find_params(self, start_x, start_y, min_hex_value):
        """This method finds the position parameter of a detected object in an image"""
        found=True
        end_x = start_x
        present_position = start_x
        end_y = start_y
        self.backward, self.forward = True, False
        #not ((self.backward and self.forward) and not found)
        while found:
            if not end_y == start_y:
                found_downward = check_downward(self.image, end_y, present_position, min_hex_value)
                end_y = end_y + 1
                end_x, found_forward = check_forward(self.image[end_y], present_position, end_x, min_hex_value)
                present_position = end_x
                start_x, found_backward = check_backward(self.image[end_y], present_position, start_x, min_hex_value)
                present_position = start_x
                found = (found_forward or found_backward or found_downward)
            else:
                end_x, found_forward = check_forward(self.image[end_y], present_position, end_x, min_hex_value)
                present_position = end_x
                start_x, found_backward = check_backward(self.image[end_y], present_position, start_x, min_hex_value)
                present_position = start_x
                found_downward = check_downward(self.image, end_y, present_position, min_hex_value)
                end_y = end_y + 1
                found = (found_forward or found_backward or found_downward)
            if len(self.image)-1 < end_y:
                break
        print("Found object number ", len(self.found_list)+1)
        print("Still searching please wait...")
        self.found_list.append([start_x, end_x, start_y, end_y])
        self.next_object(start_x, end_x, start_y, end_y, min_hex_value)
           
    def clear_mark(self):
        """Unmarks the image by taking it back to what it was earlier"""
        self.marked_image = self.image.tolist()

    def show_marked(self):
        """Shows the marked image"""
        plt.imshow(self.marked_image)
        plt.show()
