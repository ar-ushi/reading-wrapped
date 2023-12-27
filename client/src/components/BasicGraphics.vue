<template>
    <div class="container">
        <h2>Your Year At A Glance</h2>
        <div class="grid padding-top-1rem">
            <div class="flx-col">
                <h2 class="text-secondary">Total Books Read</h2>
                <h2 class="no-font-weight">{{ totalbooks}}</h2>
            </div>
            <div class="flx-col">
                <h2 class="text-secondary">Total Pages Read</h2>
                <h2 class="no-font-weight">{{ totalpages}}</h2> 
            </div>
        </div>
        <div class="grid  padding-top-1rem">
            <div class="flx-col">
                <h2 class="text-secondary">Most Read Author</h2>
                <h2 class="no-font-weight">{{ totalbooks}}</h2>
            </div>
            <div class="flx-col">
                <h2 class="text-secondary">Total Pages Read</h2>
                <h2 class="no-font-weight">{{ totalpages}}</h2> 
            </div> 
        </div>
    </div>
    </template>
    
    <script setup lang="ts">
    import { ref } from 'vue';
    import { useWrappedStore } from '../store/store';
    
    
    const store = useWrappedStore();
    const wrappedData = ref(store.getWrappedData)
    const totalbooks = wrappedData.value.totalbooksread;
    const totalpages = wrappedData.value.totalpagesread;
    
</script>

<style scoped>
.grid{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.no-font-weight{
    font-weight: 400;
}
</style>
