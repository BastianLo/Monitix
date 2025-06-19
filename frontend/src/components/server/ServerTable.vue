<template>
    <DataTable :value="enrichedServers" tableStyle="min-width: 50rem">
        <Column field="ping_successful" class="text-center w-min" style="padding-right: 0px;">
            <template #body="{ data }">
                <span class="status-bubble" v-tooltip="timeAgo(data.last_ping, currentTime)" :style="{
                    'background-color': secondsPassed(data.last_ping) > 300 ? '#555555' : data.ping_successful ? '#22c522' : '#ef4444'
                }"></span>
            </template>
        </Column>
        <Column field="name" header="Name"></Column>
        <Column field="hostname" header="Hostname"></Column>
        <Column field="latestMetrics.ram_used" , header="Ram">
            <template #body="{ data }">
                <template v-if="data.latestMetrics">
                    <ProgressBar :value="calculateRamPercentage(data.latestMetrics)"
                        :pt:value:class="getBarColor(calculateRamPercentage(data.latestMetrics), 80, 60, 40, true)">
                    </ProgressBar>
                </template>
            </template>
        </Column>
        <Column field="latestMetrics.cpu_used" , header="CPU">
            <template #body="{ data }">
                <template v-if="data.latestMetrics">
                    <ProgressBar :value="Math.round(data.latestMetrics.cpu_used)"
                        :pt:value:class="getBarColor(Math.round(data.latestMetrics.cpu_used), 80, 60, 40, true)">
                    </ProgressBar>
                </template>
            </template>
        </Column>
        <Column field="latestMetrics.disk_used" , header="Disk">
            <template #body="{ data }">
                <template v-if="data.latestMetrics">
                    <ProgressBar :value="calculateDiskPercentage(data.latestMetrics)"
                        :pt:value:class="getBarColor(calculateDiskPercentage(data.latestMetrics), 80, 60, 40, true)">
                    </ProgressBar>
                </template>
            </template>
        </Column>
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
import { Badge, Button, ProgressBar } from 'primevue'
import { ref, onMounted, onUnmounted } from 'vue'
import { useConfirm } from "primevue/useconfirm";
import { getBarColor, isBright, secondsPassed, timeAgo } from '@/utils/utils'
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

const calculateRamPercentage = (latestMetrics: any) => {
    if (!latestMetrics) return 0;
    return Math.round(latestMetrics.ram_used / (latestMetrics.ram_available + latestMetrics.ram_used) * 100);
}

const calculateDiskPercentage = (latestMetrics: any) => {
    if (!latestMetrics) return 0;
    return Math.round(latestMetrics.disk_used / (latestMetrics.disk_available + latestMetrics.disk_used) * 100)
}

const currentTime = ref(new Date());
let intervalId: number | undefined;

onMounted(() => {
    intervalId = setInterval(() => {
        currentTime.value = new Date()
        serverStore.fetchServers()

    }, 30000);
});

onUnmounted(() => {
    if (intervalId) {
        clearInterval(intervalId);
    }
});
</script>
<style scoped>
.tagCol .tagAdd {
    visibility: hidden;
}

.tagCol:hover .tagAdd {
    visibility: visible;
}

.customProgress .ui-progressbar .ui-progressbar-label {
    color: yellow;
}
</style>
