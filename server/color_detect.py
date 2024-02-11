# color_detect.py
import cv2
import numpy as np
from PIL import Image, ImageFilter
import pandas as pd
import extcolors
from matplotlib import pyplot as plt

class AIProcessor_Color:
    def __init__(self):
        pass

    @staticmethod
    def get_color(input_name, mask_file, output_width=900):
        img = cv2.imread(input_name)
        mask = cv2.imread(mask_file, 0)
        result = img.copy()
        result[mask == 0] = 255

        mask_img = Image.fromarray(result)
        mask_img = mask_img.point(lambda p: p * 1.2)
        mask_img = mask_img.convert("RGB")

        data = np.array(mask_img)
        mask = (data[:, :, 0] == 255) & (data[:, :, 1] == 255) & (data[:, :, 2] == 255)
        data[:, :, :3][mask] = [0, 0, 0]
        mask_img = Image.fromarray(data)

        wpercent = output_width / float(mask_img.size[0])
        hsize = int((float(mask_img.size[1]) * float(wpercent)))
        img_resized = mask_img.resize((output_width, hsize), resample=Image.LANCZOS)

        colors_x = extcolors.extract_from_image(img_resized, tolerance=12, limit=12)
        df_color = AIProcessor_Color.color_to_df(colors_x)
        # print(df_color)

        # Return the 0th index color
        return df_color["c_code"].iloc[0]

    @staticmethod
    def color_to_df(input):
        colors_pre_list = str(input).replace("([(", "").split(", (")[0:-1]
        df_rgb = [i.split("), ")[0] + ")" for i in colors_pre_list]
        df_percent = [i.split("), ")[1].replace(")", "") for i in colors_pre_list]

        df_color_up = [
            "#{:02x}{:02x}{:02x}".format(
                int(i.split(", ")[0].replace("(", "")),
                int(i.split(", ")[1]),
                int(i.split(", ")[2].replace(")", "")),
            )
            for i in df_rgb
        ]

        df = pd.DataFrame(zip(df_color_up, df_percent), columns=["c_code", "occurrence"])
        
        # Filter out black
        df = df[df["c_code"] != "#000000"]
        return df
