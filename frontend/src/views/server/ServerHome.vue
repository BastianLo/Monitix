<template>

    <Toolbar>
        <template #start>
            <Button class="mr-2" severity="primary" size="small" @click="editServer({})">Create</Button>
        </template>

    </Toolbar>

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
                    @click="editServerTags(data); showTagDialog = true" />
            </template>
        </Column>
        <Column>
            <template #body="{ data }">
                <Button @click="editServer(data)" icon="icon-pencil" severity="secondary" class="mr-2" rounded
                    v-tooltip.top="'Edit'"></Button>
                <Button @click="confirmDeleteServer(data)" icon="icon-trash" severity="danger" rounded
                    v-tooltip.top="'Delete'"></Button>
            </template>"
        </Column>
    </DataTable>

    <Dialog v-model:visible="showServerEditDialog" modal header="Edit Server" :style="{ width: '25rem' }">
        <div class="flex items-center gap-4 mb-4">
            <label for="servername" class="font-semibold w-24">Name</label>
            <InputText id="servername" class="flex-auto" autocomplete="off" v-model="activeServerEdit.name" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="serverhostname" class="font-semibold w-24">Hostname</label>
            <InputText id="serverhostname" class="flex-auto" autocomplete="off" v-model="activeServerEdit.hostname" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="serverport" class="font-semibold w-24">Port</label>
            <InputNumber id="serverport" class="flex-auto" autocomplete="off" v-model="activeServerEdit.port" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="serverusername" class="font-semibold w-24">Username</label>
            <InputText id="serverusername" class="flex-auto" autocomplete="off" v-model="activeServerEdit.username" />
        </div>
        <template #footer>
            <Button label="Cancel" severity="secondary" @click="showServerEditDialog = false" autofocus />
            <Button label="Save" @click="saveEditServer()" autofocus />
        </template>
    </Dialog>

    <Dialog v-model:visible="showTagDialog" modal :header="'Tags for ' + activeServerTagsEdit?.name"
        :style="{ width: '25rem' }">
        <div class="flex flex-col space-y-2">
            <template v-for="tag in tags" :key="tag.id">
                <div>
                    <Badge class="mr-2 cursor-pointer" v-if="activeServerTagsEdit?.tags.includes(tag.id)"
                        severity="danger"
                        @click="activeServerTagsEdit?.tags.splice(activeServerTagsEdit?.tags.indexOf(tag.id), 1)">
                        -
                    </Badge>
                    <Badge class="mr-2 cursor-pointer" v-if="!activeServerTagsEdit?.tags.includes(tag.id)"
                        @click="activeServerTagsEdit?.tags.push(tag.id)" severity="success">
                        +
                    </Badge>
                    <Badge class="w-fit"
                        :style="{ 'background-color': tag.color, 'color': isBright(tag.color) ? 'black' : 'white' }">
                        {{ tag.name }}
                    </Badge>
                </div>
            </template>
            <div class="mb-2">
                <ColorPicker class="mr-2" v-model="tagColor"></ColorPicker>
                <InputText type="text" v-model="newTagName" placeholder="Tag Name" size="small" />
                <badge class="cursor-pointer ml-2" @click="createTag()">create</badge>
            </div>
        </div>
        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="showTagDialog = false"></Button>
            <Button type="button" label="Save" @click="saveEditServerTags()"></Button>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import { useServerStore } from '@/stores/ServerStore'
import { useTagStore } from '@/stores/TagStore'
import { storeToRefs } from 'pinia'
import { Badge, Button, InputNumber, Toolbar } from 'primevue'
import { ref } from 'vue'
import ColorPicker from 'primevue/colorpicker';
import { useConfirm } from "primevue/useconfirm";

const confirm = useConfirm();
const serverStore = useServerStore()
const tagStore = useTagStore()
const { enrichedServers } = storeToRefs(serverStore)
const { tags } = storeToRefs(tagStore)

serverStore.fetchServers()

const activeServerEdit = ref<any>(null)

const showTagDialog = ref(false)
const showServerEditDialog = ref(false)
const activeServerTagsEdit = ref<any>(null)
const tagColor = ref('')
const newTagName = ref('')

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

const editServer = (server: any) => {
    activeServerEdit.value = JSON.parse(JSON.stringify(server))
    showServerEditDialog.value = true
}

const saveEditServer = () => {
    if (activeServerEdit.value) {
        delete activeServerEdit.value.tags
        if (activeServerEdit.value.id) {
            serverStore.patchServer(activeServerEdit.value)
        }
        else {
            serverStore.createServer(activeServerEdit.value)
        }
        showServerEditDialog.value = false
    }
}

const editServerTags = (server: any) => {
    activeServerTagsEdit.value = JSON.parse(JSON.stringify(server))
    activeServerTagsEdit.value.tags = activeServerTagsEdit.value.tags.map((tag: any) => tag.id)
    tagColor.value = (Math.random() * 0xFFFFFF << 0).toString(16)
}
const saveEditServerTags = () => {
    if (activeServerTagsEdit.value) {
        serverStore.patchServer(activeServerTagsEdit.value)
        showTagDialog.value = false
    }
}
const createTag = () => {
    if (newTagName.value.trim() === '') return
    tagStore.createTag(newTagName.value, "#" + tagColor.value)
    newTagName.value = ''
    tagColor.value = ''
}

const isBright = (hex: string) => {
    var hex = hex.substring(1);
    var rgb = parseInt(hex, 16);
    var r = (rgb >> 16) & 0xff;
    var g = (rgb >> 8) & 0xff;
    var b = (rgb >> 0) & 0xff;

    var luma = 0.2126 * r + 0.7152 * g + 0.0722 * b; // per ITU-R BT.709

    return luma > 127
}

</script>
<style scoped>
.tagCol .tagAdd {
    visibility: hidden;
}

.tagCol:hover .tagAdd {
    visibility: visible;
}
</style>