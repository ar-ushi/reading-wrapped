<!-- Vue Component: BookOpinion -->
<template>
    <div class="grid">
        <div class="flx" v-for="(item, index) in items" :key="index">
      <template v-if="item">
        <img :src="item.bookcover" class="opinion-cover" />
        <div class="grid flx-col" style="margin-left: 5px;">
          <div class="flx-col">
            <div class="rating-text">Average Rating</div>
            <h2 class="text-warning">{{item.avgrating}}</h2>
          </div>
          <div class="flx-col">
            <div class="rating-text">Your Rating</div>
            <h2 class="text-secondary">{{item.rating}}</h2>
          </div>
        </div>
      </template>
    </div>
    </div>
  </template>
  
  <script setup lang=ts>
  import {BookDetails} from '../utils/interface';
  const {items}= defineProps({
    items:{
        type: Array as () => BookDetails[],
    }
  })
  </script>

  <style>
  .opinion-cover{
    max-width:100px;
    height: 125px;
}

.rating-text{
    font-size: 12px;
    font-weight: 500;
}

.grid{
    display: flex;
    justify-content: space-evenly;
    place-items: center;
}
</style>
  