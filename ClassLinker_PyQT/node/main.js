import express from 'express';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Since __dirname is not available in ES module scope, we have to derive it
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = 8000;

// Set the view engine to ejs
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

// Serve static files from the "public" directory
app.use(express.static(__dirname + '/public'));

// Dynamically import node-fetch
import('node-fetch').then(({default: fetch}) => {
    app.get('/', async (req, res) => {
        try {
            // Send POST request to FastAPI
            const response = await fetch('http://127.0.0.1:5000', {
                method: 'POST', // Use POST method
                headers: {
                    'Content-Type': 'application/json',
                },
                // Send JSON string in the request body
                body: JSON.stringify({content: "여기에 전송할 데이터를 입력하세요."})
            });
            const data = await response.json();
            // Make sure to pass the correct data structure to the EJS template
            res.render('index', { message: data.message }); // 수정된 부분
        } catch (error) {
            console.error('Fetch error:', error);
            res.status(500).send('Error fetching data');
        }
    });

    app.listen(port, () => {
        console.log(`Server running at http://127.0.0.1:${port}/`);
    });
}).catch(error => console.error('Failed to load node-fetch:', error));
