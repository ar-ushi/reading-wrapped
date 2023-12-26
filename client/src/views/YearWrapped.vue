<template>
    <div class="container">
        <h1>{{ username }}'s year in books</h1>
        <v-tabs align-tabs="end" color="primary" v-model='activeTab'>
            <v-tab @click="setActiveTab('wrapped')" key="wrapped">Wrapped</v-tab>
            <v-tab @click="setActiveTab('stats')" key="stats">Stats (for nerds!)</v-tab>
        </v-tabs>
        <div v-if="activeTab === 'wrapped'" class="">
            <BasicWrapped />
        </div>
    </div>
</template>

<script setup lang=ts>
import { onMounted, ref } from 'vue';
import { useWrappedStore } from '../store/store';
import BasicWrapped from '../components/BasicWrapped.vue';

const store = useWrappedStore();
const wrappedData = ref(store.getWrappedData);
const username = wrappedData.value.username;
const activeTab = ref('wrapped');

onMounted(() => {
    activeTab.value = 'wrapped'
})
const setActiveTab = (value: string) => {
    activeTab.value = value
}
</script>