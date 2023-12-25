<template>
    <v-switch  color="primary" :class="{'align-right' : orientation === 'right'}"  :label="`Dark Mode ${isDarkModeOn}`" v-model="toggleDarkMode"></v-switch>
</template>

<script setup lang="ts">
    import {ref, onMounted, defineProps, watch} from 'vue';
    import {useTheme} from 'vuetify'

    const theme = useTheme()
    const {orientation, darkmode} = defineProps({
        orientation: {
         type: String as () => 'left' | 'right',
         default: 'right',
        },
        darkmode: {
        type: Boolean,
        default: false,
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
            theme.global.name.value = 'dark'
            root.style.setProperty('color', '#ffffff');
            root.style.setProperty('background-color', '#000000');
        } else{
            theme.global.name.value='light'
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