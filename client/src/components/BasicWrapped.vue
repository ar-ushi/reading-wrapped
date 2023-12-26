<template>
<div class="container">
    <transition name="fade">
        <div v-if="introText" class="intro-text">
            <h2>Hi {{username}}</h2>
            <h2 class="text-secondary">Ready to dive into your wrapped?</h2>
        </div>
    </transition>
    <p>
    </p>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useWrappedStore } from '../store/store';
import { onMounted } from 'vue';

    const store = useWrappedStore();
    const wrappedData = ref(store.getWrappedData);
    const introText = ref(true)
    const username = wrappedData.value.username;
    const totalbooks = wrappedData.value.totalbooksread;

    onMounted(() => {
        setTimeout(() => {
            introText.value = false
        }, 6000)
    })
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>