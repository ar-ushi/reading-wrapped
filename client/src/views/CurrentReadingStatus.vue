<template>
    <div class="container">
        <h3>Monthly Wrapped</h3>
        <div class="flx-flx-end">
            <v-select multiple variant="underlined" label="Months" v-model="selectedMonth" :items="monthOptions"></v-select>
        </div>
        <semicircle-progress></semicircle-progress>
        <v-progress-circular
            :size="50"
            :width="20"
            :value="(monthlystats.totalRating/monthlystats.totalBooks).toPrecision(2)"
            color="primary"
          >
            <span>{{ (monthlystats.totalRating/monthlystats.totalBooks).toPrecision(2)}}</span>
          </v-progress-circular>        <div class="flx-space-btwn">
            <h2 class="text-info">Total Books Read</h2>
            <h2 class="no-font-weight">{{ monthlystats.totalBooks }}</h2>
        </div>
        <div class="flx-space-btwn">
            <h2 class="text-info">Total Pages Read</h2>
            <h2 class="no-font-weight">{{ monthlystats.totalPages }}</h2>
        </div>
        <div class="flx-space-btwn">
            <h2 class="text-info">Average Rating</h2>
            <h2 class="no-font-weight">{{ (monthlystats.totalRating/monthlystats.totalBooks).toPrecision(2)}}</h2>
        </div>  
        <div v-if="totalBooksRead != 0">
            <h1>{{ username }}'s books read this year</h1>
            <div>
                <div v-for="rowIndex in gridNumber" :key="rowIndex" class="flx-dis">
                    <div v-for="colIndex in gridNumber" :key="colIndex" class="flx-col space-grid">
                        <img 
                            v-if="(rowIndex - 1) * gridNumber + colIndex <= totalBooksRead"
                            class="grid-book-covers"
                            :src="monthly[(rowIndex-1)*gridNumber+colIndex-1].bookcover"
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
        
    </div>
</template>

<script setup lang="ts">
    import { watch } from 'vue';
    import { ref } from 'vue';
    import { useWrappedStore } from '../store/store';
    import { WrappedDetails } from '../utils/interface';
    import { toRaw } from 'vue';
    import SemicircleProgress from '../components/SemicircleProgress.vue';

    const store = useWrappedStore();
    const monthlyData = ref(store.getWrappedData);
    const username = (monthlyData.value as WrappedDetails).username;
    const monthly = toRaw((monthlyData.value as WrappedDetails).books);
    const selectedMonth = ref();
    const monthOptions= ref([])
    const currMonth = new Date().getMonth()
    const totalBooksRead = monthly.length
    const gridNumber = Math.ceil(Math.sqrt(totalBooksRead))
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
    
    monthOptions.value = Object.keys(monthsRef).map((month, i) => {
        if (i > currMonth){
            return {title: month, props: {disabled: true}}
        } else{
            return {title: month}
        }
    })
    selectedMonth.value = 'January'

    const monthlystats = ref({ totalBooks: 0, totalPages: 0, totalRating: 0 });

    const calculateMonthlyStats = () => {
    monthlystats.value = monthly.reduce((sum, item) => {
        if (item.month === monthsRef[selectedMonth.value]) {
        sum.totalBooks += 1;
        sum.totalPages += parseInt(item.page);
        sum.totalRating += parseInt(item.rating);
        }
        return sum;
    }, { totalBooks: 0, totalPages: 0, totalRating: 0 });
    };

    // Initial calculation
    calculateMonthlyStats();

    // Watcher for selectedMonth changes
    watch(selectedMonth, () => {
    calculateMonthlyStats();
    });
</script>

<style>
 .v-select{
    max-width: 30% !important;
    min-width: 10%;
  }
.grid-book-covers{
    height:80px;
    width:60px;
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

.v-menu>.v-overlay__content>.v-card, .v-menu>.v-overlay__content>.v-list, .v-menu>.v-overlay__content>.v-sheet {
    background-color: rgb(var(--v-theme-background));
    color: rgb(var(--v-theme-book));
}
</style>