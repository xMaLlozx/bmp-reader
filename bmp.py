from dataclasses import dataclass
# import sys
# sizeof = lambda a: sys.getsizeof(a)

@dataclass
class FileHeader:
    is_bmp:     bytes
    size:       int
    field:      int
    pix_offset: int

    # def __str__(self):
    # 	return f"is bmp: {self.is_bmp=}\n" \
			 #   f"size: {self.size=}\n" \
			 #   f"field: {self.field=}\n" \
			 #   f"pixel offset: {self.pix_offset=}\n"

@dataclass
class DIBHeader:
    size_header:   int # in bytes(=40)
    width:         int
    height:        int
    layers:        int # must be 1
    bit_per_pixel: int
    comp:          int
    data_size:     int # or 0
    pwidth:        int # pix/m
    pheight:       int # pix/m
    colors_count:  int # Количество используемых цветов
    important:     int # Количество "важных" цветов.

    # def __str__(self):
    # 	return f"size header: {self.size_header}\n" \
			 #   f"width: {self.width}\n" \
			 #   f"height: {self.height}\n" \
			 #   f"layers: {self.layers}\n" \
			 #   f"bits per pixel: {self.bit_per_pixel}\n" \
			 #   f"comp: {self.comp}\n" \
			 #   f"data size: {self.data_size}\n" \
			 #   f"pwidth: {self.pwidth}\n" \
			 #   f"pheight: {self.pheight}\n" \
			 #   f"colors count: {self.colors_count}\n" \
			 #   f"important: {self.important}\n" \

@dataclass
class BMPFile:
	bmp: FileHeader
	dib: DIBHeader
	data: bytes # in file must be write like bgr

	def __str__(self):
		dibh = self.dib
		out = ""
		out += f"BMP header: {self.bmp}\n"\
			f"DIB header: {self.dib}\n"\
			f"BMP data:\n"\
			'%-4c:%2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x'%('-', *range(16))
		for i in range(dibh.data_size):
			if i % 16 == 0:
				out += f'\n{i:<4x}:'
			if bmp.data[i] != 0:
				out += f'{bmp.data[i]:>2x} '
			else:
				out += '%02x '%bmp.data[i]
		return out

class BMP:
	img = None
	pixels = []
	def __init__(self, path: str): # valid path or file
		self.readBMP(path)

	def getPixels(self, f):
		header     = self.img.bmp
		header_dib = self.img.dib
		f.seek(header.pix_offset)
	
		pixels = []
		line_bytes = (header_dib.width * header_dib.bit_per_pixel + 31) // 32 * 4
		for y in range(header_dib.height):
			for x in range(header_dib.width):
				pixel_data = f.read(header_dib.bit_per_pixel // 8)
				pixel = [int.from_bytes(pixel_data[i:i+1], 'little') for i in range(header_dib.bit_per_pixel // 8)] # or tuple(), not ()
				pixels.append(pixel)
			f.read(line_bytes - header_dib.width * (header_dib.bit_per_pixel // 8))
		self.pixels = pixels

	def readBMP(self, path: str):
		with open(path, 'rb') as f:
			header = FileHeader(
				is_bmp     = f.read(2),
				size       = int.from_bytes(f.read(4), "little"),
				field      = int.from_bytes(f.read(4), "little"),
				pix_offset = int.from_bytes(f.read(4), "little")
			)
			dib = DIBHeader(
				size_header   = int.from_bytes(f.read(4), "little"),
				width         = int.from_bytes(f.read(4), "little"),
				height        = int.from_bytes(f.read(4), "little"),
				layers        = int.from_bytes(f.read(2), "little"),
				bit_per_pixel = int.from_bytes(f.read(2), "little"),
				comp          = int.from_bytes(f.read(4), "little"),
				data_size     = int.from_bytes(f.read(4), "little"),
				pwidth        = int.from_bytes(f.read(4), "little"),
				pheight       = int.from_bytes(f.read(4), "little"),
				colors_count  = int.from_bytes(f.read(4), "little"),
				important     = int.from_bytes(f.read(4), "little")
			)
		
			f.seek(header.pix_offset) # print(f.tell())
			bmp = BMPFile(
				bmp  = header,
				dib  = dib,
				data = f.read(dib.data_size)
			)
			self.img = bmp
			self.getPixels(f)

if __name__ == '__main__':
	bmp = BMP('test.bmp') # 4x4
	print(bmp.pixels)