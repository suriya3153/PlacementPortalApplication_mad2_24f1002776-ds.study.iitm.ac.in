<template>

<div class="page">

<h2>Student Profile</h2>

<div class="profile">

<p><b>Name:</b> {{ student.name }}</p>
<p><b>Email:</b> {{ student.email }}</p>
<p><b>Phone:</b> {{ student.phone }}</p>
<p><b>Course:</b> {{ student.course }}</p>

<p>
<b>Resume:</b>
<a :href="student.resume" target="_blank">
Download Resume
</a>
</p>

</div>

<h3>Applied Drives</h3>

<table>

<tr>
<th>Drive</th>
<th>Company</th>
<th>Status</th>
</tr>

<tr v-for="a in student.applications" :key="a.drive">

<td>{{ a.drive }}</td>
<td>{{ a.company }}</td>
<td>{{ a.status }}</td>

</tr>

</table>

<button @click="$router.back()">
Back
</button>

</div>

</template>



<script>

import axios from "axios"

export default{

data(){
return{

student:{
applications:[]
}

}
},

mounted(){

this.loadStudent()

},

methods:{

getAuthHeader(){

return{
headers:{
Authorization:"Bearer "+localStorage.getItem("token")
}
}

},

async loadStudent(){

const id = this.$route.params.id

const res = await axios.get(
`http://127.0.0.1:5000/api/admin/student/${id}`,
this.getAuthHeader()
)

this.student = res.data

}

}

}

</script>



<style scoped>

.page{
padding:30px;
}

.profile{
border:1px solid #ddd;
padding:20px;
border-radius:10px;
margin-bottom:20px;
}

table{
width:100%;
border-collapse:collapse;
margin-bottom:20px;
}

th,td{
border:1px solid #ddd;
padding:10px;
}

button{
padding:8px 15px;
}

</style>