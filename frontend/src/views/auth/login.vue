<template>
  <div>
    <div class="flex justify-center items-center">
      <div class="mt-4 space-y-4">
        <div class="flex items-center content-stretch text-center mb-4">
          <img src="@/assets/logo.png" alt="Logo" width="80" height="80" />
          <h1 class="text-3xl font-bold">Monitix</h1>
        </div>
        <div class="space-x-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="username" aria-describedby="username-help" />
          <p class="text-red-500" v-if="loginResponse?.details?.username">{{ loginResponse?.details?.username[0] }}</p>
        </div>
        <div class="space-x-2">
          <label for="password">Password</label>
          <InputText id="password" v-model="password" aria-describedby="password-help" />
          <p class="text-red-500" v-if="loginResponse?.details?.password">{{ loginResponse?.details?.password[0] }}</p>
        </div>
        <div>
          <Button @click="login()">Login</Button>
        </div>
          <p class="text-red-500" v-if="loginResponse?.details?.detail">{{ loginResponse?.details?.detail }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import { ref } from "vue";
import { useAuthStore } from "@/stores/AuthStore";
import router from "@/router";
import { Button, InputText } from "primevue";

let username = ref("")
let password = ref("")

let authStore = useAuthStore()
authStore.get_valid_token()

const loginResponse = ref<any>(null)

let login = async () => {
  const response = await authStore.login(username.value, password.value)
  console.log(response)
  loginResponse.value = response
  if (response.response.ok) {
    await router.push(authStore.returnUrl)
  }
}
</script>