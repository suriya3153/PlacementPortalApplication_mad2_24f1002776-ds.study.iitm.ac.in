<template>
  <div class="admin-wrapper">
    <nav class="main-navbar">
      <div class="nav-container">
        <h2 class="brand-logo">Company<span>Portal</span></h2>
        <div class="nav-links">
          <button :class="{ active: section==='dashboard' }" @click="section='dashboard'">Dashboard</button>
          <button :class="{ active: section==='my-drives' }" @click="section='my-drives'">My Drives</button>
          <button :class="{ active: section==='applications' }" @click="section='applications'">Applications</button>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <main class="content-area">

      <div v-if="section==='dashboard'" class="dashboard-grid">
        <div class="stat-card blue-border">
          <div class="icon-box blue">🏢</div>
          <div class="stat-info">
            <h3>Company Name</h3>
            <p style="font-size: 1.2rem;">{{ company.company_name }}</p>
          </div>
        </div>
        <div class="stat-card green-border">
          <div class="icon-box green">🚀</div>
          <div class="stat-info">
            <h3>Total Drives</h3>
            <p>{{ stats.drives }}</p>
          </div>
        </div>
        <div class="stat-card purple-border">
          <div class="icon-box purple">👥</div>
          <div class="stat-info">
            <h3>Total Applicants</h3>
            <p>{{ stats.applicants }}</p>
          </div>
        </div>
        <div class="stat-card orange-border" style="cursor:pointer" @click="goToCreateDrive">
          <div class="icon-box orange">➕</div>
          <div class="stat-info">
            <h3>New Drive</h3>
            <p style="font-size: 1rem; color: #d97706;">Post Placement</p>
          </div>
        </div>
      </div>

      <section v-else class="data-section">
        
        <div class="section-header">
          <h3>{{ section === 'my-drives' ? 'My Placement Drives' : 'Student Applications' }}</h3>
        </div>

        <div class="table-card">
          <table v-if="section==='my-drives'">
            <thead>
              <tr>
                <th>ID</th>
                <th>Job Title</th>
                <th>Applicants</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="d in drives" :key="d.id">
                <td>{{ d.id }}</td>
                <td>{{ d.job_title }}</td>
                <td>{{ d.applicants }}</td>
                <td>
                  <span :class="['badge', d.status==='Approved' ? 'success' : d.status==='Closed' ? 'danger' : 'neutral']">
                    {{ d.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>

          <table v-if="section==='applications'">
            <thead>
              <tr>
                <th>ID</th>
                <th>Student Name</th>
                <th>Student Email</th>
                <th>Drive</th>
                <th>Status</th>
                <th>Resume</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in applications" :key="a.id">
  <td>{{ a.id }}</td>
  <td>{{ a.student_name }}</td>
  <td>{{ a.student_email }}</td>
  <td>{{ a.drive_title }}</td>
  <td>
    <select v-model="a.status" class="status-select">
      <option value="Applied">Applied</option>
      <option value="Shortlisted">Shortlisted</option>
      <option value="Selected">Selected</option>
      <option value="Rejected">Rejected</option>
    </select>
  </td>
  <td>
    <span v-if="a.resume">
      <a :href="'http://127.0.0.1:5000/download/' + a.resume" target="_blank" download>
        Download PDF
      </a>
    </span>
    <span v-else>N/A</span>
  </td>
  <td class="text-right">
    <button class="btn btn-success" @click="updateApplicationStatus(a)">Save Changes</button>
  </td>
</tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyDashboard",

  data() {
    return {
      section: "dashboard",
      company: {},
      stats: {},
      drives: [],
      applications: [],
      errorMessage: ""
    }
  },

  mounted() {
    this.loadAllData()
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      if (!token || token === "undefined") {
        this.$router.push("/login");
        return { headers: {} };
      }
      return {
        headers: {
          Authorization: `Bearer ${token}`
        }
      };
    },
    goToCreateDrive() {
      this.$router.push("/company/create-drive")
    },
    async updateApplicationStatus(application) {
      try {
        const res = await axios.put(
          `http://127.0.0.1:5000/api/company/applications/${application.id}/status`,
          { status: application.status },
          this.getAuthHeader()
        );
        alert(res.data.message || "Status updated successfully");
      } catch (error) {
        console.error(error);
        alert("Failed to update status");
      }
    },

    async loadAllData() {
      try {
        await this.loadCompany()
        await this.loadStats()
        await this.loadDrives()
        await this.loadApplications()
      } catch (error) {
        if (error.response && (error.response.status === 401 || error.response.status === 422)) {
          localStorage.removeItem("token")
          this.$router.push("/login")
        } else {
          this.errorMessage = "Failed to load data."
          console.error(error)
        }
      }
    },

    async loadCompany() {
      const res = await axios.get("http://127.0.0.1:5000/api/company/me", this.getAuthHeader())
      this.company = res.data
    },

    async loadStats() {
      const res = await axios.get("http://127.0.0.1:5000/api/company/stats", this.getAuthHeader())
      this.stats = res.data
    },

    async loadDrives() {
      const res = await axios.get("http://127.0.0.1:5000/api/company/drives", this.getAuthHeader())
      this.drives = res.data
    },

    async loadApplications() {
      const res = await axios.get("http://127.0.0.1:5000/api/company/applications", this.getAuthHeader())
      this.applications = res.data
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    }
  }
}
</script>

