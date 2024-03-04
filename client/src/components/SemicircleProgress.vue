<template>
    <div class="progress-container">
      <svg class="progress-circle" viewBox="0 0 100 100">
        <path class="progress-ring" :stroke="color" stroke-width="8" fill="transparent"
              :stroke-dasharray="circumference" :stroke-dashoffset="dashoffset"
               d="M 50 10
               A 40 40 0 0 1 90 50" />
      </svg>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps, computed } from 'vue';
  
  const {rating} = defineProps({
    rating:{
        type: Number,
    }
  })
  const circumference = 2 * Math.PI * 40; // Circumference of the circle
  const color = '#007AFF'; // Color of the progress indicator
  const dashoffset = computed(() => circumference * (1 - (rating/5)));
  </script>
  
  <style scoped>
  .progress-container {
    width: 100px;
    height: 100px;
    color: aqua;
  }
  
  .progress-circle {
    width: 100%;
    height: 100%;
  }
  
  .progress-ring {
    transition: stroke-dashoffset 0.35s;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
  }
  </style>
  