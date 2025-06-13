<template>
    <DataTable :value="enrichedServers" tableStyle="min-width: 50rem">
        <Column field="name" header="Name"></Column>
        <Column field="hostname" header="Hostname"></Column>
        <Column field="port" header="Port"></Column>
        <Column field="username" header="Username"></Column>
        <Column field="auth_type" header="Auth Type"></Column>
        <Column field="tags" header="Tags" class="tagCol">
            <template #body="{ data }">
                <template v-for="tag in data.tags" :key="tag">
                    <Badge class="mr-1"
                        :style="{ 'background-color': tag.color, 'color': isBright(tag.color) ? 'black' : 'white' }">{{
                            tag.name }}</Badge>
                </template>
                <Button label="+" severity="success" rounded class="h-6 w-2 tagAdd"
                    @click="openDialogEditTags(data.id); showTagDialog = true" />
            </template>
        </Column>
        <Column>
            <template #body="{ data }">
                <Button @click="openDialogEditServer(data.id)" icon="icon-pencil" severity="secondary" class="mr-2"
                    rounded v-tooltip.top="'Edit'"></Button>
                <Button @click="confirmDeleteServer(data)" icon="icon-trash" severity="danger" rounded
                    v-tooltip.top="'Delete'"></Button>
            </template>"
        </Column>
    </DataTable>

    <ServerEditTagsDialog v-if="activeServer" v-model:show="showTagDialog" v-model:serverTarget="activeServer" />
    <ServerEditDialog v-if="activeServer" v-model:show="showServerEditDialog" v-model:serverTarget="activeServer" />
</template>

<script setup lang="ts">
import { useServerStore } from '@/stores/ServerStore'
import { storeToRefs } from 'pinia'
import { Badge, Button } from 'primevue'
import { ref } from 'vue'
import { useConfirm } from "primevue/useconfirm";
import { isBright } from '@/utils/utils'
import ServerEditTagsDialog from '@/components/server/ServerEditTagsDialog.vue'
import ServerEditDialog from '@/components/server/ServerEditDialog.vue'

const confirm = useConfirm();
const serverStore = useServerStore()
const { enrichedServers } = storeToRefs(serverStore)

const showTagDialog = ref(false)
const showServerEditDialog = ref(false)

const activeServer = ref<any>(null)

const confirmDeleteServer = (server: any) => {
    confirm.require({
        message: `Are you sure you want to delete the server ${server.name}?`,
        header: 'Delete Server',
        icon: 'icon-trash',
        accept: () => {
            serverStore.deleteServer(server.id)
        },
    })
}

const openDialogEditServer = (serverId: number) => {
    activeServer.value = JSON.parse(JSON.stringify(serverStore.serverById(serverId)))
    showServerEditDialog.value = true
}
const openDialogEditTags = (serverId: number) => {
    activeServer.value = JSON.parse(JSON.stringify(serverStore.serverById(serverId)))
    showTagDialog.value = true
}

</script>