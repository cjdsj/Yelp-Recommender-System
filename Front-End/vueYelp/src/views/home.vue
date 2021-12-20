<template>
  <div
    class="home-con pb-52 bg-slate-100 flex flex-col items-center justify-center w-screen h-screen"
  >
    <div>
      <img src="../assets/logo.png" width="250" height="130" alt />
    </div>

    <div class="flex mt-20 flex-row form-control card bg-white rounded-lg">
      <label class="label">
        <span class="pl-2 label-text">My User ID:</span>
      </label>
      <div>
        <div class="relative">
          <input
            type="text"
            v-model="id"
            @keyup.enter="submit"
            placeholder="Search"
            style="width: 30vw;"
            class="pr-16 input input-ghost border-none"
          />
          <button
            @click="submit"
            :class="loading ? 'loading' : ''"
            :disabled="loading"
            class="absolute px-8 top-0 rounded-none right-0 btn"
            style="background-color: #c4372e;"
          >
            <img v-if="!loading" src="../assets/search.png" width="20" height="20" alt />
            {{ loading ? 'LOADING' : '' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { getRestaurant } from '../api'
import { useRouter } from 'vue-router';

let id = ref('');
const router = useRouter();

let loading = ref(false)
const submit = () => {
  if (loading.value) {
    return
  }

  loading.value = true

  getRestaurant({ uid: id.value }).then(res => {
    if (res.state == 0) {
      router.push({
        path: "/show",
        query: {
          ...res.data
        }
      });
    } else if (res.state == 1) {
      router.push({
        path: "/food",
      });
    }
  }, () => {
    loading.value = false
  })
};



</script>
<style>
.home-con {
  background: url("../assets/20211213114714.jpg") 100% 100%;
}
</style>
