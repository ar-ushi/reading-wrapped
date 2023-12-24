<template>
    <v-chip>{{ isDarkModeOn }}</v-chip>
</template>

<script lang="ts">
export default{
    data(){
        return{
            isDarkModeOn: 'OFF'
        }
    }
}
</script>