<template>
  <div class="admin-wrapper">
    <!-- NAVBAR -->
    <nav class="main-navbar">
      <div class="nav-container">
        <h2 class="brand-logo">Admin<span>Portal</span></h2>
        <div class="nav-links">
          <button :class="{ active: section==='dashboard' }" @click="section='dashboard'">Dashboard</button>
          <button :class="{ active: section==='students' }" @click="section='students'">Students</button>
          <button :class="{ active: section==='companies' }" @click="section='companies'">Companies</button>
          <button :class="{ active: section==='drives' }" @click="section='drives'">Drives</button>
          <button :class="{ active: section==='applications' }" @click="section='applications'">Applications</button>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <!-- MAIN CONTENT -->
    <main class="content-area">

      <!-- DASHBOARD CARDS -->
      <div v-if="section==='dashboard'" class="dashboard-grid">
        <div class="stat-card blue-border">
          <div class="icon-box blue">📊</div>
          <div class="stat-info">
            <h3>Total Students</h3>
            <p>{{ stats.students }}</p>
          </div>
        </div>
        <div class="stat-card green-border">
          <div class="icon-box green">🏢</div>
          <div class="stat-info">
            <h3>Total Companies</h3>
            <p>{{ stats.companies }}</p>
          </div>
        </div>
        <div class="stat-card purple-border">
          <div class="icon-box purple">🚀</div>
          <div class="stat-info">
            <h3>Total Drives</h3>
            <p>{{ stats.drives }}</p>
          </div>
        </div>
        <div class="stat-card orange-border">
          <div class="icon-box orange">📝</div>
          <div class="stat-info">
            <h3>Total Applications</h3>
            <p>{{ stats.applications }}</p>
          </div>
        </div>
      </div>

      <!-- DATA SECTIONS -->
      <section v-else class="data-section">

        <!-- HEADER -->
        <div class="section-header">
          <h3>{{ section.charAt(0).toUpperCase() + section.slice(1) }} Management</h3>
          <div v-if="section==='students'" class="search-bar">
            <input type="text" v-model="searchQuery" placeholder="Search by ID, Name or Email..." @input="searchStudents" />
          </div>
        </div>

        <!-- TABLE CARD -->
        <div class="table-card">
          <table v-if="section==='students'">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Course</th>
                <th>Status</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in students" :key="s.id">
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.email }}</td>
                <td>{{ s.phone }}</td>
                <td>{{ s.course }}</td>
                <td>
                  <span :class="['badge', s.status==='Active' ? 'success' : 'danger']">{{ s.status }}</span>
                </td>
                <td class="text-right">
                  <button class="btn btn-view" @click="viewStudent(s.id)">View</button>
                  <button v-if="s.status==='Active'" class="btn btn-warn" @click="blockStudent(s.id)">Block</button>
                  <button v-else class="btn btn-success" @click="activateStudent(s.id)">Activate</button>
                  <button class="btn btn-danger" @click="deleteStudent(s.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>

          <table v-if="section==='companies'">
            <thead>
              <tr>
                <th>Company</th>
                <th>Email</th>
                <th>Status</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in companies" :key="c.id">
                <td>{{ c.company_name }}</td>
                <td>{{ c.email }}</td>
                <td>
                  <span :class="['badge', c.status==='Approved' ? 'success' : c.status==='Rejected' ? 'danger' : 'neutral']">
                    {{ c.status || 'Pending' }}
                  </span>
                </td>
                <td class="text-right">
                  <button class="btn btn-success" :disabled="c.status==='Approved'" @click="updateStatus(c.id,'Approved')">Approve</button>
                  <button class="btn btn-danger" :disabled="c.status==='Rejected'" @click="updateStatus(c.id,'Rejected')">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>

          <table v-if="section==='drives'">
            <thead>
              <tr>
                <th>ID</th>
                <th>Job Title</th>
                <th>Company</th>
                <th>Deadline</th>
                <th>Status</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="d in drives" :key="d.id">
                <td>{{ d.id }}</td>
                <td>{{ d.job_title }}</td>
                <td>{{ d.company }}</td>
                <td>{{ d.deadline }}</td>
                <td>
                  <span :class="['badge', d.status==='Approved' ? 'success' : d.status==='Closed' ? 'danger' : 'neutral']">
                    {{ d.status || 'Pending' }}
                  </span>
                </td>
                <td class="text-right">
                  <button class="btn btn-success" :disabled="d.status==='Approved'" @click="updateDriveStatus(d.id,'Approved')">Approve</button>
                  <button class="btn btn-warn" :disabled="d.status==='Closed'" @click="updateDriveStatus(d.id,'Closed')">Close</button>
                </td>
              </tr>
            </tbody>
          </table>

          <table v-if="section==='applications'">
            <thead>
              <tr>
                <th>ID</th>
                <th>Student</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in applications" :key="a.id">
                <td>{{ a.id }}</td>
                <td>{{ a.student_name }}</td>
                <td>{{ a.company_name }}</td>
                <td>{{ a.job_title }}</td>
                <td>{{ a.application_date }}</td>
                <td><span class="badge neutral">{{ a.status }}</span></td>
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

  name: "AdminDashboard",

  data() {

    return {

      stats: {},

      students: [],

      companies: [],

      section: "dashboard",
      searchQuery: "",
      drives: [],
      applications: [],
    

    }

  },


  mounted(){

    this.loadDashboard()
    this.loadStudents()
    this.loadCompanies()
    this.loadDrives()
    this.loadApplications()

  },


  methods: {

    getAuthHeader(){

      return {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token")
        }
      }

    },


    async loadDashboard(){

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/dashboard",
        this.getAuthHeader()
      )

      this.stats = res.data

    },


    async loadStudents(){

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/students",
        this.getAuthHeader()
      )

      this.students = res.data

    },
    async searchStudents(){

  if(this.searchQuery === ""){
    this.loadStudents()
    return
  }

  const res = await axios.get(
    `http://127.0.0.1:5000/api/admin/students/search?q=${this.searchQuery}`,
    this.getAuthHeader()
  )

  this.students = res.data

},


    async loadCompanies(){

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/companies",
        this.getAuthHeader()
      )

      this.companies = res.data

    },
    async updateStatus(id,status){

    await axios.put(
        `http://127.0.0.1:5000/api/admin/company/${id}/status`,
        {status:status},
        this.getAuthHeader()
    )

    this.loadCompanies()

    },






    async loadDrives(){

  const res = await axios.get(
    "http://127.0.0.1:5000/api/admin/drives",
    this.getAuthHeader()
  )

  this.drives = res.data

},




