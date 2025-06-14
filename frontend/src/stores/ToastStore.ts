import { useToast } from 'primevue/usetoast'
import { defineStore } from 'pinia'

export const useToastStore = defineStore('toastStore', {
  state: () => ({
    toast: useToast(),
  }),
  getters: {},
  actions: {
    success(title: string, message: string, life: number = 3000) {
      this.toast.add({ severity: 'success', summary: title, detail: message, life: life })
    },
    error(title: string, message: string, life: number = 3000) {
      this.toast.add({ severity: 'error', summary: title, detail: message, life: life })
    },
    info(title: string, message: string, life: number = 3000) {
      this.toast.add({ severity: 'info', summary: title, detail: message, life: life })
    },
    warn(title: string, message: string, life: number = 3000) {
      this.toast.add({ severity: 'warn', summary: title, detail: message, life: life })
    },
  },
})
