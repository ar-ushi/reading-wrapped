<template>
  <div class="container">
    <div id="main-page-header">
    <h1 class="text-secondary">Track Your Reading</h1>
    <h5>Supports Goodreads (for now!)</h5>
  </div>
  <div id="main-page-links">
    <p>
      To get started, kindly copy and paste the ID of your account on Goodreads.
      You can find it <a href="https://www.goodreads.com/review/list/">here</a>.
      <br>
      <span class="url-help">
        The URL should have a format similar to: goodreads.com/review/list/### where ### is the account id.
      </span>
    </p>
    <div class="input-container">
      <v-select variant="underlined" label="Reading Year" v-model="selectedYear" :items="yearOptions"></v-select>
      <v-text-field variant="underlined" validate-on="lazy" :rules=[validateInput] v-model="uid" label="www.goodreads.com/review/list/" placeholder="########" persistent-placeholder></v-text-field>
    </div>
  </div>
  <div id="wrapped-btn">
    <v-btn color='primary' :disabled="isBtnDisabled" :loading="loading" @click="fetchBookDetails">Wrapped</v-btn>
    <v-dialog v-model="loading" width="400" :scrim="false" persistent>
    <v-card color="primary" variant="outlined">
      <v-card-text>
        Please be patient as we are parsing your Goodreads Data. This process may take upto 2-3 minutes.
      </v-card-text>
      <v-progress-linear
          indeterminate
          color=primary
        ></v-progress-linear>
    </v-card>
    </v-dialog>
  </div>
  </div>
  <reading-footer />
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import {useWrappedStore} from '../store/store';
import ReadingFooter from '../components/ReadingFooter.vue';

const selectedYear = ref();
const yearOptions = ref([] as { title: string; value: number }[]);
const uid = ref('');
const isBtnDisabled = ref(true);
const loading = ref(false);
const router = useRouter();
const store = useWrappedStore();
const date = new Date();
const currYear: number = date.getFullYear();

const generateYearsForWrapped = () => {
  const years = [];

  for (let i = currYear; i >= currYear - 5; i--) {
    years.push({ title: i.toString(), value: i });
  }

  yearOptions.value = years;
  selectedYear.value = currYear;
};

onMounted(generateYearsForWrapped);

const validateID = async (uid: string) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/wrapped/validateID?uid=${uid}`)
    if (response.status === 200){
      const data = await response.json()
      if (!data.Status){
        return data.Message
      }
      isBtnDisabled.value = false
    return true
    }
  return 'Account ID must be of 8 digits'
  } catch (error) {
    console.error('Error Fetching Data:', error) 
  }
}

function debounce(func, delay= 3000){
  let timeoutid;
  return function(...args){
    clearTimeout(timeoutid);
    timeoutid = setTimeout(() =>{
      func.call(this, ...args)
    }, delay)
  }
}

const debounceValidateID = debounce(validateID)

const validateInput = (value) =>{
  return debounceValidateID(value);
};

const fetchBookDetails = async () => {
  try {
    loading.value = !loading.value;
    const response = await fetch(`http://127.0.0.1:8000/wrapped/yearlystats?uid=${uid.value}&year=${selectedYear.value}`);
    if (response.status === 200){
      const data = await response.json();
      //update global state
      store.updateWrappedData(data);
      if (selectedYear.value !== currYear || date.getMonth() === 11){
        router.push({
        name: 'Wrapped',
        params: {uid: uid.value }
      })
      } else{ //current year selected & it's not december
      router.push({
          name: 'Reading Status',
          params: {uid: uid.value}
        })
      }
    }
  } catch (error) {
    console.error('Error Fetching Data:', error)
  } finally{
    loading.value = false;
  }
} //TODO - Figure out what to show for 'Error Fetching Data'
</script>



<style lang="scss">
  #main-page-header{
  h5{
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
    min-width: 10%;
  }
  .v-text-field{
    max-width: 40%;
 }
 .url-help{
  font-size: 12px;
 }
}
</style>

<style scoped>
 .v-card{
  background-color: white;
 }

 .v-card-text{
  font-size: 10px;
 }
</style>