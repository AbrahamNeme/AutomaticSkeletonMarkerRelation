from PIL import Image

for i in range(433):

    img = Image.open(f"./dataset/frames-cropped/frame_{i:04d}.png")
    width,height = img.size
    left = 200
    right= width-100
    top = 20
    bottom = height - 20
    img_new = img.crop((left,top,right,bottom))

    img_new.save(f"./dataset/frames-cropped/frame_{i:04d}.png")
