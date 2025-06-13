<template>
    <Dialog :visible="show" modal :header="'Tags for ' + serverTarget.name" :style="{ width: '25rem' }">
        <div class="flex flex-col space-y-2">
            <template v-for="tag in tags" :key="tag.id">
                <div>
                    <Badge class="mr-2 cursor-pointer" v-if="serverTarget.tags.includes(tag.id)" severity="danger"
                        @click="serverTarget.tags.splice(serverTarget.tags.indexOf(tag.id), 1)">
                        -
                    </Badge>
                    <Badge class="mr-2 cursor-pointer" v-if="!serverTarget.tags.includes(tag.id)"
                        @click="serverTarget.tags.push(tag.id)" severity="success">
                        +
                    </Badge>
                    <Badge class="w-fit"
                        :style="{ 'background-color': tag.color, 'color': isBright(tag.color) ? 'black' : 'white' }">
                        {{ tag.name }}
                    </Badge>
                </div>
            </template>
            <div class="mb-2">
                <ColorPicker class="mr-2" v-model="newTagColor"></ColorPicker>
                <InputText type="text" v-model="newTagName" placeholder="Tag Name" size="small" />
                <badge class="cursor-pointer ml-2" @click="createTag()">create</badge>
            </div>
        </div>
        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="setShow(false)"></Button>
            <Button type="button" label="Save" @click="saveTags()"></Button>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import { isBright } from '@/utils/utils';
import { ref } from 'vue';
import { useServerStore } from '@/stores/ServerStore';
import { useTagStore } from '@/stores/TagStore';
import { storeToRefs } from 'pinia';

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
const tagStore = useTagStore()
const { tags } = storeToRefs(tagStore)

const newTagColor = ref('')
const newTagName = ref('')

const saveTags = () => {
    if (props.serverTarget) {
        serverStore.patchServer(props.serverTarget)
        setShow(false)
    }
}
const createTag = () => {
    if (newTagName.value.trim() === '') return
    tagStore.createTag(newTagName.value, "#" + newTagColor.value)
    newTagName.value = ''
    newTagColor.value = ''
}

const setShow = (show: boolean) => {
    emit('update:show', show)
}


</script>