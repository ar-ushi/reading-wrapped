<template>
  <div id="main-page-header">
    <h2>Reading Wrapped</h2>
    <h6>Supports Goodreads (for now!)</h6>
    <div class="year-select-dropdown">
      <v-select class="custom-select" placeholder="Select Year" v-model="selectedYear" :items="yearOptions" :item-props="itemProps"></v-select>
    </div>
  </div>
  <div id="main-page-links">
    <p>
      To get started, kindly copy and paste the URL of your "my books" page on Goodreads.
      You can find it <a href="https://www.goodreads.com/review/list/">here</a>. The URL should have a format similar to: goodreads.com/review/list/###.
    </p>
    <v-text-field placeholder="www.goodreads.com/review/list/"></v-text-field>
  </div>
  <div id="wrapped-btn">
    <button disabled>Wrapped</button>
  </div>
</template>

<script lang="ts">
export default{
  data(){
    return {
      selectedYear: 2023,
      yearOptions: [] as {text: string, value: number}[]
    };
  },
  mounted(){
    this.generateYearsForWrapped();
  },
  methods: {
    generateYearsForWrapped(){
      const date : Date = new Date();
      const currMonth: number = date.getMonth();
      const currYear : number = (currMonth === 12) ? date.getFullYear() : (date.getFullYear() - 1);
      const years = [];

      for (let i = currYear; i>= currYear - 5; i--){
        years.push({text: i.toString(), value: i});
      }

      this.yearOptions = years;
      this.selectedYear = currYear;
    },
    itemProps(item: any){
      return{
        title: item.key,
      }
    }
  }
}
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