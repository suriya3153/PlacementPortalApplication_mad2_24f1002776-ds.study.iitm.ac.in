<template>
  <div class="register-container">
    <h2>Student Registration</h2>

    <form @submit.prevent="registerStudent" enctype="multipart/form-data">
      <div class="form-group">
        <label>Name</label>
        <input v-model="name" type="text" required />
      </div>

      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>

      <div class="form-group">
        <label>Phone</label>
        <input v-model="phone" type="text" />
      </div>

      <div class="form-group">
        <label>Course</label>
        <input v-model="course" type="text" />
      </div>

      <div class="form-group">
        <label>Upload Resume (PDF only)</label>
        <input type="file" @change="handleFileUpload" accept=".pdf" />
      </div>

      <button type="submit">Register</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      phone: "",
      course: "",
      resumeFile: null,
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    handleFileUpload(event) {
      this.resumeFile = event.target.files[0];
    },
    async registerStudent() {
      try {
        const formData = new FormData();
        formData.append("name", this.name);
        formData.append("email", this.email);
        formData.append("password", this.password);
        formData.append("phone", this.phone);
        formData.append("course", this.course);
        if (this.resumeFile) {
          formData.append("resume", this.resumeFile);
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/api/register/student",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.successMessage = response.data.message;
        this.errorMessage = "";
      } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "Registration failed. Try again.";
        }
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  width: 400px;
  margin: auto;
  margin-top: 80px;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 10px;
  text-align: center;
}
.form-group {
  margin-bottom: 15px;
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}
button {
  width: 100%;
  padding: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background: #218838;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
</style>