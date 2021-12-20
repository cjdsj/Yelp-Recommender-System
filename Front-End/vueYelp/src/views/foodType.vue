<template>
    <div class="bg-con"></div>

    <div class="pb-52 flex flex-col items-center justify-center w-screen min-h-screen">
        <div class="mt-20">
            <img src="../assets/logo.png" width="250" height="130" alt />
        </div>
        <div
            class="w-8/12 mt-20 text-3xl text-white"
        >Seems like you are a new user. Welcome to Yelp Recommender! Please choose any of the blow categories that you like!</div>
        <div class="border-none my-20 rounded-none card grid grid-cols-4 gap-4">
            <div
                class="form-control rounded-lg p-4 shadow-lg bg-cyan-300"
                v-for="(item,index) in state.regionList"
                :key="index"
            >
                <label class="cursor-pointer label">
                    <span class="label-text mr-2">{{ item }}</span>
                    <input
                        type="checkbox"
                        v-model="state.selectList"
                        :value="item"
                        class="checkbox"
                    />
                </label>
            </div>
        </div>
        <div>
            <button class="btn btn-primary" @click="submit">confirm</button>
        </div>
    </div>
</template>
<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router';

let state = reactive({
    selectList: [],
    regionList: ["Pizza", "Seafood",
        "Chinese", "Vegetarian", "Cafes", "Halal", "Burgers",
        "Nightlife", "Asian Fusion", "Steakhouses", "Salad", "Fast Food", "Bars",
        "Indian", "Buffets", "Mexican", "Barbeque", "Bakeries", "Italian",
        "Delis"]
});
const router = useRouter();

const submit = () => {
    router.push({
        path: "/show",
        query: {
            region: state.selectList
        }
    });
}




</script>
<style>
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
