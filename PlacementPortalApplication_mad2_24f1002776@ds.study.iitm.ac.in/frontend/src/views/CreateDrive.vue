<template>
  <div class="create-drive-container">
    <h2>Create Placement Drive</h2>

    <div class="form-group">
      <label>Job Title:</label>
      <input v-model="job_title" type="text" placeholder="Enter job title" />
    </div>

    <div class="form-group">
      <label>Job Description:</label>
      <textarea v-model="job_description" placeholder="Enter job description"></textarea>
    </div>

    <div class="form-group">
      <label>Eligibility:</label>
      <input v-model="eligibility" type="text" placeholder="Eligibility criteria" />
    </div>

    <div class="form-group">
      <label>Application Deadline:</label>
      <input v-model="deadline" type="date" />
    </div>

    <button @click="submitDrive">Submit</button>

    <p v-if="message" style="color:green">{{ message }}</p>
    <p v-if="errorMessage" style="color:red">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CreateDrive",
  data() {
    return {
      job_title: "",
      job_description: "",
      eligibility: "",
      deadline: "",
      message: "",
      errorMessage: ""
    }
  },
  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token")
      if (!token || token === "undefined") {
        this.$router.push("/login")
        return { headers: {} }
      }
      return { headers: { Authorization: `Bearer ${token}` } }
    },

    async submitDrive() {
      if (!this.job_title || !this.job_description || !this.eligibility || !this.deadline) {
        this.errorMessage = "All fields are required"
        return
      }

      try {
        const res = await axios.post(
          "http://127.0.0.1:5000/api/company/drives",
          {
            job_title: this.job_title,
            job_description: this.job_description,
            eligibility: this.eligibility,
            deadline: this.deadline
          },
          this.getAuthHeader()
        )

        this.message = res.data.message
        this.errorMessage = ""
        // Clear the form
        this.job_title = ""
        this.job_description = ""
        this.eligibility = ""
        this.deadline = ""

        // ✅ Optional: Redirect to My Drives after creation
        setTimeout(() => {
          this.$router.push("/company-dashboard")
        }, 1000)

      } catch (error) {
        this.errorMessage = error.response?.data?.error || "Failed to create drive"
      }
    }
  }
}
</script>

<style scoped>
.create-drive-container {
  max-width: 600px;
  margin: 40px auto;
  background:white;
  padding:30px;
  border-radius:8px;
  box-shadow:0 3px 10px rgba(0,0,0,0.08);
}

h2 {
  color:#1f3c88;
  text-align:center;
  margin-bottom:20px;
}

.form-group {
  margin-bottom:15px;
}

label {
  display:block;
  font-weight:600;
  margin-bottom:5px;
}

input, textarea {
  width:100%;
  padding:8px 12px;
  border-radius:6px;
  border:1px solid #ccc;
}

button {
  padding:10px 20px;
  background:#1f3c88;
  color:white;
  border:none;
  border-radius:6px;
  cursor:pointer;
  font-weight:600;
}

button:hover {
  background:#163170;
}
</style>