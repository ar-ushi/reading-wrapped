import { WrappedDetails } from "./interface";

let wrappedData: WrappedDetails;

export function defineWrappedData (data :  WrappedDetails){
    wrappedData = data;
}

export function convertPagesToMinutes(){
    //it takes 2 mins on avg to read a page 
    return (parseInt(wrappedData.totalpagesread) * 2)
}

export function convertMinutesToDays(minutes: number) {
    return Math.round(minutes / (60 * 24));
}

export function sortBooks(key: string){
    let books = wrappedData.books;
    return (books).sort((a,b) => b[key] - a[key])
}

export function getBooksCover(val: number, key: string,books){
    return books!.slice(0,val).map((book) => book[key]);
}

export function getAverage(key: string){
    let books = wrappedData.books
    const sum = books.reduce((total: any, obj: { [x: string]: any; }) => total + parseInt(obj[key]), 0);
    console.log((sum/parseInt(wrappedData.totalbooksread)).toPrecision(2));
    return (sum/parseInt(wrappedData.totalbooksread)).toPrecision(2);
}

export function getMostReadGenres(){
    const genres = (wrappedData.books).reduce((genreCount, book) => {
        genreCount[book['genre']] = (genreCount[book['genre']] || 0) + 1;
    return genreCount;
    }, {});
    let sortedGenres = Object.keys(genres).sort((a,b) => genres[b] - genres[a])
    let top5Genres = sortedGenres.splice(0,5);
    return [Object.keys(genres).length, top5Genres];
}

export function getUniqueAuthors(){
    const authors = wrappedData.books.map(book => book['author']);
    const uniqueAuthors = new Set(authors);
    const authorCounts = {};
    authors.forEach(author => {
        authorCounts[author] = (authorCounts[author] || 0) + 1;
    })
    let sortedAuthorsByReadCount = Object.keys(authorCounts).sort((a,b) => authorCounts[b] - authorCounts[a])
    let mostFrequentAuthor = sortedAuthorsByReadCount[0].split(',').reverse().join(' ')
    return [uniqueAuthors.size, mostFrequentAuthor, authorCounts[sortedAuthorsByReadCount[0]]];

}