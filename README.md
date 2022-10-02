# Analog Clock Time Reader
Reading the time from an analog clock image with openCV

Simple python script reads only one image, however it can be easily adapted for real-time use

Original image example:

![img](https://user-images.githubusercontent.com/83359345/193447369-953ea5d0-6017-4a56-8254-c5001fcf5c82.png)

Hough circle detection:

<img width="1062" alt="image" src="https://user-images.githubusercontent.com/83359345/193446527-fde1f564-c7cf-406a-b4c0-7fe4b14794a7.png">

Cropping from the biggest circle detected

<img width="632" alt="image" src="https://user-images.githubusercontent.com/83359345/193446568-7e2210eb-381d-4d9e-ac96-cf3ab7b10bab.png">

Polar Warp

<img width="376" alt="image" src="https://user-images.githubusercontent.com/83359345/193446788-ab418272-bf5b-4895-a4ee-3a7036f5cc8a.png">

Dilation with a (1,80) kernel to erase the numbers

<img width="456" alt="image" src="https://user-images.githubusercontent.com/83359345/193446801-6defa1cf-f498-4436-8835-5c4763559dc4.png">

Thresholding

<img width="360" alt="image" src="https://user-images.githubusercontent.com/83359345/193446815-a328df9d-f87f-439b-8ef6-70248171b04f.png">

Contours are searched and then hands are filtered by area and height in the image

Final print example:

<img width="65" alt="image" src="https://user-images.githubusercontent.com/83359345/193447041-e23e6972-6ea2-42af-b444-f199488a8c37.png">

*code will crash if one of the hands isn't visible, needs some error handling
