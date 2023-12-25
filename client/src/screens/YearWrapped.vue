<template>
</template>

<script setup lang=ts>
import { Ref, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

    
    const bookdetails: Ref<string|string[]> = ref('');
    const route = useRoute();

    onMounted(() => {
        bookdetails.value = route.params.data;
    })
</script>