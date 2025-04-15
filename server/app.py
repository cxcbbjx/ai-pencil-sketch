import os
import cv2
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Sketch function
def generate_sketch(input_path, output_path):
    print(f"[INFO] Reading image from {input_path}")
    image = cv2.imread(input_path)

    if image is None:
        print("[ERROR] Failed to read image.")
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)

    print(f"[INFO] Writing sketch to {output_path}")
    cv2.imwrite(output_path, sketch)
    return True

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        input_path = os.path.join(UPLOAD_DIR, file.filename)
        sketch_path = os.path.join(UPLOAD_DIR, f"sketch_{file.filename}")

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        success = generate_sketch(input_path, sketch_path)

        if not success:
            return JSONResponse(status_code=500, content={"error": "Sketch generation failed."})

        return FileResponse(sketch_path, media_type="image/png")

    except Exception as e:
        print(f"[ERROR] {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
