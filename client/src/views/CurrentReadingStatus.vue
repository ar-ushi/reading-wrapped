<template>
    <div class="container">
        <div v-if="booksread != 0">
            <h1>aru's books read this year</h1>
            <div>
                <div v-for="rowIndex in gridNumber" :key="rowIndex" class="flx-dis">
                    <div v-for="colIndex in gridNumber" :key="colIndex" class="flx-col space-grid">
                        <img 
                            v-if="(rowIndex - 1) * gridNumber + colIndex <= booksread"
                            class="grid-book-covers"
                            src="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1647789287i/60177373.jpg"
                        />
                        <div v-else class="grey-block grid-book-covers">{{ (rowIndex - 1) * gridNumber + colIndex }}</div>
                    </div>
                </div> 
            </div>
        </div>
        <div v-else>
            <h2>You've not started your reading journey for this year</h2>
            <h4>It's never too late to pick up a book.</h4>
        </div>
        <hr style="margin-top: 1.5rem;">
        <h2>Monthly Wrapped</h2>
        <div class="flx-dis">
            <v-select variant="underlined" label="Months" v-model="selectedMonth" :items="monthOptions"></v-select>
        </div>
        <!-- <div class="flx">
            <h2 class="text-secondary">Total Books Read</h2>
            <h2 class="no-font-weight">{{ monthlystats.totalBooks }}</h2>
        </div>
        <div class="flx">
            <h2 class="text-secondary">Total Pages Read</h2>
            <h2 class="no-font-weight">{{ monthlystats.totalPages }}</h2>
        </div>
        <div class="flx">
            <h2 class="text-success">Average Rating</h2>
            <h2 class="no-font-weight">{{ (monthlystats.totalRating/monthlystats.totalBooks).toPrecision(2)}}</h2>
        </div> -->
    </div>
</template>

<script setup lang="ts">
import { watch } from 'vue';
import { ref } from 'vue';

    const selectedMonth = ref();
    const monthOptions= ref([])
    let booksread = 5;
    const gridNumber = Math.ceil(Math.sqrt(booksread))
    const monthsRef = {
    'January': 'Jan',
    'February': 'Feb',
    'March': 'Mar',
    'April': 'Apr',
    'May': 'May', 
    'June': 'Jun',
    'July': 'Jul',
    'August': 'Aug',
    'September': 'Sep',
    'October': 'Oct',
    'November': 'Nov',
    'December': 'Dec'
    };
    monthOptions.value = Object.keys(monthsRef)
    selectedMonth.value = 'January'

    // const monthlystats = ref({ totalBooks: 0, totalPages: 0, totalRating: 0 });

    // const calculateMonthlyStats = () => {
    // monthlystats.value = monthly.books.reduce((sum, item) => {
    //     if (item.month === monthsRef[selectedMonth.value]) {
    //     sum.totalBooks += 1;
    //     sum.totalPages += item.page;
    //     sum.totalRating += item.rating;
    //     }
    //     return sum;
    // }, { totalBooks: 0, totalPages: 0, totalRating: 0 });
    // };

    // // Initial calculation
    // calculateMonthlyStats();

    // // Watcher for selectedMonth changes
    // watch(selectedMonth, () => {
    // calculateMonthlyStats();
    // });


</script>

<style>
 .v-select{
    max-width: 30% !important;
    min-width: 10%;
  }
.grid-book-covers{
    height:70px;
    width:50px;
    border-radius: 5px;
}

.grey-block{
    background-color: rgb(var(--v-theme-bookbg)); 
    display: flex;
    align-items: center;
    justify-content: space-around;
    font-size: 1em;
    color: var(--v-theme-book);
}

.space-grid{
    margin-right: 1rem;
    margin-top: 0.5rem
}
</style>