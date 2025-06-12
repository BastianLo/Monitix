import {defineStore} from 'pinia'
import authorizedFetch from "@/stores/CommonStore";
import {useTagStore} from "@/stores/TagStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8081/api' : window.location.origin + "/api"
export const useServerStore = defineStore("serverStore", {
    state: () => ({
        servers: [] as any[],
    }),
    getters: {
        enrichedServers: (state) => {
            return state.servers.map(server => {
                return {
                    ...server,
                    tags: server.tags.map((id: number) => {return useTagStore().tags.find(tag => tag.id === id)})
                }
            })
        }
    },
    actions: {
        async fetchServers() {
            const response = await authorizedFetch(baseUrl + '/server/', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            })
            const jsonResponse = await response.json()
            if (response.ok) {
                console.debug("Servers fetched successfully", jsonResponse)
                await useTagStore().fetchTags()
                this.servers = jsonResponse
            }
        },
        async patchServer(server: any) {
            const response = await authorizedFetch(baseUrl + '/server/' + server.id + "/", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(server)
            })
            if (response.ok) {
                console.debug("Server updated successfully", server)
                const jsonResponse = await response.json()
                // Update the local server state with the updated server
                const index = this.servers.findIndex(s => s.id === server.id)
                if (index !== -1) {
                    this.servers[index] = jsonResponse
                }
            }
        },
        async deleteServer(serverId: number) {
            const response = await authorizedFetch(baseUrl + '/server/' + serverId + "/", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                }
            })
            if (response.ok) {
                console.debug("Server deleted successfully", serverId)
                // Remove the server from the local state
                this.fetchServers()
            }
        },
        async createServer(server: any) {
            const response = await authorizedFetch(baseUrl + '/server/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(server)
            })
            if (response.ok) {
                console.debug("Server created successfully", server)
                const jsonResponse = await response.json()
                this.servers.push(jsonResponse)
            }
        },
    }
})