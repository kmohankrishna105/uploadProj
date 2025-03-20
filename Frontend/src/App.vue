<template>
  <div>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile" :disabled="!selectedFile">Upload</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      apiUrl: "http://127.0.0.1:5000/upload", // Flask API URL
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      console.log("Selected file:", this.selectedFile);
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file first.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await axios.post(this.apiUrl, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        console.log("Upload response:", response.data);
        alert("File uploaded successfully!");
      } catch (error) {
        console.error("Upload error:", error);
        alert("Error uploading file. Check console for details.");
      }
    },
  },
};
</script>
