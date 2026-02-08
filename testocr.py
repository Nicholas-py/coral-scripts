#from transformers import pipeline
import matplotlib.pyplot as plt
from matplotlib import cm
from mss import mss
import numpy as np
from PIL import Image
#from transformers import AutoProcessor, AutoModelForImageTextToText
from time import time
a = time()
pdfbounds = {'top':142,'left':0,'width':1000,'height':988}
shot = mss()
arr = np.asarray(shot.grab(pdfbounds))
im = Image.fromarray(arr).convert('RGB')
arr = np.array(im)

print('sct',time()-a)
b = time()
from mmocr.apis import MMOCRInferencer

ocr = MMOCRInferencer(det='DBNet', rec='SAR')

print(' '.join(ocr(arr, show=False)['predictions'][0]['rec_texts']))

print('OCR',time()-b)
askdaojfaposj



def a():
    pdfbounds = {'top':142,'left':0,'width':1000,'height':988}
    def screenshot(bounds, show = False, french = False):
        shot = mss()
        arr = np.asarray(shot.grab(bounds))
        im = Image.fromarray(arr)
        if show:
            im.show()
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": im,
                    },
                    {"type": "text", "text": "Recognize text in this image."},
                ],
            }
        ]
        text_prompt = processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = processor(images=im, text=[text_prompt],truncation=False, return_tensors="pt").to(model.device)

        print(inputs)

        outputs = model.generate(**inputs, max_new_tokens=512)
        text = processor.decode(outputs[0],skip_special_tokens=True)
        if show:
            print(text.strip())
        return text
    print(screenshot(pdfbounds, True))
a()
