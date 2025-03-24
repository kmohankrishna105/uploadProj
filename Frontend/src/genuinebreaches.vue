<template>
  <div>
    <v-container>
      <v-card>
        <v-card-title>
          <v-icon color="success">list</v-icon>
          <span class="title font-weight-bold">Genuine Records</span>
          <v-spacer />
          <v-btn color="primary" @click="$router.push('/')">Back</v-btn>
        </v-card-title>

        <v-data-table
          :headers="headers"
          :items="records"
          :loading="loading"
          class="elevation-0 px-3"
        >
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
              <td class="text-left">{{ item.is_genuine }}</td>
            </tr>
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      loading: false,
      records: [],
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
        { text: "Genuine Alert", value: "is_genuine" },
      ],
    };
  },
  async created() {
    await this.fetchGenuineRecords();
  },
  methods: {
    async fetchGenuineRecords() {
      this.loading = true;
      try {
        const response = await axios.get("http://localhost:5000/api/files/records");
        this.records = response.data;
      } catch (error) {
        console.error("Error fetching genuine records:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
