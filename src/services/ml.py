import torch
from transformers import ViTForImageClassification, ViTFeatureExtractor
from PIL import Image
import torch.nn.functional as F
import io

def simulate_compression_loss(img, format='JPEG', quality=85):
    buffer = io.BytesIO()
    img.save(buffer, format=format, quality=quality)
    buffer.seek(0)
    compressed_img = Image.open(buffer)
    return compressed_img

def process_image(image_path, new_size=(224, 224), simulate_loss=True):
    img = Image.open(image_path)
    resized_img = img.resize(new_size, Image.Resampling.LANCZOS) 

    if simulate_loss:
        buffer = io.BytesIO()
        resized_img.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        resized_img = Image.open(buffer)

    return resized_img

num_labels = 29
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k", num_labels=num_labels)
model_path = 'src/ml/Vit_model_best_epoch_2.pth'
#model.load_state_dict(torch.load(model_path), strict=False)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
model.eval()

feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")
image_path = "img/test_img.jpg"
resized_img = process_image(image_path)

inputs = feature_extractor(images=resized_img, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = F.softmax(logits, dim=1)

class_idx_to_label = {
    0: '출/퇴근',
    1: '일/공부',
    2: '집',
    3: '카페',
    4: '드라이브',
    5: '거리',
    6: '클럽',
    7: '파티',
    8: '휴식',
    9: '해변',
    10: '집중',
    11: '여유',
    12: '아침',
    13: '밥',
    14: '산책',
    15: '운동',
    16: '행복',
    17: '화남',
    18: '몽환적인',
    19: '밝은',
    20: '슬픔',
    21: '우울/외로움',
    22: '편안한',
    23: '사랑',
    24: '봄',
    25: '여름',
    26: '가을',
    27: '겨울',
    28: '우중충한날'
}

threshold = 0.1
high_prob_predictions = (probabilities > threshold).nonzero(as_tuple=True)[1]
for idx in high_prob_predictions:
    predicted_label = class_idx_to_label.get(idx.item(), "Unknown")
    print(f"Predicted label: {predicted_label} with probability {probabilities[0, idx].item()}")
