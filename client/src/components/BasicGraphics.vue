<template>
    <div class="container" id="graphic-stats">
        <h2>Your Year At A Glance</h2>
        <div class="padding-top-1rem flx-space-evenly">
            <template v-for="book in highestBookCovers">
                <img :src=book class="book-cover"/>
            </template>
        </div>
        <div class="grid padding-top-1rem">
            <div class="flx-col">
                <h2 class="text-secondary">Total Books Read</h2>
                <h2 class="no-font-weight">{{ totalbooks}}</h2>
            </div>
            <div class="flx-col">
                <h2 class="text-secondary">Total Minutes Read</h2>
                <h2 class="no-font-weight">{{ minutesspentreading}}</h2> 
            </div>
        </div>
        <div class="grid padding-top-1rem">
            <div class="flx-col">
                <h2 class="text-secondary">Top 5 Genres</h2>
                <template v-for="genre in top5Genre">
                    <h2 class="font-bold">{{ genre}}</h2>
                </template>
            </div>
            <div class="flx-col">
                <h2 class="text-secondary" style="margin-top: 0.5rem;">Most Read Author</h2>
                <h2 class="no-font-weight">{{mostReadAuthor}}</h2>
                <h2 class="text-secondary" style="margin-top: 0.5rem;">Average Rating</h2>
                <h2 class="no-font-weight">{{avgrating}}</h2> 
            </div> 
        </div>
    </div>
    <v-btn color="primary" @click="generatePNG">Download PNG</v-btn>
    </template>
    
<script setup lang="ts">
    import { ref } from 'vue';
    import { useWrappedStore } from '../store/store';
    import { WrappedDetails } from '../utils/interface';
    import { convertPagesToMinutes, defineWrappedData, getAverage, getBooksCover, getMostReadGenres, getUniqueAuthors, sortBooks } from '../utils/parseBookDetailsMethods';
    import html2canvas from 'html2canvas';


    const store = useWrappedStore();
    const wrappedData = ref(store.getWrappedData).value as WrappedDetails;
    /* util calls */
    defineWrappedData(wrappedData);
    const totalbooks = wrappedData.totalbooksread;
    const minutesspentreading = convertPagesToMinutes();
    const highestBookCovers = getBooksCover(4, 'bookcover', sortBooks('rating'));
    const [mostReadAuthor] = getUniqueAuthors()[1];
    const top5Genre = getMostReadGenres()[1];
    const avgrating = getAverage('rating');

    function generatePNG(){
        const parentElement = document.getElementById('graphic-stats')

        const width = 1080;
        const height = 1920;
        const scale = Math.min(width / parentElement.offsetWidth, height / parentElement.offsetHeight);

        html2canvas(parentElement, {useCORS: true, scale}).then((canvas) => {
            const dataUrl = canvas.toDataURL('readingwrapped/png');
            const downloadLink = document.createElement('a');
            downloadLink.href = dataUrl;
            downloadLink.download = 'readingwrapped.png';
            downloadLink.click();
        })
    }
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
@media (max-width: 768px) {
    .grid:nth-child(2){
        justify-content: space-between;
    }
}

.container{
    margin-bottom: 1.5rem;
}
</style>
