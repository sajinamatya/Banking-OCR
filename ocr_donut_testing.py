from donut import DonutModel
from PIL import Image
import torch

#loading the trained model on the custom dataset 
model = DonutModel.from_pretrained("E:\Sajilo E-bank\pretrained")
# inspecting if the gpu is avaible or not 
if torch.cuda.is_available():
    model.half()
    device = torch.device("cuda")
    model.to(device)
else:
    model.encoder.to(torch.bfloat16)
# model evaluation 
model.eval()
# image path 
image = Image.open("path/to/image.jpg").convert("RGB") 
with torch.no_grad():
  output = model.inference(image=image, prompt="<s_data>")
