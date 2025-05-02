from donut import DonutModel
from PIL import Image
import torch

# Change the path here:
model = DonutModel.from_pretrained("E:\Sajilo E-bank\pretrained")
if torch.cuda.is_available():
    model.half()
    device = torch.device("cuda")
    model.to(device)
else:
    model.encoder.to(torch.bfloat16)

model.eval()

image = Image.open("path/to/image.jpg").convert("RGB") # Change here
with torch.no_grad():
  output = model.inference(image=image, prompt="<s_data>")