from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="AIzaSyCdPH68VPN1ytRKBst4uaOGtc-IHVgQ8zc")

# Set up the model
generation_config = {   
    "temperature": 0.45,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                            generation_config=generation_config,
                            safety_settings=safety_settings)

def ask_for_image():
    while True:
        image_path = input("Lütfen bir resim dosyasının yolunu girin: ")
        image_path = Path(image_path)
        if image_path.exists():
            return image_path
        else:
            print("Belirtilen yol bulunamadı. Lütfen doğru bir yol girin.")

# Kullanıcıdan resim girişini iste
image_path = ask_for_image()

# Resmi oku ve içeriği oluşturacak parçaları hazırla
image_parts = [
    {
        "mime_type": f"image/{image_path.suffix[1:]}",  # Uzantıdan MIME türünü otomatik belirle
        "data": image_path.read_bytes()
    },
]


prompt_parts = [
    image_parts[0],
]

prompt_parts = [    
    image_parts[0],
    "bu görsel/görseller de Kanser var mı? Eğer varsa evresi nedir? Kanserin yeri ve büyüklüğü nedir? Detaylıca, bir doktora anlatır gibi anlatın ve sadece görsel hakkında bilgiler verin",
]

# Modelden yanıtı al
response = model.generate_content(prompt_parts)

# Kullanıcıya modelin çıktısını göster
print(response.text)

