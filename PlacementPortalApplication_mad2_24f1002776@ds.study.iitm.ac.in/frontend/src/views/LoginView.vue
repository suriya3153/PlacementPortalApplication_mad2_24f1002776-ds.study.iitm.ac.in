<template>
  <div class="login-container">
    <h2>Placement Portal Login</h2>

    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>

      <button type="submit">Login</button>

<p v-if="errorMessage" class="error">{{ errorMessage }}</p>


<p>
  <a @click="$router.push('/register-student')">Register as Student</a> | 
  <a @click="$router.push('/register-company')">Register as Company</a>
</p>
    </form>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      errorMessage: ""
    }
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          email: this.email,
          password: this.password
        });

        if (!response.data || !response.data.data || !response.data.data.access_token) {
          this.errorMessage = "Login failed. No token returned.";
          return;
        }

        const userData = response.data.data;
        const token = userData.access_token;
        const role = userData.role;

       
        localStorage.setItem("token", token);
        localStorage.setItem("role", role);
        localStorage.setItem("user_id", userData.user_id);
        localStorage.setItem("email", userData.email);


        if (role === "admin") {
          this.$router.push("/admin");
        } else if (role === "student") {
          this.$router.push("/student");
        } else if (role === "company") {
          this.$router.push("/company-dashboard");
        } else {
          this.errorMessage = "Unknown role. Cannot login.";
        }

      } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "Login failed. Please try again.";
        }
      }
    }
  }
}
</script>

<style scoped>
.login-container{
  width:350px;
  margin:auto;
  margin-top:120px;
  padding:30px;
  border:1px solid #ddd;
  border-radius:10px;
  text-align:center;
}
.form-group{
  margin-bottom:15px;
}
input{
  width:100%;
  padding:8px;
  margin-top:5px;
}
button{
  width:100%;
  padding:10px;
  background:#2c7be5;
  color:white;
  border:none;
  border-radius:5px;
  cursor:pointer;
}
button:hover{
  background:#1a5fd0;
}
.error{
  color:red;
  margin-top:10px;
}
</style>