<style scoped>
/* FULL WIDTH LAYOUT (Mirroring Admin Portal) */
.admin-wrapper { width: 100%; min-height: 100vh; background: #f4f6fb; font-family: "Segoe UI", sans-serif; }
.main-navbar { width: 100%; background: #1f3c88; color: white; display: flex; align-items: center; justify-content: center; padding: 10px 5%; position: sticky; top: 0; z-index: 100; }
.nav-container { display: flex; justify-content: space-between; width: 100%; max-width: 1600px; }
.brand-logo span { color: #8ba2e0; font-weight: 300; }

.nav-links button { margin-left: 10px; padding: 8px 16px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; background: transparent; color: white; }
.nav-links button:hover { background: #e8ecff; color: #1f3c88; }
.nav-links button.active { background: white; color: #1f3c88; }
.logout-btn { background: #f44336 !important; color: white !important; }

.content-area { padding: 20px 0; }

/* DASHBOARD CARDS */
.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; padding: 30px; max-width: 1600px; margin: auto; }
.stat-card { background: white; padding: 25px; border-radius: 12px; display: flex; align-items: center; box-shadow: 0 3px 10px rgba(0,0,0,0.08); transition: 0.2s; }
.stat-card:hover { transform: translateY(-4px); }
.icon-box { width: 50px; height: 50px; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size: 1.5rem; margin-right: 15px; }

.blue { background: #eff6ff; } .green { background: #ecfdf5; } .purple { background: #f5f3ff; } .orange { background: #fffbeb; }
.stat-info h3 { font-size: 0.85rem; color: #64748b; margin:0; text-transform: uppercase; }
.stat-info p { font-size: 1.8rem; font-weight: 700; margin: 0; color: #1f3c88; }

/* TABLES & DATA SECTIONS */
.data-section { padding: 0 30px 40px 30px; max-width: 1600px; margin: auto; }
.section-header { margin-bottom: 20px; color: #1f3c88; }
.table-card { background: white; border-radius: 12px; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }

table { width: 100%; border-collapse: collapse; min-width: 900px; } /* Ensures table stays wide enough */
th { background: #1f3c88; color: white; padding: 15px; text-align: left; }
td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
tr:nth-child(even) { background: #fafbff; }

/* BADGES & SELECTS */
.badge { padding: 6px 12px; border-radius: 99px; font-weight: 600; font-size: 0.8rem; }
.success { background: #dcfce7; color: #166534; }
.danger { background: #fee2e2; color: #991b1b; }
.neutral { background: #f1f5f9; color: #475569; }

.status-select { padding: 6px; border-radius: 4px; border: 1px solid #ccc; font-family: inherit; }

/* BUTTONS */
.btn { padding: 8px 16px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer; border: none; }
.btn-success { background: #1f3c88; color: white; }
.btn-success:hover { background: #2d54bd; }
.text-right { text-align: right; }

@media(max-width: 600px) {
  .nav-container { flex-direction: column; gap: 10px; }
  .nav-links { display: flex; flex-wrap: wrap; justify-content: center; }
}
</style>