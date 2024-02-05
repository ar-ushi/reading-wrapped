<template>
    <div class="container">
        <div v-if="booksread != 0">
            <h1>aru's books read this year</h1>
            <div>
                <div v-for="rowIndex in gridNumber" :key="rowIndex" class="flx-dis">
                    <div v-for="colIndex in gridNumber" :key="colIndex" class="flx-col space-grid">
                        <img 
                            v-if="(rowIndex - 1) * gridNumber + colIndex < booksread"
                            class="grid-book-covers"
                            src="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1647789287i/60177373.jpg"
                        />
                        <div v-else class="grey-block grid-book-covers">{{ (rowIndex - 1) * gridNumber + colIndex }}</div>
                    </div>
                </div> 
            </div>
        </div>
        <div v-else>
            <h1>You've not started your reading journey for this year</h1>
            <h6>It's never too late in the year to pick up a book.</h6>
        </div>
    </div>
</template>

<script setup lang="ts">
    let booksread = 5;
    const gridNumber = Math.ceil(Math.sqrt(booksread))
    console.log(gridNumber)
</script>

<style>
.grid-book-covers{
    height:125px;
    width:100px;
}

.grey-block{
    background-color: #808080; 
    display: flex;
    align-items: center;
    justify-content: space-around;
    font-size: xx-large;
    color: #bcbcbc;
}

.space-grid{
    margin-right: 1rem;
    margin-top: 0.5rem
}
</style>