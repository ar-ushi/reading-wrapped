<template>
    <div>
        <h2></h2>
        <SwitchTheme />
        <v-tabs align-tabs="center">
            <v-tab></v-tab>
            <v-tab>Stats (for nerds!)</v-tab>
        </v-tabs> 
    </div>
</template>

<script setup lang=ts>
import { computed } from 'vue';
import SwitchTheme from '../components/SwitchTheme.vue';
import { useWrappedStore } from '../store/store';

const store = useWrappedStore();
const wrappedData = computed(() => {
    return store.getWrappedData;
})
console.log(wrappedData);
</script>