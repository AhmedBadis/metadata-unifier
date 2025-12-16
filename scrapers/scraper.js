import 'dotenv/config';
import chai from 'chai';
import chaiHttp from 'chai-http';

chai.use(chaiHttp);
const login_url = process.env.SCRAPERS_LOGIN_URL;

chai.request.agent(login_url)
    .post('/specification')  // Ensure this matches the actual endpoint
    .type('form')
    .send({
        username: process.env.SCRAPERS_PAYLOAD_USERNAME,
        password: process.env.SCRAPERS_PAYLOAD_PASSWORD
    })
    .end(function(err, res) {
        if (err) {
            return done(err);
        }

        // Check response status
        console.log(res.status)
    });

chai.request.agent(login_url)
    .post('/login.py')  // Ensure this matches the actual endpoint
    .type('form')
    .send({
        username: process.env.SCRAPERS_PAYLOAD_USERNAME,
        password: process.env.SCRAPERS_PAYLOAD_PASSWORD
    })
    .end(function(err, res) {
        if (err) {
            return done(err);
        }

        // Check response status
        console.log(res.status)
    });