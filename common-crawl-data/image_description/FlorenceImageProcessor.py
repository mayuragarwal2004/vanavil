import requests
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

class FlorenceImageProcessor:
    def __init__(self, model_id='HuggingFaceM4/Florence-2-DocVQA', device=None):
        # Set device and precision for PyTorch
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        # Initialize the model and processor
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=self.torch_dtype, trust_remote_code=True).to(self.device)
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    def run_florence(self, task_prompt, image, text_input=None):
        """General method to run the Florence model for different tasks."""
        if text_input is None:
            prompt = task_prompt
        else:
            prompt = task_prompt + text_input
            
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torch_dtype)
        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            early_stopping=False,
            do_sample=False,
            num_beams=3,
        )
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed_answer = self.processor.post_process_generation(
            generated_text,
            task=task_prompt,
            image_size=(image.width, image.height)
        )
        return parsed_answer

    def run_vqa(self, image, vqa_text):
        """Method to run a Visual Question Answering (VQA) task using Florence."""
        task_prompt = "<VQA>"
        result = self.run_florence(task_prompt, image, vqa_text)
        return result['<VQA>']  # Returning the VQA answer directly

    def generate_caption(self, image):
        """Generates caption for the image."""
        task_prompt = '<CAPTION>'
        return self.run_florence(task_prompt, image)['<CAPTION>']

    def generate_detailed_caption(self, image):
        """Generates a detailed caption for the image."""
        task_prompt = '<DETAILED_CAPTION>'
        return self.run_florence(task_prompt, image)['<DETAILED_CAPTION>']

    def generate_more_detailed_caption(self, image):
        """Generates a more detailed caption for the image."""
        task_prompt = '<MORE_DETAILED_CAPTION>'
        return self.run_florence(task_prompt, image)['<MORE_DETAILED_CAPTION>']

    def detect_objects(self, image):
        """Detects objects in the image."""
        task_prompt = '<OBJECT_DETECTION>'
        return self.run_florence(task_prompt, image)['<OBJECT_DETECTION>']

    def detect_logo(self, image):
        """Detects whether there is a logo in the image."""
        return self.run_vqa(image, "Is it a company logo?")

    def detect_human(self, image):
        """Detects whether there is a human in the image."""
        return self.run_vqa(image, "Is there a human in the image?")

    def plot_bbox(self, image, data):
        """Plots bounding boxes on the image."""
        fig, ax = plt.subplots()

        # Display the image
        ax.imshow(image)

        # Plot each bounding box
        for bbox, label in zip(data['bboxes'], data['labels']):
            x1, y1, x2, y2 = bbox
            rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.text(x1, y1, label, color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))

        ax.axis('off')
        plt.show()

    def fetch_image(self, url):
        """Fetches and processes an image from the given URL."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

            if image.mode == 'L':  # Grayscale image
                image = image.convert("RGB")
            elif image.mode not in ('RGB', 'RGBA'):
                raise ValueError(f"Unsupported image mode: {image.mode}")
                
            return image
        except Exception as e:
            print(f"Error fetching or processing image from URL {url}: {e}")
            return None


# Example Usage:
if __name__ == "__main__":
    # Initialize processor
    florence_processor = FlorenceImageProcessor()

    # Fetch an image
    image_url = "https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg"
    image = florence_processor.fetch_image(image_url)

    if image:
        # Run Visual Question Answering (VQA)
        vqa_text = "What is in the image?"
        vqa_answer = florence_processor.run_vqa(image, vqa_text)

        # Output the VQA result
        print(f"VQA Answer: {vqa_answer}")
