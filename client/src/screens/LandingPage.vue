<template>
  <SwitchTheme orientation="right" />
  <div class="container">
    <div id="main-page-header">
    <h2>Reading Wrapped</h2>
    <h6>Supports Goodreads (for now!)</h6>
  </div>
  <div id="main-page-links">
    <p>
      To get started, kindly copy and paste the ID of your account on Goodreads.
      You can find it <a href="https://www.goodreads.com/review/list/">here</a>.
      <span class="url-help">
        The URL should have a format similar to: goodreads.com/review/list/### where ### is the account id.
      </span>
    </p>
    <div class="input-container">
      <v-select variant="underlined" label="Reading Year" v-model="selectedYear" :items="yearOptions"></v-select>
      <v-text-field variant="underlined" v-model="uid" label="www.goodreads.com/review/list/" placeholder="########" persistent-placeholder></v-text-field>
    </div>
  </div>
  <div id="wrapped-btn">
    <v-btn color='primary' :disabled="isBtnDisabled" :loading="loading" @click="fetchBookDetails">Wrapped</v-btn>
    <v-dialog v-model="loading" width="auto" height="auto" :scrim="false" persistent>
    <v-card color="primary">
      <v-card-text>
        Please be patient as we are parsing your Goodreads Data.This process may take upto 2-3 minutes.
        <v-progress-linear
            indeterminate
            color=white
          ></v-progress-linear>
      </v-card-text>
    </v-card>
    </v-dialog>
  </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import SwitchTheme from '../components/SwitchTheme.vue';

const selectedYear = ref(2023);
const yearOptions = ref([] as { title: string; value: number }[]);
const uid = ref('');
const isBtnDisabled = ref(true);
const loading = ref(false);
const fetchBookDetails = async () => {
  try {
    loading.value = !loading.value;
    const response = await fetch(`http://127.0.0.1:5000/wrapped?gr_user_id=${uid.value}&year=${selectedYear.value}`);
    if (response.status === 200){
      const data = await response.json();
    }
  } catch (error) {
    console.error('Error Fetching Data:', error)
  } finally{
    loading.value = false;
  }
} //TODO - Figure out what to show for 'Error Fetching Data'
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
watch(uid, (newValue) => {
  isBtnDisabled.value = newValue.trim() === '';
});
</script>



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
    padding: 1rem 0 1rem 0;
}
  .v-select{
    max-width: 70px !important;
  }
  .v-text-field{
    max-width: 40%;
 }
 .url-help{
  font-size: 12px;
 }
}
}
</style>