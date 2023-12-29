<template>
<div class="container padding-top-1rem flx-dis" >
    <v-stepper non-linear color="primary" flat mobile bg-color="transparent" :items="items" min-width="80%" max-width="80%" min-height="60%" max-height="60%">
        <v-stepper-window>
            <v-stepper-window-item v-for="(phrase, i) in stepperPhrases" :value="i+1" :key="`${i}--content`">
            <v-card v-html="phrase" color="transparent"></v-card>
            </v-stepper-window-item>
            <v-stepper-window-item :value="8">
                <h4 class="text-secondary" style="padding-bottom: 10px;">On some days, you agreed with all the rage on Goodreads!</h4>
                <book-opinions :items="categoriseByPopularOpinion"/>
                <h4 class="padding-top-1rem text-secondary">On other days, you held opinions strictly against the crowd.</h4>
                <book-opinions :items="categoriseByUnpopularOpinion" />
            </v-stepper-window-item>
            <v-stepper-window-item :value="9" :key="`8--content`">
                <basic-graphics />
            </v-stepper-window-item>
        </v-stepper-window>
    </v-stepper>
</div>
</template>

<script setup lang="ts">
import { ref, toRaw } from 'vue';
import { useWrappedStore } from '../store/store';
import BasicGraphics from './BasicGraphics.vue';
import BookOpinions from './BookOpinions.vue';
import { WrappedDetails } from '../utils/interface';

    const store = useWrappedStore();
    const items: string[] = [ '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    const wrappedData = ref(store.getWrappedData).value as WrappedDetails;
    const totalbooks = wrappedData.totalbooksread;
    const totalpages = wrappedData.totalpagesread;
    const minutesspentreading = convertPagesToMinutes(totalpages);
    const daysspentreading = convertMinutesToDays(minutesspentreading);
    const avgrating = getAverage('rating');
    const avgpageread = Math.round(getAverage('page'));
    const longBookCovers = getBooksCover(4, 'bookcover', sortBooks('page'));
    const highestRatedBookCovers = getBooksCover(5, 'bookcover', sortBooks('rating'))
    const [categoriseByPopularOpinion, categoriseByUnpopularOpinion] = groupPopularOpinion();
    const [totalAuthorsRead, mostReadAuthor, mostReadBooksByAuthor] = getUniqueAuthors();
    const [countOfTotalGenres,top5Genre] = getMostReadGenres();
    const avgratingtext = () => {
        let text = '';
        if (avgrating >= 3.5){
            text += `Why wouldn't you read so much when you've had such a good year? <h2 class="text-secondary">Your average rating for the year was ${avgrating}</h2>`
        } else {
            text += `We hope you had fun reading this year. <h2 class="text-secondary"Your average rating for the year was ${avgrating} </h2>`
        }
        text+= ` <span class="font-bold font-size-1rem">Here are some of your highest rated books of the year</span><div class='flx-dis'>${highestRatedBookCovers.map((cover: any) => `<img src="${cover}" alt="Book Cover" class="book-cover" />`).join('')}</div>`
        return text;
    }
    const stepperPhrases = [
        `<h2 class="text-secondary font-size-3rem">Ready to dive into your wrapped?</h2>`,
        `This year was full of highs and lows, but more importantly, it was a year filled with books. <h2 class="text-secondary font-size-3rem">You've read a total of ${totalbooks} books!</h2>`,
        `The average book length was <span class="font-bold"> ${avgpageread} </span> pages and you read a total of <span class="font-bold"> ${totalpages} </span> pages. According to our calculations, that's <h1 class="text-secondary">${minutesspentreading} minutes </h1> spent throughout the year.`,
        `If that doesn't already sound like a lot, <h2 class="text-secondary">that comes close to ${daysspentreading} days.</h2> <span class="font-bold font-size-1.5rem">These books probably took up your time </span>
        <div class='flx-dis'>${longBookCovers.map((cover: any) => `<img src="${cover}" alt="Book Cover" class="book-cover" />`).join('')}</div>`,  
        avgratingtext(),
        `You read from a total of ${totalAuthorsRead} authors but one clearly stole your heart.</br> You enjoyed reading from <h2 class="text-secondary">${mostReadAuthor}</h2> the most with <span class="text-secondary font-bold"> ${mostReadBooksByAuthor} </span> books`,
        `Speaking of stealing your heart, you read a whopping total of <span class="text-secondary font-bold">${countOfTotalGenres} </span> unique genres this year. <div class='flx-col'> <h2 class="text-secondary">Top 5 Genres </h2> ${(top5Genre as string[]).map((genre: string) => `<span class="font-bold"> ${genre} </span>`).join('')} </div>`
    ]

    function convertPagesToMinutes(pg: string){
        //it takes 2 mins on avg to read a page 
        return (parseInt(pg) * 3)
    }

    function convertMinutesToDays(minutes: number) {
        return Math.round(minutes / (60 * 24));
    }

    function sortBooks(key: string){
        let books = wrappedData.books;
        return toRaw(books).sort((a,b) => b[key] - a[key])
    }

    function getBooksCover(val: number, key: string,books){
        return books!.slice(0,val).map((book) => book[key]);
    }

    function getAverage(key: string){
        const sum = toRaw(wrappedData.books).reduce((total: any, obj: { [x: string]: any; }) => total + obj[key], 0);
        return sum/parseInt(totalbooks);
    }

    function groupPopularOpinion(){
        let key1 = 'rating';
        let key2 = 'avgrating'
        let books = toRaw(wrappedData.books);
        let bucket = '4';
        let finalPopularResult = [];
        let finalUnpopularResult = [];
        let randomBook;
        const popularOpinions = books.reduce((res, book) => {
            if (book[key1]>= 3.7 && book[key2] >=3.7){
                res['4'].push(book);
            } else if (book[key1] >= 3 && book[key1] < 3.7 && book[key2] >= 3 && book[key2] < 3.7){
                res['3'].push(book)
            } else if (book[key1] <=2 && book[key2] <=2) {
                res['2'].push(book);
            } else {
                res['unpopular'].push(book);
            }
            return res; 
        }, {'4' : [], '3': [], '2': [], 'unpopular': []})
        while (finalPopularResult.length < 3){
            let usedIndices = [];
            do {
                randomBook = Math.floor(Math.random() * (popularOpinions[bucket].length))
            } while (usedIndices.includes(randomBook));
            if (popularOpinions[bucket][randomBook]){
                finalPopularResult.push(popularOpinions[bucket][randomBook])
            }
            usedIndices.push(randomBook);
            bucket = bucket === '4' ? '3' : bucket === '3' ? '2' : '4'
        }
        while (finalUnpopularResult.length < 3){
            let usedIndices = [];
            do {
            randomBook = Math.floor(Math.random() * (popularOpinions['unpopular'].length))
            } while (usedIndices.includes(randomBook));
            finalUnpopularResult.push(popularOpinions['unpopular'][randomBook]);
            usedIndices.push(randomBook);
        }
        return [finalPopularResult, finalUnpopularResult];
    }

    function getUniqueAuthors(){
        const authors = toRaw(wrappedData.books).map(book => book['author']);
        const uniqueAuthors = new Set(authors);
        const authorCounts = {};
        authors.forEach(author => {
            authorCounts[author] = (authorCounts[author] || 0) + 1;
        })
        let sortedAuthorsByReadCount = Object.keys(authorCounts).sort((a,b) => authorCounts[b] - authorCounts[a])
        let mostFrequentAuthor = sortedAuthorsByReadCount[0].split(',').reverse().join(' ')
        return [uniqueAuthors.size, mostFrequentAuthor, authorCounts[sortedAuthorsByReadCount[0]]];
    }

    function getMostReadGenres(){
        const genres = toRaw(wrappedData.books).reduce((genreCount, book) => {
            genreCount[book['genre']] = (genreCount[book['genre']] || 0) + 1;
        return genreCount;
        }, {});
        let sortedGenres = Object.keys(genres).sort((a,b) => genres[b] - genres[a])
        let top5Genres = sortedGenres.splice(0,5);
        console.log(top5Genres)
        return [Object.keys(genres).length, top5Genres];
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
    min-height: 50vh;
}
h4{
    margin-block-start: 0;
}
</style>

<style>
.book-cover{
    width:15%;
    height: 30%;
    margin: 5px;
}

.v-stepper-header{
    height:50px;
    box-shadow: none;
}
.v-stepper-item__avatar.v-avatar{
    background: rgb(var(--v-theme-primary));
    color: white;
    font-weight: 500;
}

.v-stepper-item--complete .v-stepper-item__avatar.v-avatar, .v-stepper-item--selected .v-stepper-item__avatar.v-avatar{
    background: rgba(var(--v-theme-secondary));
} 

.font-bold{
    font-weight: 600;
}

.font-size-2rem{
    font-size: 2rem;
}

.font-size-1rem{
    font-size: 1rem;
}

</style>