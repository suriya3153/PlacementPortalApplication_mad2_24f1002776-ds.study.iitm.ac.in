<template>
  <div class="student-container">

    <!-- NAVBAR -->
    <nav class="navbar">
      <h2 class="brand-logo">Student Portal</h2>
      <div class="nav-links">
        <button :class="{ active: section==='dashboard' }" @click="section='dashboard'">Dashboard</button>
        <button :class="{ active: section==='browse' }" @click="section='browse'">Browse Jobs</button>
        <button :class="{ active: section==='my-apps' }" @click="section='my-apps'">My Applications</button>
        <button @click="$router.push('/student/profile')">Profile</button>
        <button class="logout-btn" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- MAIN CONTENT -->
    <main class="main-content">

      <!-- DASHBOARD -->
      <div v-if="section==='dashboard'" class="dashboard-grid">
        <div class="card">
          <h3>Welcome, {{ profile.name }}</h3>
          <p>{{ profile.course }}</p>
        </div>
        <div class="card">
          <h3>Applications Sent</h3>
          <p>{{ myApplications.length }}</p>
        </div>
      </div>

      <!-- TABLES -->
      <div v-else class="table-section">
        <h3>{{ section==='browse' ? 'Available Placement Drives' : 'Your Application Status' }}</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Company</th>
                <th>Role</th>
                <th v-if="section==='browse'">Deadline</th>
                <th v-if="section==='my-apps'">Applied Date</th>
                <th>Status / Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in section==='browse' ? availableDrives : myApplications" :key="item.id">
                <td>{{ item.company_name }}</td>
                <td>{{ item.job_title }}</td>
                <td v-if="section==='browse'">{{ item.deadline }}</td>
                <td v-if="section==='my-apps'">{{ item.applied_on }}</td>
                <td>
                  <button v-if="section==='browse'" class="apply-btn" @click="apply(item.id)">Apply Now</button>
                  <span v-if="section==='my-apps'" :class="'badge ' + item.status.toLowerCase()">{{ item.status }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      section: 'dashboard',
      profile: {},
      availableDrives: [],
      myApplications: []
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    getAuthHeader() {
      return { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } };
    },
    async fetchData() {
      try {
        const [prof, drives, apps] = await Promise.all([
          axios.get("http://127.0.0.1:5000/api/student/me", this.getAuthHeader()),
          axios.get("http://127.0.0.1:5000/api/student/available-drives", this.getAuthHeader()),
          axios.get("http://127.0.0.1:5000/api/student/my-applications", this.getAuthHeader())
        ]);
        this.profile = prof.data;
        this.availableDrives = drives.data;
        this.myApplications = apps.data;
      } catch (err) {
        console.error("Session expired or error loading data", err);
        this.$router.push("/login");
      }
    },
    async apply(driveId) {
      try {
        await axios.post(`http://127.0.0.1:5000/api/student/apply/${driveId}`, {}, this.getAuthHeader());
        alert("Applied successfully!");
        this.fetchData();
      } catch (err) {
        alert(err.response?.data?.error || "Failed to apply");
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    }
  }
}
</script>

<style scoped>
/* FULL PAGE LAYOUT */
.student-container { width: 100%; min-height: 100vh; background: #f5f7fa; display: flex; flex-direction: column; font-family: 'Inter', sans-serif; }
.navbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: #2c3e50; color: #fff; }
.brand-logo span { color: #4f46e5; font-weight: bold; }
.nav-links button { margin-left: 10px; padding: 8px 14px; border-radius: 6px; border: none; cursor: pointer; color: #fff; background: #34495e; transition: 0.2s; }
.nav-links button:hover { background: #4f46e5; }
.nav-links button.active { background: #4f46e5; }
.logout-btn { background: #e74c3c !important; }

.main-content { padding: 20px 40px; flex: 1; display: flex; flex-direction: column; gap: 20px; }

/* DASHBOARD CARDS */
.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.card { background: #fff; padding: 20px; border-radius: 12px; border-left: 5px solid #2c3e50; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; transition: 0.2s; }
.card:hover { transform: translateY(-2px); }

/* TABLE SECTION */
.table-section h3 { margin-bottom: 15px; font-weight: 600; }
.table-wrapper { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; min-width: 700px; table-layout: auto; }
th, td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #ddd; }
th { background: #2c3e50; color: #fff; font-weight: 600; }

/* STATUS BADGES */
.badge { padding: 5px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
.applied { background: #e0e0e0; color: #333; }
.shortlisted { background: #fff3cd; color: #856404; }
.selected { background: #d4edda; color: #155724; }
.rejected { background: #f8d7da; color: #721c24; }

/* APPLY BUTTON */
.apply-btn { padding: 6px 12px; border-radius: 6px; background: #27ae60; color: #fff; border: none; cursor: pointer; transition: 0.2s; }
.apply-btn:hover { background: #218c4f; }

/* RESPONSIVE */
@media (max-width: 768px) {
  .main-content { padding: 15px; }
  .nav-links button { margin-left: 5px; padding: 6px 10px; font-size: 14px; }
}
</style>