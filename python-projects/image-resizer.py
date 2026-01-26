import cv2

userImage = input("Enter the name of the image with '.' extension: ")

# Configurables
source = f"{userImage}"
destination = "newImage.png"
scale_percent = 12.5

# To open the file
src = cv2.imread(source, cv2.IMREAD_UNCHANGED)

# Calculate the new widhts and new heights
new_width = int(src.shape[1] * scale_percent / 100)
new_height = int(src.shape[0] * scale_percent / 100)

# Final Image
output = cv2.resize(src, (new_width , new_height))

cv2.imwrite(destination, output)
