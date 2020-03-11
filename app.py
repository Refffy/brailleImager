import io, sys
from PIL import Image

def dot2braille(*args):
	A  = args[0]

	dots = [
		A[7], A[6],
		A[5], A[3],
		A[1], A[4],
		A[2], A[0]
	]
	offset = 0

	for i in dots[::-1]:
		offset <<= 1
		offset |= i

	return chr(10240 + offset)
#print(dot2braille(0, 1, 0, 1, 0, 1, 0, 1))
def render():
	img_Path = sys.argv[1]
	img_Scale = float(sys.argv[2])
	img = Image.open(img_Path)
	w, h = img.size
	img = img.resize((int(w * img_Scale), int(h * img_Scale)))
	w, h = img.size
	block_w, block_h = 2, 4 #Dividing the image into chunks, each chunk is assigned a symbol and writes it instead of drawing pixels.
	with open("result.txt", "w", encoding="utf-8") as f:
		for y in range(0, h, block_h):
			for x in range(0, w, block_w):
				block = [0] * 8 #The chunk is encoded with 8 bits.
				for j in range(0, min(block_h, h - y)):
					for i in range(0, min(block_w, w - x)):
						px = img.getpixel((x + i, y + j))
						block[i * j] = ((0.2126*px[0]) + (0.7152*px[1]) + (0.0722*px[2])) < 200 #Depending on the brightness of the pixels, parse the symbol from zeros and ones.
				f.write(dot2braille(block))
			f.write('\n')
	print("Done!")
if __name__ == '__main__':
	render()