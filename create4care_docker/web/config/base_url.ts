export function getBaseUrl(): string {
    const protocol = window.location.protocol; // "http:" or "https:"
    const hostname = window.location.hostname; // "localhost"
    return `${protocol}//api.${hostname}`
    // return `https://api.${hostname}`
}
