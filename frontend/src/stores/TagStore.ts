import { defineStore } from 'pinia'
import authorizedFetch from '@/stores/CommonStore'

const baseUrl = import.meta.env.DEV ? 'http://localhost:8081/api' : window.location.origin + '/api'
export const useTagStore = defineStore('tagStore', {
  state: () => ({
    tags: [] as any[],
  }),
  getters: {},
  actions: {
    async fetchTags() {
      const response = await authorizedFetch(baseUrl + '/tag/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      const jsonResponse = await response.json()
      if (response.ok) {
        console.debug('Tags fetched successfully', jsonResponse)
        this.tags = jsonResponse
      }
    },
    async createTag(name: string, color: string) {
      const response = await authorizedFetch(baseUrl + '/tag/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, color: color }),
      })
      if (response.ok) {
        const jsonResponse = await response.json()
        console.debug('Tag created successfully', jsonResponse)
        await this.fetchTags()
      }
    },
  },
})
