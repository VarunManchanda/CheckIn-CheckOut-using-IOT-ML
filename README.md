# CheckIn-CheckOut-using-IOT-ML
This Project basically deals with Check In - Check Out of person by performing Face Detection and Recognition process using Haar-Cascade file.
H/W required:-
1)Raspberry Pi(3 or 4)
2)Raspberry picamera
3)Ethernet Cable
4)Laptop 
S/W required:-
1)openCV
2)Python2
To run this Project, just run projectFirst.py file.
How it is Working?
-> In saveDetails method first camera is opened and it captures 10 images in different-different ways, after that it maps with haar_cascade file and store output of it in ".yml" file.
->In checkIn method camera capture your photo and then recognise it using the above saved ".yml" file, if found then it makes your entry in a dictionary where key is your id and value is your current timestamp.
-> In checkOut method camera once again capture your photo and find your id using ".yml" file if found using that id it will extract your timestamp value saved in above dictionary and subtract current time, to show how much time you were invloved.
