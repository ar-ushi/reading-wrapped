import { defineStore } from 'pinia';

export interface State {
    bookdetails: object
  }

export const useWrappedStore = defineStore('wrappedstore', {
    state: () => ({wrappeddata: {}}),
    getters: {
        getWrappedData: (state) => state.wrappeddata
    },
    actions:{
        updateWrappedData(value: object) {
            this.wrappeddata = value
        }
    }
})