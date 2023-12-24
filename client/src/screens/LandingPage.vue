<template>
  <SwitchTheme />
<div id="main-page-header">
    <h2>Reading Wrapped</h2>
    <h6>Supports Goodreads (for now!)</h6>
    <div class="year-select-dropdown">
      <v-select placeholder="Select Year" v-model="selectedYear" :items="yearOptions" :item-props="itemProps"></v-select>
    </div>
  </div>
  <div id="main-page-links">
    <p>
      To get started, kindly copy and paste the URL of your "my books" page on Goodreads.
      You can find it <a href="https://www.goodreads.com/review/list/">here</a>. The URL should have a format similar to: goodreads.com/review/list/###.
    </p>
    <v-text-field persistent-placeholder placeholder="www.goodreads.com/review/list/"></v-text-field>
  </div>
  <div id="wrapped-btn">
    <v-btn disabled>Wrapped</v-btn>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import SwitchTheme from '../components/SwitchTheme.vue';
const selectedYear = ref(2023);
const yearOptions = ref([] as { text: string; value: number }[]);

const generateYearsForWrapped = () => {
  const date = new Date();
  const currMonth: number = date.getMonth();
  const currYear: number = currMonth === 12 ? date.getFullYear() : date.getFullYear() - 1;
  const years = [];

  for (let i = currYear; i >= currYear - 5; i--) {
    years.push({ text: i.toString(), value: i });
  }

  yearOptions.value = years;
  selectedYear.value = currYear;
};

const itemProps = (item: any) => {
  return {
    title: item.key,
  };
};

onMounted(generateYearsForWrapped);
</script>



<style lang="scss">
#main-page-header{
  h2{
    margin-block-end: 0;
  }
  h6{
    margin-block-start: 0;
  }
  .year-select-dropdown{
    display: flex;
    justify-content: center;
  }
}

</style>