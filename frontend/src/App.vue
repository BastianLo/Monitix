<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/AuthStore'
import { ref } from 'vue'
import Menubar from 'primevue/menubar'
import { Avatar } from 'primevue'

const authStore = useAuthStore()
const logout = async () => {
    await authStore.logout()
    window.location.reload()
}
const router = useRouter()

const visible = ref(false)

const items = ref([
    {
        label: 'Menu',
        icon: 'icon-list',
        command: () => {
            visible.value = !visible.value
        },
    },
    {
        label: 'Server',
        icon: 'icon-server',
        command: () => {
            router.push({ name: 'serverHome' })
        },
    },
])
</script>

<template>
    <Menubar :model="items">
        <template #start>
            <RouterLink :to="{name: 'home'}">
                <img src="@/assets/logo.png" alt="Logo" width="40" height="40" />
            </RouterLink>
            <RouterLink :to="{name: 'home'}" class="text-3xl font-bold">Monitix</RouterLink>
        </template>

        <template #end>
            <div class="flex items-center gap-2">
                <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" />
            </div>
        </template>
    </Menubar>
    <div class="card flex justify-center">
        <Drawer v-model:visible="visible" header="Drawer" :permanent="true">
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                laboris nisi ut aliquip ex ea commodo consequat.
            </p>
        </Drawer>
    </div>
    <RouterView />
    <ConfirmDialog></ConfirmDialog>
    <Toast />

</template>
