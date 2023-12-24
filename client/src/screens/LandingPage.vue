<template>
  <SwitchTheme orientation="right" />
  <div class="container">
    <div id="main-page-header">
    <h2>Reading Wrapped</h2>
    <h6>Supports Goodreads (for now!)</h6>
  </div>
  <div id="main-page-links">
    <p>
      To get started, kindly copy and paste the URL of your "my books" page on Goodreads.
      You can find it <a href="https://www.goodreads.com/review/list/">here</a>. The URL should have a format similar to: goodreads.com/review/list/###.
    </p>
    <div class="input-container">
      <v-select variant="underlined" placeholder="Select Year" v-model="selectedYear" :items="yearOptions"></v-select>
      <v-text-field variant="underlined" v-model="url" validate-on="input lazy" :rules=[validateURL] persistent-placeholder placeholder="www.goodreads.com/review/list/"></v-text-field>
    </div>
  </div>
  <div id="wrapped-btn">
    <v-btn :disabled="isBtnDisabled">Wrapped</v-btn>
  </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import SwitchTheme from '../components/SwitchTheme.vue';
const selectedYear = ref(2023);
const yearOptions = ref([] as { title: string; value: number }[]);
const url = ref('');
const isBtnDisabled = ref(true);
const validateURL = (value : string) => {
  if (value.includes('www.goodreads.com/review/list/')){
    isBtnDisabled.value = false;
    return true
  }
  return 'Please enter the expected input for Wrapped'
}
const generateYearsForWrapped = () => {
  const date = new Date();
  const currMonth: number = date.getMonth();
  const currYear: number = currMonth === 11 ? date.getFullYear() : date.getFullYear() - 1;
  const years = [];

  for (let i = currYear; i >= currYear - 5; i--) {
    years.push({ title: i.toString(), value: i });
  }

  yearOptions.value = years;
  selectedYear.value = currYear;
};

onMounted(generateYearsForWrapped);
watch(selectedYear, (newValue, oldValue) => {
  console.log('Selected Year changed:', newValue);
});</script>



<style lang="scss">
.container{
  text-align: center;
  #main-page-header{
  h2{
    margin-block-end: 0;
  }
  h6{
    margin-block-start: 0;
  }
}
#main-page-links{
  padding-top: 3rem;
  .input-container{
    display: flex;
    justify-content: space-evenly;
    padding-top: 0.5rem;
}
  .v-select{
    max-width: 70px !important;
  }
  .v-text-field{
    max-width: 40%;
  }
}
}
</style>