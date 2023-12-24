<template>
    <div :class="{'align-right' : orientation === 'right'}">
        <v-chip>{{isDarkModeOn}}</v-chip>
    </div>
</template>

<script lang="ts">
export default{
    props:{
        orientation:{
            type: String as () => 'left' | 'right',
            default: 'left',
        }
    },
    data(){
        return{
            isDarkModeOn: 'OFF'
        }
    }
}
</script>

<style scoped>
    .align-right{
        text-align: right !important;
    }
</style>