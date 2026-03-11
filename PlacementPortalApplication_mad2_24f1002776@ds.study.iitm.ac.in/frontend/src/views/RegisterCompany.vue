<template>
  <div class="register-container">
    <h2>Company Registration</h2>

    <form @submit.prevent="registerCompany">
      <div class="form-group">
        <label>Company Name</label>
        <input v-model="company_name" type="text" required />
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
        <label>HR Contact</label>
        <input v-model="hr_contact" type="text" />
      </div>

      <div class="form-group">
        <label>Website</label>
        <input v-model="website" type="text" />
      </div>

      <button type="submit">Register</button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>

      <p class="login-link">
        Already have an account? 
        <router-link to="/login">Login here</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterCompany",
  data() {
    return {
      company_name: "",
      email: "",
      password: "",
      hr_contact: "",
      website: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async registerCompany() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/register/company",
          {
            company_name: this.company_name,
            email: this.email,
            password: this.password,
            hr_contact: this.hr_contact,
            website: this.website,
          }
        );

        // Show success message
        this.successMessage = response.data.message;
        this.errorMessage = "";

        // Optional: redirect to login after registration
        setTimeout(() => {
          this.$router.push("/login");
        }, 1500);
      } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "Registration failed. Try again.";
        }
      }
    },
  },
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
  background: #17a2b8;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background: #138496;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
.login-link {
  margin-top: 15px;
}
</style>