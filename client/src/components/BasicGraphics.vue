<template>
    <div class="container">
        <h2>Your Year At A Glance</h2>
        <div class="padding-top-1rem flx-space-evenly">
            <template v-for="book in highestBookCovers">
                <img :src=book class="book-cover"/>
            </template>
        </div>
        <div class="grid padding-top-1rem">
            <div class="flx-col">
                <h2 class="text-secondary">Total Genres</h2>
                <h2 class="no-font-weight">{{ totalbooks}}</h2>
            </div>
            <div class="flx-col">
                <h2 class="text-secondary">Total Minutes Read</h2>
                <h2 class="no-font-weight">{{ minutesspentreading}}</h2> 
            </div>
        </div>
        <div class="grid  padding-top-1rem">
            <div class="flx-col">
                <h2 class="text-secondary">Top 5 Genres</h2>
                <template v-for="genre in top5Genre">
                    <h2 class="font-bold">{{ genre}}</h2>
                </template>
            </div>
            <div class="flx-col">
                <h2 class="text-secondary">Most Read Author</h2>
                <h2 class="no-font-weight">{{mostReadAuthor}}</h2>
                <h2 class="text-secondary">Average Rating</h2>
                <h2 class="no-font-weight">{{avgrating}}</h2> 
 
            </div> 
        </div>
    </div>
    </template>
    
    <script setup lang="ts">
    import { ref } from 'vue';
    import { useWrappedStore } from '../store/store';
    import { WrappedDetails } from '../utils/interface';
    import { convertPagesToMinutes, defineWrappedData, getAverage, getBooksCover, getMostReadGenres, getUniqueAuthors, sortBooks } from '../utils/parseBookDetailsMethods';
    
    const store = useWrappedStore();
    const wrappedData = ref(store.getWrappedData).value as WrappedDetails;
    /* util calls */
    defineWrappedData(wrappedData);
    const totalbooks = wrappedData.totalbooksread;
    const minutesspentreading = convertPagesToMinutes();
    const highestBookCovers = getBooksCover(4, 'bookcover', sortBooks('rating'));
    const [totalAuthorsRead, mostReadAuthor, mostReadBooksByAuthor] = getUniqueAuthors();
    const [countOfTotalGenres,top5Genre] = getMostReadGenres();
    const avgrating = getAverage('rating');
//basic idea -- 3 covers of highest rated book, top author, top genres - books read, minutes read 

</script>

<style scoped>
.grid{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.no-font-weight{
    font-weight: 400;
}
</style>
