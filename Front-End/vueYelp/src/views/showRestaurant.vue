<template>
    <div class="bg-con"></div>
    <div class="card w-3/12 bg-slate-100 rounded shadow-md">
        <div class="card-body bg-white p-3 font-bold">
            <label class="label justify-start">
                <span class="pr-3 inline-block">USER ID :</span>
                {{ userInfo.user_id }}
            </label>
            <label class="label justify-start">
                <span class="pr-3 inline-block">Name :</span>
                {{ userInfo.name }}
            </label>
        </div>
    </div>
    
    <div  class="flex items-center flex-col justify-center w-screen min-h-screen">
        <div>
            <img src="../assets/logo.png" width="250" height="130" alt />
        </div>
         
        <div
            class="mt-20 text-4xl text-white"
        >Here are some restaurants that you may like! Try for it!</div>
        <button v-if="resList.length==0" class="mt-20 btn btn-link btn-lg loading" >loading</button>
        <div v-if="resList.length!=0" class="mt-20 mb-20 card p-0 shadow-xl">
            <div class="card-body p-0">
                <table class="table w-full">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Restaurant</th>
                            <th>Rating</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="hover" v-for="(item,index) in resList" :key="index">
                            <th>{{ index + 1 }}</th>
                            <td>{{ item.name }}</td>
                            <td>{{ item.stars }}</td>
                            <td>{{ item.categories }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>
</template>
<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { getResList } from '../api'

const route = useRoute();
const resList = reactive([])
const userInfo = reactive({})

const getData = (data) => {
    getResList(data).then(res => {
        if (res.state == 0) {
            Object.assign(resList, res.data)
        }
    })
}

onMounted(() => {
    Object.assign(userInfo, route.query)
    getData(userInfo)
    // console.log(route.query);
})




</script>
<style>
.table thead td,
.table thead th {
    --tw-bg-opacity: 1;
    background-color: hsla(var(--b2) / var(--tw-bg-opacity, 2));
    font-weight: 700;
    font-size: 1.125rem;
    line-height: 1.75rem;
    text-transform: none;
}
.bg-con {
    background: url("../assets/2.jpg") no-repeat;
    background-size: 100% 100%;
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}
</style>
