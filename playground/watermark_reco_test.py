import WatermarkReco.model.model as model
import torch
from torchvision import *
from PIL import *
from matplotlib import pyplot as plt

PATH = './WatermarkReco/model/SyntheticFinetuned83.pth'
PATH2 = './WatermarkReco/model/EngravingFinetuned75.pth'
IMAGE_PATH = './testImage2.png'

model = model.ResNetLayer3Feat( None )
model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))
model.eval()

imsize = 352
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

def image_loader(image_name):
    """load image, returns cuda tensor"""
    image = Image.open(image_name)
    image = image.convert('RGB')
    image = loader(image).float()
    image = torch.autograd.Variable(image, requires_grad=True)
    image = image.unsqueeze(0)
    return image.to('cpu')

image = image_loader(IMAGE_PATH)

with torch.no_grad() : 
    result = model(image).data

print(result.shape)

"""

result=torch.squeeze(result)
transform = transforms.ToPILImage()
img = transform(result)
img.show()
#image = result.detach().numpy()
#plt.imshow(image)

print(result.shape) 
transform = transforms.ToPILImage()
img = transform(result)
img.show()
print(result)
print(type(result))
print(result.shape)
"""
