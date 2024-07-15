function uploadAudio() {
  const audioFile = document.getElementById("audioFile").files[0];
  if (!audioFile) {
    alert("Please select an audio file");
    return;
  }

  const formData = new FormData();
  formData.append("audio", audioFile);

  fetch("/upload_audio", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.transcription) {
        document.getElementById("transcription").innerText = data.transcription;
      } else {
        alert("Error: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred");
    });
}
