<template>
  <div class="mb-6">
    <!-- Snackbar Notification -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000" top>
      {{ messageAnswer }}
      <v-btn dark outlined @click="snackbar = false">Close</v-btn>
    </v-snackbar>

    <v-row align="left" justify="center">
      <v-col cols="10">
        <v-card>
          <v-card-title>
            <v-icon color="ubs_carbon">view_list</v-icon>
            <span class="title font-weight-bold">Breach Document</span>
            <v-spacer />
            <v-text-field v-model="search" append-icon="search" label="Search" />
            <v-btn color="primary" @click="fetchGenuineRecords">Show Genuine Records</v-btn>
          </v-card-title>

          <!-- File Upload / Update Dialog -->
          <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <span class="headline">Update or Insert Evidence</span>
                <v-spacer />
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.kpi_relevant" label="KPI Relevant" />
                    </v-col>
                    <v-col>
                      <v-text-field v-model="editedItem.genuine" label="Genuine" />
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.filename" label="Filename" />
                      <div class="upload-container">
                        <input type="file" @change="handleFileUpload" />
                        <button @click="uploadFile" :disabled="!selectedFile">Upload File</button>
                        <button
                          v-if="editedItem.id && editedItem.filename"
                          @click="downloadFile(editedItem.id)">
                          Download File
                        </button>
                      </div>
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.remarks" label="Remarks" />
                    </v-col>
                  </v-row>

                </v-container>
              <v-row>
              <v-col>
              <p>Checkbox Value: {{ editedItem.is_genuine }}</p>

                <v-checkbox
                  v-model="editedItem.is_genuine"
                  label="Is Genuine?"
                  :true-value="true"
                  :false-value="false"
                ></v-checkbox>
              </v-col>
                </v-row>

               </v-card-text>

              <v-card-actions>
                <v-spacer />
                <v-btn color="primary" text @click="close">Cancel</v-btn>
                <v-btn depressed color="primary" @click="saveItem">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-dialog v-model="showGenuineDialog" persistent max-width="600px">
  <v-card>
    <v-card-title>
      <span class="headline">Genuine Records</span>
      <v-spacer />
    </v-card-title>

    <v-card-text>
      <v-container>
        <v-data-table
          :headers="genuineHeaders"
          :items="records"
          class="elevation-0"
        >
          <template v-slot:item="{ item }">
            <tr>
              <td>{{ item.date_time }}</td>
              <td>{{ item.alert_type }}</td>
              <td>{{ item.value }}</td>
              <td class="text-left">{{ item.currency }}</td>
                <td class="text-left">{{ item.breach_trigger }}</td>
                <td class="text-left">{{ item.region }}</td>
                <td class="text-left">{{ item.kpi_relevant }}</td>
                <td class="text-left">{{ item.genuine }}</td>
              <td>{{ item.remarks }}</td>

            </tr>
          </template>
        </v-data-table>
      </v-container>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn color="primary" text @click="showGenuineDialog = false">Close</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>


          <!-- Data Table -->
          <v-data-table
            :headers="headers"
            :items="items"
            :search="search"
            :loading="loading"
            :options.sync="options"
            class="elevation-0 px-3 column-reverse"
          >
           <template v-slot:headers>
    <tr>
      <th v-for="header in headers" :key="header.value">
        {{ header.text }}
      </th>
    </tr>
  </template>


                <template v-slot:item="{ item }">
              <tr>
                <td class="text-left">{{ item.date_time }}</td>
                <td class="text-left">{{ item.alert_type }}</td>
                <td class="text-left">{{ item.value }}</td>
                <td class="text-left">{{ item.currency }}</td>
                <td class="text-left">{{ item.breach_trigger }}</td>
                <td class="text-left">{{ item.region }}</td>
                <td class="text-left">{{ item.kpi_relevant }}</td>
                <td class="text-left">{{ item.genuine }}</td>
                <td class="text-left">{{ item.remarks }}</td>
                <td class="text-left">{{ item.sub_date_time }}</td>
                <td class="text-left">{{ item.filename }}</td>
                <v-checkbox v-model="item.is_genuine" disabled></v-checkbox>

                <v-btn color="primary" @click="editItem(item)">Edit</v-btn>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      editedItem: {},
      is_genuine: false, // Default value (false)
      options: {}, // Add this line
      api: "http://localhost:5000/api/files/",
      saveapi:"http://localhost:5000/api/files/model",
      dialog: false,
      selectedFile: null,
      selectedFileId: null,
      search: "",
      loading: false,
      snackbar: false,
      snackbarColor: "success",
      messageAnswer: "",
      headers: [
        { text: "Date", value: "date_time", width: "10%" },
        { text: "Alert Type", value: "alert_type", width: "5%" },
        { text: "Value", value: "value", width: "5%" },
        { text: "Currency", value: "currency", width: "5%" },
        { text: "Breach Trigger", value: "breach_trigger", width: "10%" },
        { text: "Region", value: "region", width: "5%" },
        { text: "KPI Relevant", value: "kpi_relevant", width: "5%" },
        { text: "Genuine", value: "genuine", width: "5%" },
        { text: "Remarks", value: "remarks", width: "10%" },
        { text: "Timestamp", value: "sub_date_time", width: "10%" },
        { text: "Filename", value: "filename", width: "5%" },
        { text: "GenuineAlert", value: "is_genuine", width: "5%" },



      ],
      items: [],
      editedItem: {},
      showGenuineDialog: false,
      records: [],
      api: "http://localhost:5000/api/files",
    };
  },
  created() {
    this.getItems();
  },
  methods: {
    async getItems() {
      this.loading = true;
      try {
        const res = await axios.get(this.api);
        console.log("API Response:", res.data); // 🔥 Debugging

        this.items = res.data.map(item => ({
      ...item,
      is_genuine: item.is_genuine === true || item.is_genuine === "true"|| item.is_genuine === "t" ? "Yes" : "No" ,// 🔥 Ensure Boolean
    }));
      } catch (error) {
        console.error("Error fetching items:", error);
      } finally {
        this.loading = false;
      }
    },
    async editItem(item) {
      try {
      const res = await axios.get(`${this.api}/${item.id}`);
      console.error("respoooooonse fata", res.data);
      this.editedItem = res.data;
      this.dialog = true;
      this.editedItem.is_genuine = res.data.is_genuine === true || res.data.is_genuine === "true";

    } catch (error) {
      console.error("Error fetching item details:", error);
    }
  },
    async saveItem() {
      try {
        await axios.post(this.saveapi, this.editedItem);
        this.getItems();
        this.close();
      } catch (error) {
        console.error("Error saving item:", error);
      }
    },
    close() {
      this.dialog = false;
      this.editedItem = {};
    },
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
      console.log("file11111111111111", this.selectedFile)
      formData.append("id", this.editedItem.id); // Add this
      console.log("file333333333333333", this.editedItem.id)

      try {
        const response = await axios.post(`${this.api}/upload`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        console.log("Server response:", response.data);
        this.editedItem.filename = response.data.filename;
        await this.saveItem();  // Save the updated item

        alert("File uploaded successfully!");
        this.getItems();
        console.log("File uploaded successfully :", this.getItems()); // Debugging

        //this.close();
      } catch (error) {
        console.error("Error uploading file:", error);
        alert("File upload failed.");
      }
    },
    selectFileForUpdate(file) {
      this.selectedFileId = file;
      console.log("Selected file for update:", this.selectedFileId);
    },
    async fetchGenuineRecords() {
      try {
        const response = await axios.get(`${this.api}/records`);
        this.records = response.data;
        this.showGenuineDialog = true;
      } catch (error) {
        console.error('Error fetching genuine records:', error);
      }
    },
  },
  async downloadFile(fileId) {
    try {
      const response = await axios({
        url: `${this.api}/download/${fileId}`, // Adjust API URL if needed
        method: "GET",
        responseType: "blob", // Important for handling file downloads
      });

      // Create a Blob URL to trigger the download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
       const filename = this.editedItem?.filename || "downloaded_file";

        link.setAttribute("download", filename); // Set correct filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
      console.error("Error downloading file:", error);
      alert("File download failed.");
    }
  }

};
</script>

<style scoped>
.column-reverse {
  display: flex;
  flex-direction: column-reverse;
}
.upload-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.show-checkbox {
  display: block !important;
  visibility: visible !important;
}

</style>
computed: {
  processedItems() {
    return this.items.map(item => ({
      ...item,
      is_genuine: item.is_genuine ? "Yes" : "No"
    }));
  }
}