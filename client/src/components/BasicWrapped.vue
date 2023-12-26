<template>
<div class="container padding-top-1rem" >
    <transition name="fade">
        <div>
            <span v-html="introText"></span>
        </div>

    </transition>
</div>
</template>

<script setup lang="ts">
import { ref, toRaw } from 'vue';
import { useWrappedStore } from '../store/store';
import { onMounted } from 'vue';

    const store = useWrappedStore();
    const wrappedData = ref(store.getWrappedData);
    const introText = ref('')
    const username = wrappedData.value.username;
    const totalbooks = wrappedData.value.totalbooksread;
    const totalpages = wrappedData.value.totalpagesread;
    const minutesspentreading = convertPagesToMinutes(totalpages);
    const daysspentreading = convertMinutesToDays(minutesspentreading);
    const longBookCovers = getLongestBooksCover(4);
    const transitionPhases = [
    `2023 was full of highs and lows, but more importantly, it was a year filled with books. <h2 class="text-secondary font-size-3rem">You've read a total of ${ totalbooks} books!</h2>`,
    `You read a total of ${totalpages} pages. According to our calculations, that's a total of ${minutesspentreading} minutes spent across the year`,
    `<h2 class="text-secondary">If that doesn't already sound like a lot, that comes close to ${daysspentreading} days.</h2> These books probably filled a lot more of your time than you wish to admit -
    <div class='flx-dis'>${longBookCovers.map((cover: any) => `<img src="${cover}" alt="Book Cover" class="book-cover" />`).join('')}</div>`
    
    ]
    

    onMounted(() => {
        introText.value = `
        Hi ${username}!
        <h2 class="text-secondary font-size-3rem">Ready to dive into your wrapped?</h2>
        `
        transitionPhases.forEach((phrase, index) => {
        setTimeout(() => {
            introText.value = phrase;
        }, 6000 * (index + 1)); // Adjust the delay based on the index
    });
    })

    function convertPagesToMinutes(pg: string){
        //it takes 2 mins on avg to read a page 
        return (parseInt(pg) * 3)
    }

    function convertMinutesToDays(minutes: number) {
        return Math.round(minutes / (60 * 24));
    }

    function getLongestBooks(){
        let books = wrappedData.value.books;
        return toRaw(books).sort((a: { page: number; },b: { page: number; }) => b.page - a.page)
    }

    function getLongestBooksCover(val: number){
        let books = getLongestBooks();
        console.log(books)
        return books.slice(0,val).map((book: { bookcover: any; }) => book.bookcover);
    }

    function mostReadAuthor(){
        let books = toRaw(wrappedData.value.books);
        books.forEach(book => {
            const author = book.author;
            author[conts]
        })
    }
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
span{
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 500;
    min-height: 60vh;
}
</style>

<style>
.book-cover{
    image-rendering: pixelated;
    width:20%;
    margin: 5px;
}
</style>