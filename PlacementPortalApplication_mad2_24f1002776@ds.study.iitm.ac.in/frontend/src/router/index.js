import { createRouter, createWebHistory } from "vue-router"

// -----------------------------
// IMPORT VIEWS
// -----------------------------
import LoginView from "../views/LoginView.vue"
import AdminDashboard from "../views/AdminDashboard.vue"
import StudentDashboard from "../views/StudentDashboard.vue"
import CompanyDashboard from "../views/CompanyDashboard.vue"
import AdminStudentView from "../views/AdminStudentView.vue"
import CreateDrive from "../views/CreateDrive.vue"

// ✅ New registration pages
import RegisterStudent from "../views/RegisterStudent.vue"
import RegisterCompany from "../views/RegisterCompany.vue"

// ✅ Student Profile page
import StudentProfile from "../views/StudentProfile.vue"

// -----------------------------
// ROUTES
// -----------------------------
const routes = [
  {
    path: "/",
    redirect: "/login"
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView
  },

  // -----------------------------
  // ADMIN ROUTES
  // -----------------------------
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard
  },
  {
    path: "/admin/student/:id",
    name: "AdminStudentView",
    component: AdminStudentView
  },

  // -----------------------------
  // STUDENT ROUTES
  // -----------------------------
  {
    path: "/student",
    name: "StudentDashboard",
    component: StudentDashboard
  },
  {
    path: "/student/profile",
    name: "StudentProfile",
    component: StudentProfile
  },

  // -----------------------------
  // COMPANY ROUTES
  // -----------------------------
  {
    path: "/company-dashboard",
    name: "CompanyDashboard",
    component: CompanyDashboard
  },
  {
    path: "/company/create-drive",
    name: "CreateDrive",
    component: CreateDrive
  },

  // -----------------------------
  // REGISTRATION ROUTES
  // -----------------------------
  {
    path: "/register-student",
    name: "RegisterStudent",
    component: RegisterStudent
  },
  {
    path: "/register-company",
    name: "RegisterCompany",
    component: RegisterCompany
  }
]

// -----------------------------
// CREATE ROUTER
// -----------------------------
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router