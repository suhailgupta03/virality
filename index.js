const express = require('express');
let app = express();
const bodyParser = require('body-parser');
const http = require('http');
const Joi = require('joi');
const schema = require('./schema');
const { spawn } = require('child_process');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json({ limit: 2097152 }));
// Retrieve the raw body as a buffer and match all content types
app.use(bodyParser.raw({ type: "*/*" }));



let httpServer = http.createServer(app);

httpServer.listen(4000, (err) => { // Start the http server
    if (!err)
        console.log(`Process (http) ${process.pid} listening at 4000`);
});


app.get('/', (req, resp, next) => {
    resp.json({
        message: 'Hi!'
    })
});


app.post('/predict', async (req, resp, next) => {

    try {
        const { error, value } = Joi.validate(req.body, schema.Predict);
        if (error) {
            resp.json({
                status: false,
                message: error
            });
        } else {
            const model = spawn('python3', [
                'call-gcloud-ml.py',
                '--sentiment',
                value.sentiment,
                '--post_length',
                value.postLength,
                '--hash_tag_count',
                value.hashTagCount,
                '--content_url_count',
                value.contentURLCount,
                '--like_count',
                value.likeCount,
                '--share_count',
                value.shareCount,
                '--comment_count',
                value.commentCount,
                '--followers_count',
                value.followersCount,
                '--following_count',
                value.followingCount,
                '--tweet_count',
                value.tweetCount,
                '--gender',
                value.gender,
                '--seconds_elapsed',
                value.secondsElapsed
            ]);

            let score = null;
            model.stdout.on('data', (data) => {
                score = JSON.parse(data).score;
            });

            model.stderr.on('data', (data) => {
                console.log(`stderr: ${data}`);
            });

            model.on('close', (code) => {
                resp.json({
                    status: code == 0 ? true : false,
                    score
                });
            });
        }
    } catch (err) {
        resp.json({
            status: false,
            message: err.message
        });
    }

});