import {defineStore} from 'pinia'
import {useAuthStore} from "@/stores/AuthStore";
import {useRouter} from "vue-router";
import { useToastStore } from "@/stores/ToastStore";

export default async function authorizedFetch(url: string, options: RequestInit = {}): Promise<Response> {
    useCommonStore().request_fetching = true;
    options.headers = {
        ...options.headers,
        Authorization: `Bearer ${await useAuthStore().get_valid_token()}`,
    };
    const fetch_response = fetch(url, options);
    fetch_response.then(() => {
        useCommonStore().request_fetching = false;
    })
    .catch((error) => {
        useToastStore().error("Network Error", "An error occurred while fetching data. Please try again later.");
        console.log("Network Error:", error);
    });
    const status_code = (await fetch_response).status
    if (status_code == 401){
        await useAuthStore().logout()
    }
    else if ( status_code>= 400) {
        useToastStore().error("Request Error", (await fetch_response).statusText);
    }
    return fetch_response;
}

export const useCommonStore = defineStore("commonStore", {
    state: () => ({
        request_fetching: false,
        router: useRouter(),
    }),
    getters: {},
    actions: {}
})