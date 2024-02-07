/*
    before you run this script, make sure chromadb is started (in the docker container); run:
    npm run "start-chroma"
*/

import { Document } from 'langchain/document';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { HuggingFaceTransformersEmbeddings } from '@langchain/community/embeddings/hf_transformers';
import { Chroma } from '@langchain/community/vectorstores/chroma';

import puppeteer from 'puppeteer';
import dotenv from 'dotenv';
dotenv.config();

const browser = await puppeteer.launch({ headless: 'true' });
console.log('starting crawl');

//** create a new page, specify the user agent to avoid http/2 errors
const page = await browser.newPage();
page.setUserAgent(process.env.USER_AGENT);

//** navigate to the page, wait for it to load
console.log('crawling: ', process.env.WHATS_NEW_IN_OCI_URL);
await page.goto(process.env.WHATS_NEW_IN_OCI_URL)
await page.waitForSelector('.rc84post');

//** grab all the anchor tags off the page
const links = await page.$$eval('section.rc84v1 a', links => links.map(l => l.href));

console.log('crawling each page');

//** follow each and parse the headers and content from the page
let docs = []
for(const link of links.slice(0, 10)) {
    let doc = await parsePage(link);
    if(!!doc.pageContent)
        docs.push(doc);
}

//** create a recursive text splitter; by recursive it means it will try several splitters (\n, \\n, "", " ") until the chunk sizze is achieved
console.log('splitting text');
const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 600, 
    chunkOverlap: 5
})

//** split our collection of documents
const splitDocs = await splitter.splitDocuments(docs);

//** use huggingface transformers to create embeddings/vectors for the content in our documents
const model = new HuggingFaceTransformersEmbeddings({ modelName: 'Xenova/all-MiniLM-L6-v2'});

//** create a chromadb client, and add the split documents
console.log('creating embeddings');
const store = new Chroma(model, { collectionName: 'news' });
await store.addDocuments(splitDocs);

//** perform a sematic search against the vector store
const results = await store.similaritySearch('what tool was released for troubleshooting a kubernetes network configuration');
console.log(results);

await browser.close();

function parsePage(link) {
    return new Promise(async (resolve, reject) => {
        const page = {
            url: link,
            headers: [],
            content: []
        }

        console.log('crawling', link);

        //** create and navigate to a new page
        let linkPage = await browser.newPage();
        linkPage.setUserAgent(process.env.USER_AGENT);
        await linkPage.goto(link);

        //** grab the headers content off the page
        page.headers = await linkPage.$$eval('h2', headers => headers.map(header => header.textContent));
        page.content = await linkPage.$$eval('p', ps => ps.map(p => p.textContent));

        const doc = new Document({ 
            pageContent: (page.headers.join(' ') + page.content.join(' ')) || '', 
            metadata: {
                source: link
            }
        });

        resolve(doc);
    });
}
