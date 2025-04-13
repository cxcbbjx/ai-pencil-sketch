async function uploadAndTransform() {
    const input = document.getElementById('imageInput');
    if (!input.files.length) {
      alert('Please select an image!');
      return;
    }
  
    const formData = new FormData();
    formData.append('image', input.files[0]);
  
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    });
  
    const data = await response.json();
    if (data.output_url) {
      const fullURL = `http://localhost:5000${data.output_url}`;
      document.getElementById('result').innerHTML = `
        <img src="${fullURL}" alt="Sketch Image"/>
        <br>
        <a href="${fullURL}" download="sketch.jpg" class="download-btn">Download Sketch</a>
      `;
    } else {
      alert('Something went wrong.');
    }
  }
  