import torch
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch.nn.functional as F
import io

class ImageProcessor:
    def __init__(self, model_path, num_labels=29):
        # 모델을 초기화하고 학습된 가중치를 로드합니다.
        self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k", num_labels=num_labels)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
        self.model.eval()

        # 이미지 프로세서를 초기화합니다.
        self.image_processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")

    def process_image(self, image_path, new_size=(224, 224), simulate_loss=True):
        # 이미지를 열고 크기를 조정합니다.
        img = Image.open(image_path)
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

        # 선택적으로 이미지의 압축 손실을 시뮬레이션합니다.
        if simulate_loss:
            buffer = io.BytesIO()
            resized_img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            resized_img = Image.open(buffer)

        return resized_img

    def extract_tags(self, image_path, threshold=0.06):
        # 이미지를 처리하고 모델에 입력하기 위해 전처리합니다.
        resized_img = self.process_image(image_path)
        inputs = self.image_processor(images=resized_img, return_tensors="pt")

        # 모델을 사용하여 태그 확률을 예측합니다.
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = F.softmax(logits, dim=1)
            predictions = (probabilities >= threshold).int()
            # 확률이 임계값 이상인 태그에 대해 1을, 그렇지 않은 태그에 대해 0을 할당합니다.
            one_hot_encoded_predictions = (probabilities >= threshold).int().squeeze().tolist()

        # 원-핫 인코딩된 예측 결과를 반환합니다.
        return predictions.squeeze().cpu().numpy()

#사용 코드입니다.
#image_processor = ImageProcessor(model_path='src/ml/Vit_model_best_epoch_2.pth')
#tags = image_processor.extract_tags(image_path='images/dw2.jpg')
#print(tags)


