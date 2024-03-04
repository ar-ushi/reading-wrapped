<template>
    <div class="progress-container">
      <svg class="progress-circle" viewBox="0 0 100 100">
        <path class="progress-ring" stroke="black" stroke-width="7" fill="transparent"
        :stroke-dasharray="dasharray"
               d="M 50 10
               A 40 40 0 0 1 50 90" />
        <path class="progress-ring" :stroke="color" stroke-width="8" fill="transparent"
        :stroke-dasharray="dasharray" :stroke-dashoffset="dashoffset"
               d="M 50 10
               A 40 40 0 0 1 50 90" />
      </svg>
      <div class="progress-display">
        <slot>
         <div class="inner-progress-number">
            {{ rating }}
         </div>   
        </slot>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue';
  
  const {rating} = defineProps({
    rating:{
        type: Number,
    }
  })
  const circumference = 2 * Math.PI * 40; // Circumference of the circle
  const color = '#007AFF'; // Color of the progress indicator
  const dasharray = `${circumference/2}`;
  const dashoffset = - parseFloat(dasharray) * ((rating == 5 ? 5 : rating)/5)+ circumference/2;
  </script>
  
  <style scoped>
  .progress-container {
    width: 150px;
    height: 150px;
    position: relative;
    display: flex;
    justify-content: center;
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
  .progress-display{
    position: absolute;
    width: 100%;
    height: 100%;
    left: 50%;
    bottom: 12px;
    transform: translateX(-50%);
  }
  .inner-progress-number{
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
  }
  </style>
  