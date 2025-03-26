<template>
<v-app>
  <div class="mb-6">
    <!-- Snackbar Notification -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000" top>
      {{ messageAnswer }}
      <v-btn color="white" outlined @click="snackbar = false">Close</v-btn>
    </v-snackbar>

    <v-row justify="center">
      <v-col cols="10">
        <v-card>
          <v-card-title>
            <v-icon color="primary">mdi-view-list</v-icon>
            <span class="title font-weight-bold">Breach Document</span>
            <v-spacer />
           <v-text-field v-model="search" append-inner-icon="mdi-magnify" label="Search"  class="small-search" />
          <v-btn color="primary" @click="fetchGenuineRecords" small density="compact">Show Genuine Records</v-btn>


          </v-card-title>
           <v-dialog v-model="genuineDialog" max-width="900px">
  <v-card>
    <v-card-title>
      <span class="headline">Genuine Records</span>
      <v-spacer />
      <v-btn icon @click="genuineDialog = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-data-table
        :headers="headers"
        :items="genuineRecords"
        class="elevation-1"
        dense
      >
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.date_time }}</td>
            <td>{{ item.alert_type }}</td>
            <td>{{ item.value }}</td>
            <td>{{ item.currency }}</td>
            <td>{{ item.breach_trigger }}</td>
            <td>{{ item.region }}</td>
            <td>{{ item.kpi_relevant }}</td>
            <td>{{ item.genuine }}</td>
            <td>{{ item.remarks }}</td>
            <td>{{ item.sub_date_time }}</td>
            <td>{{ item.filename }}</td>
            <td>
              <v-checkbox v-model="item.is_genuine" disabled></v-checkbox>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn color="error" text @click="genuineDialog = false">Close</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
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
                        <v-btn color="primary" @click="uploadFile" :disabled="!selectedFile">Upload File</v-btn>
                        <v-btn
                          v-if="editedItem.id && editedItem.filename"
                          color="secondary"
                          @click="downloadFile(editedItem.id)"
                        >
                          Download File
                        </v-btn>
                      </div>
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.remarks" label="Remarks" />
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col>
                      <p>Checkbox Value: {{ editedItem.is_genuine }}</p>
                      <v-checkbox
                        v-model="editedItem.is_genuine"
                        label="Is Genuine?"
                        :true-value="true"
                        :false-value="false"
                      />
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer />
                <v-btn color="error" text @click="close">Cancel</v-btn>
                <v-btn color="primary" @click="saveItem">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <!-- Data Table -->
          <v-data-table
            :headers="headers"
            :items="processedItems"
            :search="search"
            :loading="loading"
            class="elevation-1 px-3"
          >
            <template v-slot:item="{ item }">
              <tr>
                <td>{{ item.date_time }}</td>
                <td>{{ item.alert_type }}</td>
                <td>{{ item.value }}</td>
                <td>{{ item.currency }}</td>
                <td>{{ item.breach_trigger }}</td>
                <td>{{ item.region }}</td>
                <td>{{ item.kpi_relevant }}</td>
                <td>{{ item.genuine }}</td>
                <td>{{ item.remarks }}</td>
                <td>{{ item.sub_date_time }}</td>
                <td>{{ item.filename }}</td>
                <td>
                  <v-checkbox v-model="item.is_genuine" disabled></v-checkbox>
                </td>
                <td>
                  <v-btn color="primary" @click="editItem(item)">Edit</v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>

  </v-app>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      genuineDialog: false,
      genuineRecords: [],
      dialog: false,
      editedItem: {},
      selectedFile: null,
      search: "",
      loading: false,
      snackbar: false,
      snackbarColor: "success",
      messageAnswer: "",
      headers: [
        { text: "Date", value: "date_time" },
        { text: "Alert Type", value: "alert_type" },
        { text: "Value", value: "value" },
        { text: "Currency", value: "currency" },
        { text: "Breach Trigger", value: "breach_trigger" },
        { text: "Region", value: "region" },
        { text: "KPI Relevant", value: "kpi_relevant" },
        { text: "Genuine", value: "genuine" },
        { text: "Remarks", value: "remarks" },
        { text: "Timestamp", value: "sub_date_time" },
        { text: "Filename", value: "filename" },
        { text: "GenuineAlert", value: "is_genuine" },
      ],
      items: [],
      api: "http://localhost:5000/api/files",
    };
  },
  computed: {
    processedItems() {
      return this.items.map((item) => ({
        ...item,
        is_genuine: item.is_genuine ? "Yes" : "No",
      }));
    },
  },
  created() {
    this.getItems();
  },
  methods: {
    async getItems() {
      this.loading = true;
      try {
        const res = await axios.get(this.api);
        this.items = res.data;
      } catch (error) {
        console.error("Error fetching items:", error);
      } finally {
        this.loading = false;
      }
    },
    editItem(item) {
      try {
    console.log("Editing item ID:", item.id);
     this.editedItem = { ...item };
    this.dialog = true;  // Open the dialog
    //const res = await axios.get(`${this.api}/${item.id}`);
    //console.log("Fetched Data:", res.data);
    //console.log("Fetched Data:", item.id);

    //this.editedItem = { ...this.editedItem, ...res.data };
    //this.editedItem = {...this.editedItem};
  } catch (error) {
    console.error("Error fetching item details:", error);
  }
    },
    async saveItem() {
      try {
        await axios.put(`${this.api}/Update`,{
        is_genuine: this.editedItem.is_genuine,
        file_id : this.editedItem.id,
        remarks : this.editedItem.remarks
        }, {
        headers: { "Content-Type": "application/json" }
      });
       console.log("Item updated successfully");
        await this.getItems();
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
    },
    async uploadFile() {
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      console.log("File ID response:", this.editedItem.id);
      formData.append("file_id", this.editedItem.id);

      try {
        const response = await axios.post(`${this.api}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
});
        console.log("Server response:", response.data);
        this.editedItem.filename = response.data.filename;
        await this.saveItem();  // Save the updated item

        alert("File uploaded successfully!");
        this.getItems();
        console.log("File uploaded successfully :");
        this.close();
        this.getItems(); // Debugging



      } catch (error) {
        console.error("Error uploading file:", error);
      }
    },
    async fetchGenuineRecords() {
    try {
      const response = await axios.get(`${this.api}/records`);
      this.genuineRecords = response.data;
      console.log("Genuine records received:", this.genuineRecords);
      this.genuineDialog = true;
    } catch (error) {
      console.error("Error fetching genuine records:", error);
    }
  }
  },
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  gap: 10px;

}
</style>
