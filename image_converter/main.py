import argparse
import math
import os
from typing import List
from wand.image import Image

class SubImage():
    def __init__(self, x_idx, y_idx, x_range, y_range):
        self.x_idx = x_idx
        self.y_idx = y_idx
        self.x_range = x_range
        self.y_range = y_range

    def x_slice(self):
        return slice(self.x_range[0], self.x_range[1])

    def y_slice(self):
        return slice(self.y_range[0], self.y_range[1])

# creates structure in output_path/image_name/
def main(image_path: str, output_path: str, tile_width:int, tile_height:int):
    image_map_path = os.path.join(output_path, os.path.basename(image_path) + ".map")
    with Image(filename=image_path) as img:
        x_size, y_size = img.size
        print(f'Creating image map in {image_map_path}/')
        os.makedirs(image_map_path,exist_ok=True)

        for su in chop_images(x_size, y_size, tile_width, tile_height):
            with img[su.x_slice(), su.y_slice()] as cropped:
                #print(f'{su.x_idx}, {su.y_idx}, {su.x_slice()}, {su.y_slice()}')
                for level in range(1): # todo support for multiple resolutions
                    cur_dir = os.path.join(image_map_path, str(level), str(su.x_idx))
                    os.makedirs(cur_dir, exist_ok=True)
                    img_file = os.path.join(cur_dir, str(su.y_idx))

                    cropped_x, cropped_y = cropped.size
                    if cropped_x != tile_width or cropped_y != tile_height:
                        with Image(width=tile_width,height=tile_height) as out:
                            out.format = 'png'
                            out.composite(cropped, left=0, top=0)
                            out.save(filename=img_file)
                            continue
                    cropped.save(filename=img_file)

def chop_images(x_size, y_size, max_width, max_height) -> List[SubImage]:
    x_ranges = get_ranges(x_size, max_width)
    y_ranges = get_ranges(y_size, max_height)

    subimages = []
    for (x_idx, x_range) in enumerate(x_ranges):
        for (y_idx, y_range) in enumerate(y_ranges):
            subimages.append(SubImage(x_idx, y_idx, x_range, y_range))
    return subimages

def get_ranges(total_size, max_part_size):
    x_begin = [x for x in range(0,total_size,max_part_size)]
    x_end = [x for x in x_begin[1:]] + [total_size]

    return list(zip(x_begin, x_end))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('image_path', help='Path to image')
    parser.add_argument('output_path', help='Output directory')
    parser.add_argument('--tile_width', nargs='?', type=int, default=512, help="Maximum tile width")
    parser.add_argument('--tile_height', nargs='?', type=int, default=512, help="Maximum tile height")
    args = parser.parse_args()

    main(args.image_path, args.output_path, args.tile_width, args.tile_height)
