<template>
    <v-switch  color="primary" :class="{'align-right' : orientation === 'right'}"  :label="`Dark Mode ${isDarkModeOn}`" v-model="toggleDarkMode"></v-switch>
</template>

<script setup lang="ts">
    import {ref, onMounted, defineProps, watch} from 'vue';
    const {orientation, darkmode} = defineProps({
        orientation: {
         type: String as () => 'left' | 'right',
         default: 'left',
        },
        darkmode: {
        type: Boolean,
        default: true,
        },
    })
    const toggleDarkMode = ref(false);
    const isDarkModeOn = ref('Off');

    onMounted(() => {
        updateDarkMode()
    })

    function updateDarkMode(){
        isDarkModeOn.value = darkmode ? 'On' : 'Off'
        toggleDarkMode.value = darkmode
    }

    watch(toggleDarkMode, (value) => {
        isDarkModeOn.value = value? 'On' : 'Off'
        const root = document.querySelector('#app') as HTMLElement;
        if (value){ //dark mode on 
        root.style.setProperty('color', '#ffffff');
        root.style.setProperty('background-color', '#000000')
        } else{
            root.style.removeProperty('color');
            root.style.removeProperty('background-color');
        }
    })
</script>

<style scoped>
    .align-right{
       display: flex;
       justify-content: flex-end;
    }
</style>