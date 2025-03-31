const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('MongoDB 연결 성공'))
  .catch(err => console.log('MongoDB 연결 실패', err));

app.use('/api/foodtrucks', require('./routes/foodtrucks'));

app.listen(process.env.PORT, () => {
  console.log(`서버가 http://localhost:${process.env.PORT} 에서 실행 중입니다.`);
});
