import sys
from PIL import Image


def dot2braille(*args):
    A = args[0]

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
# print(dot2braille(0, 1, 0, 1, 0, 1, 0, 1))


def render(img_path: str, img_scale: float):
    img = Image.open(img_path)
    w, h = img.size
    img = img.resize((int(w * img_scale), int(h * img_scale)))
    w, h = img.size
    '''Dividing the image into chunks,
    each chunk is assigned a symbol
    and writes it instead of drawing pixels.'''
    block_w, block_h = 2, 4
    with open("result.txt", "w", encoding="utf-8") as f:
        for y in range(0, h, block_h):
            for x in range(0, w, block_w):
                block = [0] * 8  # The chunk is encoded with 8 bits.
                for j in range(0, min(block_h, h - y)):
                    for i in range(0, min(block_w, w - x)):
                        px = img.getpixel((x + i, y + j))
                        '''Depending on the brightness of the pixels,
                        parse the symbol from zeros and ones sequence.'''
                        block[i * j] = ((0.2126*px[0]) +
                                        (0.7152*px[1]) + (0.0722*px[2])) < 200
                f.write(dot2braille(block))
            f.write('\n')


if __name__ == '__main__':
    try:
        render(sys.argv[1], float(sys.argv[2]))
        print("[+]Done!")
    except FileNotFoundError:
        print(f'[-]No such file: {sys.argv[1]}')
        sys.exit(1)
    except IndexError:
        print("[-]You did not specify scale or image")
        sys.exit(1)
