<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>My Profile</h2>
      
      <form @submit.prevent="updateProfile" enctype="multipart/form-data">
        <div class="form-group">
          <label>Full Name</label>
          <input v-model="form.name" type="text" required />
        </div>

        <div class="form-group">
          <label>Email Address</label>
          <input v-model="form.email" type="email" required />
        </div>

        <div class="form-group">
          <label>Phone Number</label>
          <input v-model="form.phone" type="text" />
        </div>

        <div class="form-group">
          <label>Course</label>
          <input v-model="form.course" type="text" />
        </div>

        <div class="form-group">
          <label>Update Resume (PDF only)</label>
          <input type="file" @change="handleFileUpload" accept=".pdf" />
          <p v-if="profile.resume" class="current-file">
            Current: <a :href="'http://127.0.0.1:5000/download/' + profile.resume" target="_blank">View PDF</a>
          </p>
        </div>

        <div class="button-group">
          <button type="submit" class="save-btn" :disabled="loading">
            {{ loading ? 'Saving...' : 'Update Everything' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      profile: {},
      form: { name: "", email: "", phone: "", course: "" },
      resumeFile: null,
      loading: false
    };
  },
  mounted() {
    this.loadProfile();
  },
  methods: {
    handleFileUpload(event) {
      this.resumeFile = event.target.files[0];
    },
    async loadProfile() {
      const res = await axios.get("http://127.0.0.1:5000/api/student/me", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      this.profile = res.data;
      this.form = { ...res.data }; 
    },
    async updateProfile() {
      this.loading = true;
      try {
        
        let formData = new FormData();
        formData.append("name", this.form.name);
        formData.append("email", this.form.email);
        formData.append("phone", this.form.phone);
        formData.append("course", this.form.course);
        
        if (this.resumeFile) {
          formData.append("resume", this.resumeFile);
        }

        await axios.put("http://127.0.0.1:5000/api/student/profile/update", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        });

        alert("Profile updated successfully!");
        this.loadProfile();
      } catch (err) {
        alert("Error updating profile");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.profile-container { display: flex; justify-content: center; padding: 40px; background: #f4f7f6; min-height: 100vh; }
.profile-card { background: white; padding: 30px; border-radius: 8px; width: 450px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.form-group { margin-bottom: 18px; }
label { display: block; font-weight: 600; margin-bottom: 6px; color: #444; }
input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.save-btn { width: 100%; padding: 12px; background: #1f3c88; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; transition: 0.3s; }
.save-btn:hover { background: #162d66; }
.current-file { font-size: 13px; margin-top: 5px; color: #666; }
</style>