<template>
    <Dialog :visible="show" modal :header="(serverTarget.id ? 'Edit' : 'Create') + ' Server'"
        :style="{ width: '25rem' }">
        <div class="flex items-center gap-4 mb-4">
            <label for="servername" class="font-semibold w-24">Name</label>
            <InputText id="servername" class="flex-auto" autocomplete="off" v-model="serverTarget.name" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="serverhostname" class="font-semibold w-24">Hostname</label>
            <InputText id="serverhostname" class="flex-auto" autocomplete="off" v-model="serverTarget.hostname" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="serverport" class="font-semibold w-24">Port</label>
            <InputNumber id="serverport" class="flex-auto" autocomplete="off" v-model="serverTarget.port" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="serverusername" class="font-semibold w-24">Username</label>
            <InputText id="serverusername" class="flex-auto" autocomplete="off" v-model="serverTarget.username" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="authkey" class="font-semibold w-24">Auth Key</label>
            <Password toggleMask id="authkey" class="flex-auto" autocomplete="off" v-model="serverTarget.auth_key" />
        </div>
        <template #footer>
            <Button label="Cancel" severity="secondary" @click="setShow(false)" autofocus />
            <Button label="Save" @click="saveEditServer()" autofocus />
        </template>
    </Dialog>
</template>

<script setup lang="ts">
import { useServerStore } from '@/stores/ServerStore';
import { Password } from 'primevue';

const props = defineProps({
    show: {
        type: Boolean,
        required: true
    },
    serverTarget: {
        required: true,
        type: Object
    }
})
const emit = defineEmits(['update:show'])

const serverStore = useServerStore()

const saveEditServer = () => {
    if (props.serverTarget) {
        delete props.serverTarget.tags
        if (props.serverTarget.id) {
            serverStore.patchServer(props.serverTarget)
        }
        else {
            serverStore.createServer(props.serverTarget)
        }
        setShow(false)
    }
}
const setShow = (show: boolean) => {
    emit('update:show', show)
}
</script>