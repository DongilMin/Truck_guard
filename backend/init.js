const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/foodtruck_guard');

const FoodtruckSchema = new mongoose.Schema({
  name: String,
  hygieneGrade: String,
  location: {
    lat: Number,
    lng: Number
  },
  updatedAt: Date
});

const Foodtruck = mongoose.model('Foodtruck', FoodtruckSchema);

Foodtruck.create({
  name: "샘플 푸드트럭",
  hygieneGrade: "A",
  location: { lat: 37.5665, lng: 126.9780 },
  updatedAt: new Date()
}).then(() => {
  console.log("초기 데이터 삽입 완료");
  mongoose.disconnect();
});
