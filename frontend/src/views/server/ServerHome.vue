<template>
    <Toolbar>
        <template #start>
            <Button class="mr-2" severity="primary" size="small" @click="openDialogCreateServer()">Create</Button>
        </template>
    </Toolbar>
    <ServerTable />
    <ServerEditDialog v-if="activeServer" v-model:show="showServerEditDialog" v-model:serverTarget="activeServer" />

</template>

<script setup lang="ts">
import { useServerStore } from '@/stores/ServerStore'
import { Button, Toolbar } from 'primevue'
import { ref } from 'vue'
import ServerTable from '@/components/server/ServerTable.vue';
import ServerEditDialog from '@/components/server/ServerEditDialog.vue';

const serverStore = useServerStore()
serverStore.fetchServers()

const showServerEditDialog = ref(false)
const activeServer = ref<any>(null)

const openDialogCreateServer = () => {
    activeServer.value = {}
    showServerEditDialog.value = true
}

</script>