import cv2
import numpy
import importlib
import os

try:  ## check if a directory exist, if not create an output directory.
    os.mkdir("output")
except : pass 


# params:
size_of_board = [100, 100, 100, 30, 100, 30]
board_start_mode = [1, 2, 4, 0, 0, 0]
probability = [5000,8000]
rle = ["", "", "", "7bo6b$6bobo5b$7bo6b2$5b5o4b$4bo5bob2o$3bob2o3bob2o$3bobo2bobo3b$2obo3b2obo3b$2obo5bo4b$4b5o5b2$"
       "6bo7b$5bobo6b$6bo!", "5b3o11b3o5b$4bo3bo9bo3bo4b$3b2o4bo7bo4b2o3b$2bobob2ob2o5b2ob2obobo2b$"
       "b2obo4bob2ob2obo4bob2ob$o4bo3bo2bobo2bo3bo4bo$12bobo12b$2o7b2obobob2o7b2o$12bobo12b$6b3o9b3o6b$6bo3bo9bo6b$"
       "6bobo4b3o11b$12bo2bo4b2o5b$15bo11b$11bo3bo11b$11bo3bo11b$15bo11b$12bobo!", "7bo6b$6bobo5b$7bo6b2$5b5o4b$" 
       "4bo5bob2o$3bob2o3bob2o$3bobo2bobo3b$2obo3b2obo3b$2obo5bo4b$4b5o5b2$6bo7b$5bobo6b$6bo!"]
pattern_position = [0, 0, 0, (4, 13), (40, 40), (4, 13)]
rules = ["B36/S23", "B45/S23", "B3/S23", "B3/S23", "B3/S23", "B3/S23"]
I = [0, 0, 270, 20, 180, 0]



######################################################################################################
######################################################################################################
flag=True
while flag:
    print("Please enter a file name:")
    File=input()

    if not (File.isdigit()):
        print("File name is invalid! The file name should be your identity number")
    else:
        flag=False
######################################################################################################
######################################################################################################

## import the py file:
Module = importlib.import_module(File)
Output = File
Output += "-test"
print(Output)
numpy.random.seed(seed=1)
GOL = Module.GameOfLife(size_of_board[0], board_start_mode[0], rules[0],rle[0],pattern_position[0])
if not(isinstance(GOL.return_board(),list)):
    print("Warning Board type must be list type!")
for j in range(len(I)):
    test_number=str(j+1)
    try:
        GOL = Module.GameOfLife(size_of_board[j], board_start_mode[j], rules[j],rle[j],pattern_position[j])
        for i in range(I[j]):
            GOL.update()
            board = GOL.return_board()
        board = GOL.return_board()
        if(j<2):
            alive = numpy.sum(board)
            alive = alive / 255
            if probability[j]*1.1>alive and probability[j]*0.9<alive:
                print("Test number-", test_number, "pass")
            else:
                print("Test number-", test_number, "Failed:the Board was not properly started")
        else:
            GOL.save_board_to_file("output/OutImage" + str(test_number) + ".png")
            imge_test_path = "test/test" + test_number + ".png"
            image_test = cv2.imread(imge_test_path, cv2.IMREAD_GRAYSCALE)
            (thresh, im_bw) = cv2.threshold(image_test, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # make a list from the test image.
            image_test_arr = numpy.array(im_bw)
            check1 = numpy.array_equal(image_test_arr, board)  # checks if the lists are equals
            image_test = cv2.imread(imge_test_path)
            image_output = cv2.imread("output/OutImage" + str(test_number) + ".png")
            image_test_arr = numpy.array(image_test)
            image_output_arr = numpy.array(image_output)
            check2 = numpy.array_equal(image_test_arr, image_output_arr)  # checks if the images are equals
            if check2&check1:
                print("Test number-", test_number, "pass")
            else:
                print("Test number-", test_number, "Failed:The board is the same?-",check1," The image is the same?-", check2)
    except Exception as e:  # if the code is crashing report it
        print("Test Number ",test_number,": crashed-", e)