async updateDriveStatus(id,status){

  await axios.put(
    `http://127.0.0.1:5000/api/admin/drive/${id}/status`,
    {status:status},
    this.getAuthHeader()
  )

  this.loadDrives()

},


   

    // -------------------------
    // STUDENT ACTION METHODS
    // -------------------------

    viewStudent(id){

      this.$router.push(`/admin/student/${id}`)

    },


    async blockStudent(id){

      await axios.put(
        `http://127.0.0.1:5000/api/admin/student/${id}/block`,
        {},
        this.getAuthHeader()
      )

      this.loadStudents()

    },


    async activateStudent(id){

  await axios.put(
    `http://127.0.0.1:5000/api/admin/student/${id}/activate`,
    {},
    this.getAuthHeader()
  )

  this.loadStudents()
},


    async deleteStudent(id){

      if(confirm("Delete this student?")){

        await axios.delete(
          `http://127.0.0.1:5000/api/admin/student/${id}`,
          this.getAuthHeader()
        )

        this.loadStudents()

      }

    },

    async loadApplications(){
  try{
    const res = await axios.get(
      "http://127.0.0.1:5000/api/admin/applications",
      this.getAuthHeader()
    )
    this.applications = res.data
  }
  catch(err){
    console.error(err)
  }
},

    


    logout(){

      localStorage.removeItem("token")
      localStorage.removeItem("role")

      this.$router.push("/login")

    }

  }

}

</script>

<style scoped>
/* FULL WIDTH LAYOUT */
.admin-wrapper { width: 100%; min-height: 100vh; background: #f4f6fb; font-family: "Segoe UI", sans-serif; }
.main-navbar { width: 100%; background: #1f3c88; color: white; display: flex; align-items: center; justify-content: center; padding: 10px 5%; position: sticky; top: 0; z-index: 100; }
.nav-container { display: flex; justify-content: space-between; width: 100%; max-width: 1600px; }
.nav-links button { margin-left: 10px; padding: 8px 16px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.nav-links button:hover { background: #e8ecff; color: #1f3c88; }
.nav-links button.active { background: white; color: #1f3c88; }
.logout-btn { background: #f44336; color: white; }

/* DASHBOARD CARDS */
.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px,1fr)); gap: 25px; padding: 30px; }
.stat-card { background: white; padding: 25px; border-radius: 12px; display: flex; align-items: center; box-shadow: 0 3px 10px rgba(0,0,0,0.08); transition: 0.2s; }
.stat-card:hover { transform: translateY(-4px); }
.icon-box { width: 50px; height: 50px; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size: 1.5rem; margin-right: 15px; }
.blue { background: #eff6ff; } .green { background: #ecfdf5; } .purple { background: #f5f3ff; } .orange { background: #fffbeb; }
.stat-info h3 { font-size: 0.85rem; color: #64748b; margin:0; text-transform: uppercase; }
.stat-info p { font-size: 2rem; font-weight: 700; margin: 0; color: #1f3c88; }

/* TABLES */
.data-section { padding: 0 20px 40px 20px; max-width: 1600px; margin: auto; }
.table-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
table { width: 100%; border-collapse: collapse; }
th { background: #1f3c88; color: white; padding: 12px; text-align: center; }
td { padding: 12px; text-align: center; border-bottom: 1px solid #eee; word-wrap: break-word; }
tr:nth-child(even) { background: #fafbff; }
.badge { padding: 6px 12px; border-radius: 99px; font-weight: 600; }
.success { background: #dcfce7; color: #166534; }
.danger { background: #fee2e2; color: #991b1b; }
.neutral { background: #f1f5f9; color: #475569; }

/* BUTTONS */
.btn { padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; margin: 0 2px; }
.btn-view { background: #f1f5f9; color: #1f3c88; }
.btn-warn { background: #fff7e6; color: #d97706; }
.btn-success { background: #ecfdf5; color: #059669; }
.btn-danger { background: #fee2e2; color: #b91c1c; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* SEARCH */
.search-bar input { padding: 10px 16px; border-radius: 8px; border: 1px solid #ccc; width: 300px; }
.search-bar input:focus { outline:none; border-color:#1f3c88; box-shadow: 0 0 0 3px rgba(31,60,136,0.15); }

/* RESPONSIVE */
@media(max-width: 900px) { .dashboard-grid { grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); } }
@media(max-width: 600px) { .nav-links { flex-wrap: wrap; } .search-bar input { width: 100%; margin-top: 10px; } }
</style>