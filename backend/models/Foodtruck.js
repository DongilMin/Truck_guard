const mongoose = require('mongoose');

const FoodtruckSchema = new mongoose.Schema({
    license_no: String,
    permission_date: String,
    organization: String,
    business_name: String,
    address: String,
    ceo_name: String,
    tel_no: String,
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Foodtruck', FoodtruckSchema);
