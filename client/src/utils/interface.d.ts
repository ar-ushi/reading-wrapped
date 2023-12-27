export interface BookDetails {
 'author' : string,
 'page': string,
 'rating': string,
 'avgrating': string,
 'booklink': booklink,
 'bookcover' : bookcover   
}

export interface WrappedDetails{
    'username' : string,
    'totalpagesread': string,
    'totalbooksread': string,
    'month': string[],
    'books': BookDetails[]
}