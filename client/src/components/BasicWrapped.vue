<template>
<div class="container padding-top-1rem flx-dis" >
    <v-stepper non-linear color="primary" flat mobile bg-color="transparent" :items="items" min-width="80%" max-width="80%" min-height="60%" max-height="60%" step="6">
        <v-stepper-window>
            <v-stepper-window-item v-for="(phrase, i) in stepperPhrases" :value="i+1" :key="`${i}--content`">
            <v-card v-html="phrase" color="transparent"></v-card>
            </v-stepper-window-item>
            <v-stepper-window-item :value="6">
                <h5 class="text-secondary">On some days, you agreed with all the rage on Goodreads!</h5>
                <div class="grid padding-top-1rem">
                    <div class="flx" v-for="(item, index) in categoriseByPopularOpinion" :key="index">
                <template v-if="item">
                    <img :src="item.bookcover" class="opinion-cover" />
                    <div class="grid flx-col" style="margin-left: 5px;">
                        <div class="flx-col">
                            <div class="rating-text">Average Rating</div>
                            <h2 class="text-warning">{{item.avgrating}}</h2>
                        </div>
                    <div class="flx-col">
                        <div class="rating-text">Your Rating</div>
                        <h2 class="text-secondary">{{item.rating}}</h2>
                    </div>
                    </div>                    
                </template>
                </div>
                </div>
                <h5 class="padding-top-1rem text-secondary">On other days, you held opinions strictly against the crowd.</h5>
                <div class="grid padding-top-1rem">
                    <div class="flx" v-for="(item, index) in categoriseByUnpopularOpinion" :key="index">
                <template v-if="item">
                    <img :src="item.bookcover" class="opinion-cover" />
                    <div class="grid flx-col" style="margin-left: 5px;">
                        <div class="flx-col">
                            <div class="rating-text">Average Rating</div>
                            <h2 class="text-warning">{{item.avgrating}}</h2>
                        </div>
                    <div class="flx-col">
                        <div class="rating-text">Your Rating</div>
                        <h2 class="text-secondary">{{item.rating}}</h2>
                    </div>
                    </div>                    
                </template>
                </div>
                </div>
            </v-stepper-window-item>
            <v-stepper-window-item :value="7" :key="`7--content`">
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

    const store = useWrappedStore();
    const items: string[] = [ '1', '2', '3', '4', '5', '6', '7'];
    const wrappedData = ref(store.getWrappedData);
    const totalbooks = wrappedData.value.totalbooksread;
    const totalpages = wrappedData.value.totalpagesread;
    const minutesspentreading = convertPagesToMinutes(totalpages);
    const daysspentreading = convertMinutesToDays(minutesspentreading);
    const avgrating = getAverage('rating');
    const avgpageread = Math.round(getAverage('page'));
    const longBookCovers = getBooksCover(4, 'bookcover', sortBooks('page'));
    const highestRatedBookCovers = getBooksCover(5, 'bookcover', sortBooks('rating'))
    const [categoriseByPopularOpinion, categoriseByUnpopularOpinion] = groupPopularOpinion();
    const avgratingtext = () => {
        let text = '';
        if (avgrating >= 3.5){
            text += `Why wouldn't you read so much when you've had such a good year? <h2 class="text-secondary">Your average rating for the year was ${avgrating}</h2>`
        } else {
            text += `We hope you had fun reading this year. <h2 class="text-secondary"Your average rating for the year was ${avgrating} </h2>`
        }
        text+= ` <span class="font-bold font-size-1.5rem">Here are some of your highest rated books of the year</span><div class='flx-dis'>${highestRatedBookCovers.map((cover: any) => `<img src="${cover}" alt="Book Cover" class="book-cover" />`).join('')}</div>`
        return text;
    }
    const stepperPhrases = [
        `<h2 class="text-secondary font-size-3rem">Ready to dive into your wrapped?</h2>`,
        `This year was full of highs and lows, but more importantly, it was a year filled with books. <h2 class="text-secondary font-size-3rem">You've read a total of ${totalbooks} books!</h2>`,
        `The average book length was <span class="font-bold"> ${avgpageread} </span> pages and you read a total of <span class="font-bold"> ${totalpages} </span> pages. According to our calculations, that's <h1 class="text-secondary">${minutesspentreading} minutes </h1> spent throughout the year.`,
        `If that doesn't already sound like a lot, <h2 class="text-secondary">that comes close to ${daysspentreading} days.</h2> <span class="font-bold font-size-1.5rem">These books probably took up your time </span>
        <div class='flx-dis'>${longBookCovers.map((cover: any) => `<img src="${cover}" alt="Book Cover" class="book-cover" />`).join('')}</div>`,  
        avgratingtext(),
    ]
    function convertPagesToMinutes(pg: string){
        //it takes 2 mins on avg to read a page 
        return (parseInt(pg) * 3)
    }

    function convertMinutesToDays(minutes: number) {
        return Math.round(minutes / (60 * 24));
    }

    function sortBooks(key: string){
        let books = wrappedData.value.books;
        return toRaw(books).sort((a,b) => b[key] - a[key])
    }

    function getBooksCover(val: number, key: string,books){
        return books!.slice(0,val).map((book) => book[key]);
    }

    function getAverage(key: string){
        const sum = toRaw(wrappedData.value.books).reduce((total: any, obj: { [x: string]: any; }) => total + obj[key], 0);
        return sum/totalbooks;
    }

    function groupPopularOpinion(){
        let key1 = 'rating';
        let key2 = 'avgrating'
        let books = toRaw(wrappedData.value.books);
        let bucket = '4';
        let finalPopularResult = [];
        let finalUnpopularResult = [];
        const popularOpinions = books.reduce((res, book) => {
            if (book[key1]>= 4 && book[key2] >=4){
                res['4'].push(book);
            } else if (book[key1] >= 3 && book[key1] < 4 && book[key2] >= 3 && book[key2] < 4){
                res['3'].push(book)
            } else if (book[key1] <=2 && book[key2] <=2) {
                res['2'].push(book);
            } else {
                res['unpopular'].push(book);
            }
            return res; 
        }, {'4' : [], '3': [], '2': [], 'unpopular': []})
        while (finalPopularResult.length < 3){
            const randomBook = Math.floor(Math.random() * (popularOpinions[bucket].length))
            finalPopularResult.push(popularOpinions[bucket][randomBook])
            bucket = bucket === '4' ? '3' : bucket === '3' ? '2' : '4'
        }
        while (finalUnpopularResult.length < 3){
            const randomBook = Math.floor(Math.random() * (popularOpinions['unpopular'].length))
            finalUnpopularResult.push(popularOpinions['unpopular'][randomBook])
        }
        return [finalPopularResult, finalUnpopularResult];
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
.opinion-cover{
    max-width:100px;
    height: 125px;
}

.rating-text{
    font-size: 12px;
    font-weight: 500;
}

.grid{
    display: flex;
    justify-content: space-evenly;
    place-items: center;
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
.v-stepper-item{
    color: var(--v-theme-primary);
}

.font-bold{
    font-weight: 600;
}

.font-size-1.5rem{
    font-size: 1.5rem;
}

</style>