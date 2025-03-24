<template>
  <div>
    <h2>📂 Existing Files</h2>

    <div v-if="files.length === 0">No files found.</div> <!-- ✅ Debugging message -->

    <div v-for="file in files" :key="file.id">
      <span>{{ file.filename }}</span>
      <button @click="selectFileForUpdate(file)">📝 Update</button> <!-- ✅ Should display -->
      <a :href="`http://localhost:5000/api/files/download/${file.id}`" download>⬇ Download</a>
    </div>

    <h2>⬆ Upload / Update a File</h2>
    <input type="file" @change="handleFileChange" />
    <p v-if="selectedFile">Selected: {{ selectedFile.name }}</p>
    <p v-if="selectedFileId">Updating: {{ selectedFileId.filename }}</p>

    <button @click="uploadFile">
      {{ selectedFileId ? "🔄 Update File" : "📤 Upload File" }}
    </button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      files: [], // Holds existing records
      selectedFile: null, // Holds the file selected for upload
      selectedFileId: null, // Holds the file object to update
    };
  },
  methods: {
    // ✅ Fetch existing files
    async fetchFiles() {
      try {
        const response = await axios.get("http://localhost:5000/api/files");
        this.files = response.data; // Assuming response is a list of files
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    },

    // ✅ Handle file selection
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },

    // ✅ Upload or Update File
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      // If updating, send file ID
      if (this.selectedFileId) {
        formData.append("id", this.selectedFileId.id);
      }

      try {
        const response = await axios.post(
          "http://localhost:5000/api/files/upload",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        alert(response.data.message);
        this.fetchFiles(); // Refresh list
        this.selectedFile = null;
        this.selectedFileId = null; // Clear selection
      } catch (error) {
        console.error("Upload failed:", error);
      }
    },

    // ✅ Select file for updating
    selectFileForUpdate(file) {
      this.selectedFileId = file; // Store file object for reference
    },
  },
  mounted() {
    this.fetchFiles(); // Fetch files on page load
  },
};
</script>