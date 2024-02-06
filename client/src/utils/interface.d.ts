export interface BookDetails {
 'author' : string,
 'page': string,
 'rating': string,
 'avgrating': string,
 'booklink': string,
 'bookcover' : string,
 'readcount': string,
 'month' : string
}

export interface WrappedDetails{
    'username' : string,
    'totalpagesread'?: string,
    'totalbooksread'?: string,
    'month': string[],
    'books': BookDetails[]
}