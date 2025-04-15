const uploadInput = document.getElementById('upload');
const submitBtn = document.getElementById('submit');
const originalImg = document.getElementById('original');
const sketchImg = document.getElementById('sketch');

uploadInput.addEventListener('change', () => {
  const file = uploadInput.files[0];
  if (file) {
    originalImg.src = URL.createObjectURL(file);
    sketchImg.src = ""; // Clear previous sketch
  }
});

submitBtn.addEventListener('click', async () => {
  const file = uploadInput.files[0];
  if (!file) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Sketch generation failed");
    }

    const blob = await response.blob();
    sketchImg.src = URL.createObjectURL(blob);
  } catch (error) {
    alert("Error: " + error.message);
  }
});
